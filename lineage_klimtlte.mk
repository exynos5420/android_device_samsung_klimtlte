#
# Copyright (C) 2014-2016 The CyanogenMod Project
# Copyright (C) 2017-2018 The LineageOS Project
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

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Inherit from klimtlte device
$(call inherit-product, device/samsung/klimtlte/device.mk)

# Inherit some common LineageOS stuff.
$(call inherit-product, vendor/lineage/config/common_full_phone.mk)

# Device identifier. This must come after all inclusions
PRODUCT_DEVICE := klimtlte
PRODUCT_NAME := lineage_klimtlte
PRODUCT_BRAND := samsung
PRODUCT_MODEL := SM-T705
PRODUCT_MANUFACTURER := samsung

PRODUCT_GMS_CLIENTID_BASE := android-samsung

PRODUCT_BUILD_PROP_OVERRIDES += \
    PRODUCT_NAME=klimtltexx \
    PRIVATE_BUILD_DESC="klimtltexx-user 6.0.1 MMB29K T705DDS1CRK1 release-keys"

BUILD_FINGERPRINT := samsung/klimtltexx/klimtlte:6.0.1/MMB29K/T705DDS1CRK1:user/release-keys
