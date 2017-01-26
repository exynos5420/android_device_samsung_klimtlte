/*
   Copyright (c) 2013, The Linux Foundation. All rights reserved.

   Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions are
   met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above
      copyright notice, this list of conditions and the following
      disclaimer in the documentation and/or other materials provided
      with the distribution.
    * Neither the name of The Linux Foundation nor the names of its
      contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

   THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED
   WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
   MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT
   ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS
   BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
   CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
   SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
   BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
   OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
   IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#include <stdlib.h>

#include "vendor_init.h"
#include "property_service.h"
#include "util.h"

#define DEVICE_NAME "klimt"

static void set_device(const char *radio,
		       const char *region,
		       const char *model)
{
	char device[16], name[16];

	sprintf(device, "%s%s", DEVICE_NAME, radio);
	sprintf(name, "%s%s", device, region);

	property_set("ro.product.name", name);
	property_set("ro.product.device", device);
	property_set("ro.product.model", model);
}

void vendor_load_properties()
{
	char bootloader[PROP_VALUE_MAX];

	property_get("ro.bootloader", bootloader);
	if (strstr(bootloader, "T705M")) {
		/* South Americas */
		set_device("lte", "ub", "SM-T705M");
		property_set("ro.build.description", "klimtlteub-user 6.0.1 MMB29K T705MUBU1CPJ1 release-keys");
		property_set("ro.build.fingerprint", "samsung/klimtlteub/klimtlte:6.0.1/MMB29K/T705MUBU1CPJ1:user/release-keys");
	} else if (strstr(bootloader, "T705W")) {
		/* Canada */
		set_device("lte", "can", "SM-T705W");
		property_set("ro.build.description", "klimtltevl-user 5.0.2 LRX22G T705WVLU1BOD7 release-keys");
		property_set("ro.build.fingerprint", "samsung/klimtltevl/klimtltecan:5.0.2/LRX22G/T705WVLU1BOD7:user/release-keys");
	} else if (strstr(bootloader, "T705Y")) {
		/* Oceanic */
		set_device("lte", "do", "SM-T705Y");
		property_set("ro.build.description", "klimtltedo-user 6.0.1 LMY49M T705YDOU1CPI4 release-keys");
		property_set("ro.build.fingerprint", "samsung/klimtltedo/klimtlte:6.0.1/MMB29K/T705YDOU1CPI4:user/release-keys");
	} else {
		/* all other variants become International LTE */
		set_device("lte", "xx", "SM-T705");
		property_set("ro.build.description", "klimtltexx-user 6.0.1 MMB29K T705DDU1CPL3 release-keys");
		property_set("ro.build.fingerprint", "samsung/klimtltexx/klimtlte:6.0.1/MMB29K/T705DDU1CPL3:user/release-keys");
	}
}