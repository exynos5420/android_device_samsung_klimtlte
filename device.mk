#
# Copyright (C) 2018 The LineageOS Project
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

# Ramdisk
PRODUCT_PACKAGES += \
    init.baseband.rc \
    init.target.rc

# Radio
PRODUCT_PACKAGES += \
    libprotobuf-cpp-full \
    libxml2 \
    rild \
    libril \
    libreference-ril \
    android.hardware.radio@1.0 \
    android.hardware.radio.deprecated@1.0

PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/configs/init/rild.rc:$(TARGET_COPY_OUT_VENDOR)/etc/init/rild.legacy.rc

# System properties
-include $(LOCAL_PATH)/system_prop.mk

# Inherit from klimt-common
$(call inherit-product, device/samsung/klimt-common/device-common.mk)

# call the proprietary setup
$(call inherit-product-if-exists, vendor/samsung/klimtlte/klimtlte-vendor.mk)
