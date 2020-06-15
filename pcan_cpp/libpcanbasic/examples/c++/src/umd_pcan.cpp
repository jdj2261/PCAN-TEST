#include "umd_pcan.hpp"

////////////////////////////////////////////////////////////////////////////////////////////////////
/// <summary>	Main entry-point for this application. </summary>
///
/// <remarks>	 </remarks>
///
/// <param name="argc">	The argc. </param>
/// <param name="argv">	[in,out] If non-null, the argv. </param>
///
/// <returns>	. </returns>
////////////////////////////////////////////////////////////////////////////////////////////////////

namespace unmansol

{
    namespace can
    {

    Pcan::Pcan()
    {

    }

    Pcan::Pcan(unsigned int device) 
        : Device(0)
    {
        this->Device = device; 
    }

    Pcan::~Pcan()
    {
    }
        
    bool Pcan::onInitialize()
    {
        std::cout << "Initialize" << std::endl;
        this->Status = CAN_Initialize(this->Device, PCAN_BAUD_500K, 0, 0, 0);  

        /* 
        *  TMessage Init
        */
        this->TMessage.ID = 0x181;
        this->TMessage.LEN = 8;
        this->TMessage.MSGTYPE = PCAN_MESSAGE_STANDARD;
        memset(this->TMessage.DATA, '\0', sizeof(this->TMessage.DATA));

        // 0이 아니면 종료
        if (this->Status) exit(1);
        else return true;

    }

    void Pcan::onExcute()
    {
        std::cout << "Excute" << std::endl;
        while (1) 
        {

            this->read();

            if (Status != PCAN_ERROR_OK) 
            {
                printf("CAN_Read(%xh) failure 0x%x\n", this->Device, (int)Status);
                break;
            }

            // this->write();

            // if (Status != PCAN_ERROR_QXMTFULL) 
            // {
            //     printf("CAN_Write(%xh): Error 0x%x\n", this->Device, (int)Status);
            //     break;
            // }
            // printf("  - S ID:%4x LEN:%1x DATA:%02x %02x %02x %02x %02x %02x %02x %02x\n",
            // (int) TMessage.ID, (int) TMessage.LEN, (int) TMessage.DATA[0],
            // (int) TMessage.DATA[1], (int) TMessage.DATA[2],
            // (int) TMessage.DATA[3], (int) TMessage.DATA[4],
            // (int) TMessage.DATA[5], (int) TMessage.DATA[6],
            // (int) TMessage.DATA[7]);

            // sleep(1);
        }
    }

    void Pcan::onStart()
    {
        std::cout << "Start" << std::endl;
        bool isConnect = onInitialize();
        if (isConnect) onExcute();
    }

    void Pcan::read()
    {
        TPCANMsg receive_data;

        receive_data = receive_all();
        parse_rawdata(receive_data);


    }

    TPCANMsg Pcan::receive_all()
    {
        while ((this->Status=CAN_Read(this->Device, &RMessage, NULL)) == PCAN_ERROR_QRCVEMPTY)
            if (usleep(100))
                break;

        printf("  - R ID:%4x LEN:%1x DATA:%02x %02x %02x %02x %02x %02x %02x %02x\n",
            (int)RMessage.ID, (int)RMessage.LEN,
            (int)RMessage.DATA[0], (int)RMessage.DATA[1],
            (int)RMessage.DATA[2], (int)RMessage.DATA[3],
            (int)RMessage.DATA[4], (int)RMessage.DATA[5],
            (int)RMessage.DATA[6], (int)RMessage.DATA[7]);
        
        return RMessage;
    }

    int Pcan::parse_rawdata(TPCANMsg msg)
    {
        int parse_data = (int)msg.DATA[1] + (int)msg.DATA[0];
        std::cout << parse_data << std::endl; 
    }

    void Pcan::write()
    {
        while ((this->Status = CAN_Write(this->Device, &(this->TMessage))) == PCAN_ERROR_OK) 
        {
			// increment data bytes
			for (int i = 0; i < 8; i++)
				if (++ (this->TMessage.DATA[i]))
					break;
        }
        
    }

    } //namespace can

} // namespace unmansol




int main(int argc, char* argv[])
{
    // unmansol::can::Pcan umd_pcan;
    unsigned int pcan_device = PCAN_DEVICE;
    unmansol::can::Pcan umd_pcan(pcan_device);

#ifndef NO_RT
	mlockall(MCL_CURRENT | MCL_FUTURE);

#ifdef RTAI
	// Initialize LXRT
	RT_TASK *mainr = rt_task_init_schmod(nam2num("MAINR"), 0, 0, 0,
					     SCHED_FIFO, 0xF);
	if (!mainr) {
		printf("pcanread(%xh): unable to setup main RT task\n",
			PCAN_DEVICE);
		return -1;
	}
	rt_make_hard_real_time();
#endif
#endif

	// get the device from the cmd line if provided
	if (argc > 1) {
		char *endptr;
		unsigned long tmp = strtoul(argv[1], &endptr, 0); 
		if (*endptr == '\0')
			pcan_device = tmp;
	}

	// below usleep() will be INTRuptible by user
	signal(SIGINT, umd_pcan.signal_handler);
    umd_pcan.onStart();
    

	return 0;
}

