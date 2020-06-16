/* SPDX-License-Identifier: LGPL-2.1-only */

/**
 * @file umd_pcan.hpp
 *
 * @brief Relay control using PCAN library 
 * 
 * Relay control using PCAN library 
 * 
 * Contact:    <jdj2261@unmansol.com>
 * Maintainer: Stephane Grosjean <s.grosjean@peak-system.com>
 * Author:     Dae Jong Jin <jdj2261@github.com>
 *
 **/

/*****************************************************************************
** Ifdefs
*****************************************************************************/
#ifndef NO_RT
#include <sys/mman.h>

#ifdef RTAI
#include <rtai_lxrt.h>
#endif

// PCAN-Basic device used to read on
// (RT version doesn't handle USB devices)
#define PCAN_DEVICE	PCAN_PCIBUS1
#else

// PCAN-Basic device used to read on
#define PCAN_DEVICE	PCAN_USBBUS1
#endif



#ifndef UMD_PCAN_H
#define UMD_PCAN_H

#define MAX_VEL		7800
#define INCREMENT 	10.017
inline unsigned long THRESHOLD(int x)
{
	return (MAX_VEL/90) * x;
} 
/*****************************************************************************
** Includes
*****************************************************************************/
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <string.h>
#include <asm/types.h>
#include <iostream>
#include <math.h>
#include "PCANBasic.h"

namespace unmansol
{
	namespace can
	{
		class Pcan
		{
		private:
			/* Variables */
			unsigned int _device;
			unsigned long _ulIndex;
			unsigned int _send_data;
			unsigned int _square;
			unsigned int _parse_data;

			int _curStatus;
			int _preStatus;
			int _degree;

			/* data */
		public:

			/**
			 * Default Constructor
			 */
			Pcan(/* args */);

			/**
			 * Copy Constructor
			 *
			 * @param device
			 *      The <code>Exception</code> instance to copy.
			 */
			Pcan(unsigned int device, int degree);
			
			/**
			 * DeConstructor
			 */

			virtual ~Pcan();

			TPCANMsg _RMessage;
			TPCANMsg _TMessage;
			TPCANStatus _RStatus;
			TPCANStatus _TStatus;
			TPCANMsg receive_all();
			unsigned int read();
			bool onInitialize();
			void onStart();
			void onExcute();

			void write(unsigned int data);
			unsigned int parse_rawdata(TPCANMsg msg);
			void compare(unsigned long threshold);

			static void signal_handler(int s)
			{
				printf("Interrupted by SIG%u!\n", s);
				exit(1);
			}
			
		};		
	}	// namespace can
} 		// namespace unmansol
#endif

