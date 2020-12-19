#!/bin/bash
#
# Copyright (C) 2018-2021 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

set -e

DEVICE=klimtlte
VENDOR=samsung

# Load extract_utils and do some sanity checks
MY_DIR="${BASH_SOURCE%/*}"
if [[ ! -d "${MY_DIR}" ]]; then MY_DIR="${PWD}"; fi

ANDROID_ROOT="${MY_DIR}/../../.."

HELPER="${ANDROID_ROOT}/tools/extract-utils/extract_utils.sh"
if [ ! -f "${HELPER}" ]; then
    echo "Unable to find helper script at ${HELPER}"
    exit 1
fi
source "${HELPER}"

# Default to sanitizing the vendor folder before extraction
CLEAN_VENDOR=true

while [ "${#}" -gt 0 ]; do
    case "${1}" in
        -n | --no-cleanup )
                CLEAN_VENDOR=false
                ;;
        -k | --kang )
                KANG="--kang"
                ;;
        -s | --section )
                SECTION="${2}"; shift
                CLEAN_VENDOR=false
                ;;
        * )
                SRC="${1}"
                ;;
    esac
    shift
done

if [ -z "${SRC}" ]; then
    SRC="adb"
fi

# Initialize the helper
setup_vendor "${DEVICE}" "${VENDOR}" "${ANDROID_ROOT}" false "${CLEAN_VENDOR}"

extract "${MY_DIR}/proprietary-files.txt" "${SRC}" "${KANG}" --section "${SECTION}"

# Fix proprietary blobs
BLOB_ROOT="$ANDROID_ROOT"/vendor/"$VENDOR"/"$DEVICE"/proprietary

# Replace libs to fix missing symbols
"${PATCHELF}" --replace-needed libprotobuf-cpp-full.so libprotobuf-cpp-full-v23.so $BLOB_ROOT/vendor/lib/libsec-ril.so
"${PATCHELF}" --replace-needed libcutils.so libcutils-v29.so $BLOB_ROOT/vendor/lib/libsec-ril.so

# Vendor separation
(perl -pi -e "s/\/system\/bin\/gpsd/\/vendor\/bin\/gpsd/g" $BLOB_ROOT/vendor/lib/libsec-ril.so)
sed -i "s|system/etc|vendor/etc|g" $BLOB_ROOT/vendor/lib/libfloatingfeature.so
sed -i "s|system/etc|vendor/etc|g" $BLOB_ROOT/vendor/lib/libsec-ril.so

# replace SSLv3_client_method with SSLv23_method
sed -i "s/SSLv3_client_method/SSLv23_method\x00\x00\x00\x00\x00\x00/" $BLOB_ROOT/vendor/bin/gpsd

"${MY_DIR}/setup-makefiles.sh"
