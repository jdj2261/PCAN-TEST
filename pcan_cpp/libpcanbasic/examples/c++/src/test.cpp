#include <iostream>
#include <stdio.h>

using namespace std;
int main()
{

    while(1)
    {
        int degree;
        std::cout << "원하는 각도를 입력하세요 : " << std::endl;
        std::cin >> degree; 
        // printf()
        if (0< degree && degree<= 90) 
        {
            printf("잘 입력했어요");
        }
        else printf("다시 입력하세요: \n");
    
    }
    // cout << "Hello" << endl;
    
    // int a = 1;
    // int b = 0x11;
    // int c = a | (b<<8);
    // cout << c << endl;
    // printf("%02x\n", a);

    // if (0<a<5){
    //     printf("test");
    // }


    return 0;
}

//    unmansol::can::Pcan umd_pcan;
//     while(true)
//     {
//         try
//         {
//             int degree;
//             std::cout << "원하는 각도를 입력하세요 : " << std::endl;
//             std::cin >> degree; 

//             if (degree < 0 || degree > 90)  printf("90도 이하로 입력하세요");
//             unsigned int pcan_device = PCAN_DEVICE;
    
//             unmansol::can::Pcan umd_pcan(pcan_device, degree);
