# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/telephony.mk)

# Inherit from klimtlte device
$(call inherit-product, device/samsung/klimtlte/device.mk)

PRODUCT_BRAND := samsung

# Inherit some common LineageOS stuff.
$(call inherit-product, vendor/cm/config/common_full_tablet_wifionly.mk)

# Inherit more LineageOS stuff.
$(call inherit-product, vendor/cm/config/telephony.mk)

PRODUCT_NAME := lineage_klimtlte
PRODUCT_DEVICE := klimtlte

PRODUCT_BUILD_PROP_OVERRIDES += \
    PRODUCT_MODEL=SM-T705 \
    PRODUCT_NAME=klimtlte \
    PRODUCT_DEVICE=klimtlte \
    PRIVATE_BUILD_DESC="samsung/klimtltexx/klimtlte:6.0.1/MMB29K/T705XXU1CQB1:user/release-keys" \
    TARGET_DEVICE=klimtlte

BUILD_FINGERPRINT := samsung/klimtltexx/klimtlte:6.0.1/MMB29K/T705XXU1CQB1:user/release-keys
