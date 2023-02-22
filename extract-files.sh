#!/bin/bash
#
# Copyright (C) 2016 The CyanogenMod Project
# Copyright (C) 2017-2020 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

function blob_fixup() {
    case "${1}" in
        vendor/lib/libsec-ril.so)
            "${PATCHELF}" --replace-needed "libprotobuf-cpp-full.so" "libprotobuf-cpp-haxx.so" "${2}"
            (perl -pi -e "s/\/system\/bin\/gpsd/\/vendor\/bin\/gpsd/g" "${2}")
            ;;
        vendor/lib/libfloatingfeature.so)
            sed -i "s|system/etc|vendor/etc|g" "${2}"
            ;;
        vendor/lib/libsec-ril.so)
            sed -i "s/SSLv3_client_method/SSLv23_method\x00\x00\x00\x00\x00\x00/" "${2}"
            ;;
    esac
}

# If we're being sourced by the common script that we called,
# stop right here. No need to go down the rabbit hole.
if [ "${BASH_SOURCE[0]}" != "${0}" ]; then
    return
fi

set -e

export DEVICE=klimtlte
export DEVICE_COMMON=klimt-common
export VENDOR=samsung

"./../../${VENDOR}/${DEVICE_COMMON}/extract-files.sh" "$@"
