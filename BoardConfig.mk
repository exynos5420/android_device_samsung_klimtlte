#
# Copyright (C) 2013 The CyanogenMod Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

LOCAL_PATH := device/samsung/klimtlte

# Platform
BOARD_VENDOR := samsung
TARGET_SOC := exynos5420

# RIL
BOARD_PROVIDES_LIBRIL := true
# hardware/samsung/ril
BOARD_MODEM_TYPE := xmm7260
# RIL.java overwrite
BOARD_RIL_CLASS := ../../../$(LOCAL_PATH)/ril
BOARD_MODEM_NEEDS_VIDEO_CALL_FIELD := true

# Bluetooth
BOARD_BLUETOOTH_BDROID_BUILDCFG_INCLUDE_DIR := $(LOCAL_PATH)/bluetooth

# Bootloader
TARGET_OTA_ASSERT_DEVICE := klimtlte

# Kernel
TARGET_KERNEL_CONFIG := cyanogenmod_deathly_klimtlte_defconfig

# Include path
TARGET_SPECIFIC_HEADER_PATH := $(LOCAL_PATH)/include

# Cyanogen Hardware
BOARD_HARDWARE_CLASS := $(LOCAL_PATH)/cmhw

# Partitions
BOARD_SYSTEMIMAGE_PARTITION_SIZE := 2506096640
BOARD_USERDATAIMAGE_PARTITION_SIZE := 12629049344
BOARD_CACHEIMAGE_PARTITION_SIZE := 209715200

# SELinux
BOARD_SEPOLICY_DIRS += \
    device/samsung/klimtlte/sepolicy

# Inherit from exynos5420-common
include device/samsung/exynos5420-common/BoardConfigCommon.mk
