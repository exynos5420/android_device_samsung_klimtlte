/*
 * Copyright (C) 2013 The CyanogenMod Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef _BDROID_BUILDCFG_H
#define _BDROID_BUILDCFG_H

#include <cutils/properties.h>
#include <string.h>

inline const char* BtmGetDefaultName()
{
	char product_name[PROPERTY_VALUE_MAX];
	property_get("ro.product.name", product_name, "");

	if (!strcmp("klimtlteub", product_name))
		return "SM-T705M";
	if (!strcmp("klimtltecan", product_name))
		return "SM-T705W";
	if (!strcmp("klimtltedo", product_name))
		return "SM-T705Y";

	return "SM-T705";
}

#define BTM_DEF_LOCAL_NAME BtmGetDefaultName()

// Networking, Capturing, Object Transfer
// MAJOR CLASS: COMPUTER
// MINOR CLASS: LAPTOP
#define BTA_DM_COD {0x1A, 0x01, 0x0C}

#endif
