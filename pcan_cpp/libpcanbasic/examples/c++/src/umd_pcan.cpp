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

    Pcan::Pcan(unsigned int device, int degree) 
        : _device(0)
        , _ulIndex(0)
		, _send_data(0)
		, _square(0)
		, _parse_data(0)
        , _curStatus(0)
        , _preStatus(0)
    {
        this->_device = device; 
        this->_device = degree;
        printf("Degree : %d \n", degree);
    }

    Pcan::~Pcan()
    {
    }
        
    bool Pcan::onInitialize()
    {
        std::cout << "Initialize" << std::endl;
        this->_RStatus = CAN_Initialize(this->_device, PCAN_BAUD_500K, 0, 0, 0);  

        /* 
        *  TMessage Init
        */
        this->_TMessage.ID = 0x181;
        this->_TMessage.LEN = 8;
        this->_TMessage.MSGTYPE = PCAN_MESSAGE_STANDARD;
        memset(this->_TMessage.DATA, '\0', sizeof(this->_TMessage.DATA));

        // 0이 아니면 종료
        if (this->_RStatus) exit(1);
        else return true;

    }

    void Pcan::onExcute()
    {
        std::cout << "Excute" << std::endl;
        
        while (1) 
        {

            this->_parse_data = this->read();
            this->compare(THRESHOLD(90));

            if (this->_RStatus != PCAN_ERROR_OK) 
            {
                printf("CAN_Read(%xh) failure 0x%x\n", this->_device, (int)this->_RStatus);
                break;
            }

            if (_TStatus != PCAN_ERROR_OK) 
            {
			printf("CAN_Write(%xh) failure 0x%x\n", this->_device, (int)this->_TStatus);
			// break;
		    }
        }
    }

    void Pcan::onStart()
    {
        std::cout << "Start" << std::endl;
        bool isConnect = onInitialize();
        if (isConnect) onExcute();
    }

    unsigned int Pcan::read()
    {
        TPCANMsg receive_data;

        receive_data = receive_all();
        return parse_rawdata(receive_data);
    }

    TPCANMsg Pcan::receive_all()
    {
        while ((this->_RStatus=CAN_Read(this->_device, &_RMessage, NULL)) == PCAN_ERROR_QRCVEMPTY)
            if (usleep(100))
                break;

        // printf("  - R ID:%4x LEN:%1x DATA:%02x %02x %02x %02x %02x %02x %02x %02x\n",
        //     (int)_RMessage.ID, (int)_RMessage.LEN,
        //     (int)_RMessage.DATA[0], (int)_RMessage.DATA[1],
        //     (int)_RMessage.DATA[2], (int)_RMessage.DATA[3],
        //     (int)_RMessage.DATA[4], (int)_RMessage.DATA[5],
        //     (int)_RMessage.DATA[6], (int)_RMessage.DATA[7]);
        
        return _RMessage;
    }

    unsigned int Pcan::parse_rawdata(TPCANMsg msg)
    {
        unsigned int result_data;
        result_data = (msg.DATA[0]) | (msg.DATA[1] << 8);
        std::cout << result_data << std::endl; 
        return result_data;
    }

    void Pcan::write(unsigned int data)
    {
        unsigned int send_data;
        send_data = data;
        _TMessage.DATA[0] = 0x20;
        _TMessage.DATA[1] = 0x00;
        _TMessage.DATA[2] = 0x00;
        _TMessage.DATA[3] = 0x01;
        _TMessage.DATA[4] = send_data;
		_TStatus = CAN_Write(this->_device, &_TMessage);
    }

    void Pcan::compare(unsigned long threshold)
    {
        unsigned int read_data;
        unsigned int send_data;

        read_data = this->_parse_data;

        if(read_data == 0)
        {
            _curStatus = 0;
            send_data = 0;
        }
        else if(read_data >= threshold && read_data <= 65535-threshold)
            _curStatus = threshold;
        
        int right_rotate_data = read_data - 65535;
        int left_rotate_data = read_data;

        for(int i = 0; i < 8 ; i++)
        {
            if ((int)(INCREMENT * _degree) * (-1) * (i+1) < right_rotate_data && 
                right_rotate_data< (int)(INCREMENT * _degree) * (-1) * (i))
                {
                    _curStatus = (-1) * (i+1);
                }
            else if ((int)(INCREMENT * _degree) * (-1) * (i+1) < left_rotate_data &&
                left_rotate_data< (int)(INCREMENT * _degree) * (-1) * (i))
                {
                    _curStatus = i+1;
                }
            
            if (_preStatus != _curStatus)
            {
                printf("prestatus : %d, curstatus : %d", _preStatus, _curStatus);
            
                if      (_curStatus == i+1)         send_data = pow(2,i+1)-1;
                else if (_curStatus == (-1)*(i+1))  send_data = pow(2,i+1) * (pow(2,8-(i+1))-1);
                else if (_curStatus == threshold)   send_data = 0x81;

                this->write(send_data);
                _preStatus = _curStatus;
                
            }
        }
    }

    } //namespace can

} // namespace unmansol


int main(int argc, char* argv[])
{
    unmansol::can::Pcan umd_pcan;
    while(true)
    {

        int degree;
        std::cout << "원하는 각도를 입력하세요 : " << std::endl;
        std::cin >> degree; 

        if (0< degree && degree<= 90) 
        {
            unsigned int pcan_device = PCAN_DEVICE;

            unmansol::can::Pcan umd_pcan(pcan_device, degree);

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
                
        }
        else 
        {
            if (!std::cin)
            {
                std::cout << "숫자만 입력해 주세요." << std::endl;
                std::cin.clear();
                std::cin.ignore(__INT_MAX__, '\n');
            }
            else printf("90도 이하로 입력해 주세요. \n");
        }
    }

    return 0;

}

