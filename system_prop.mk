#
# system.prop for klimtlte
#

# UI
PRODUCT_PROPERTY_OVERRIDES += \
    ro.sf.lcd_density=320

# Radio
PRODUCT_PROPERTY_OVERRIDES += \
    rild.libpath=/system/lib/libsec-ril.so \
    rild.libargs=-d /dev/ttyS0 \
    ro.telephony.default_network=9 \
    ro.telephony.ril_class=SlteRIL \
    ro.ril.telephony.mqanelements=5 \

# Randomly from stock
PRODUCT_PROPERTY_OVERRIDES += \
    ro.ril.gprsclass=10 \
    ro.ril.hsxpa=1 \
    ro.sec.fle.encryption=true \
    ro.secwvk=220
