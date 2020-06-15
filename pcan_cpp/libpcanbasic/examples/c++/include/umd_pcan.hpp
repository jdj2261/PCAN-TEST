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
#include "PCANBasic.h"

namespace unmansol
{
	namespace can
	{
		class Pcan
		{
		private:
			/* Variables */
			unsigned int Device;
			unsigned long ulIndex = 0;
			unsigned int send_data = 0;
			unsigned int square = 0;

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
			Pcan(unsigned int device);
			
			/**
			 * DeConstructor
			 */

			virtual ~Pcan();

			TPCANMsg RMessage;
			TPCANMsg TMessage;
			TPCANStatus Status;

			bool onInitialize();
			void onStart();
			void onExcute();

			void read();
			void write();

			TPCANMsg receive_all();
			int parse_rawdata(TPCANMsg msg);

			static void signal_handler(int s)
			{
				printf("Interrupted by SIG%u!\n", s);
			}
		};		
	}	// namespace can
} 		// namespace unmansol
#endif

