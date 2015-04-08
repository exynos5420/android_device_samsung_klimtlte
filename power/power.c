/*
 * Copyright (C) 2014, The CyanogenMod Project <http://www.cyanogenmod.org>
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
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#define LOG_TAG "KlimtWifiPowerHAL"
#include <utils/Log.h>

#include <hardware/hardware.h>
#include <hardware/power.h>

#define TSP_POWER "/sys/class/input/input1/enabled"
#define TOUCHKEY_POWER "/sys/class/input/input8/enabled"
#define INPUT_POWER7 "/sys/class/input/input7/enabled"
#define INPUT_POWER6 "/sys/class/input/input6/enabled"
#define INPUT_POWER5 "/sys/class/input/input5/enabled"
#define INPUT_POWER4 "/sys/class/input/input4/enabled"
#define INPUT_POWER3 "/sys/class/input/input3/enabled"
#define INPUT_POWER2 "/sys/class/input/input2/enabled"

static void sysfs_write(char *path, char *s) {
    char buf[80];
    int len;
    int fd = open(path, O_WRONLY);

    if (fd < 0) {
        strerror_r(errno, buf, sizeof(buf));
        ALOGE("Error opening %s: %s\n", path, buf);
        return;
    }

    len = write(fd, s, strlen(s));
    if (len < 0) {
        strerror_r(errno, buf, sizeof(buf));
        ALOGE("Error writing to %s: %s\n", path, buf);
    }

    close(fd);
}

static void power_init(struct power_module *module)
{
}

static void power_set_interactive(struct power_module *module, int on)
{
    ALOGD("%s: %s input devices", __func__, on ? "enabling" : "disabling");
    sysfs_write(TSP_POWER, on ? "1" : "0");
    sysfs_write(TOUCHKEY_POWER, on ? "1" : "0");
    sysfs_write(INPUT_POWER2, on ? "1" : "0");
    sysfs_write(INPUT_POWER3, on ? "1" : "0");
    sysfs_write(INPUT_POWER4, on ? "1" : "0");
    sysfs_write(INPUT_POWER5, on ? "1" : "0");
    sysfs_write(INPUT_POWER6, on ? "1" : "0");
    sysfs_write(INPUT_POWER7, on ? "1" : "0");
}

static void power_hint(struct power_module *module, power_hint_t hint,
                       void *data) {
    switch (hint) {
    default:
        break;
    }
}

static struct hw_module_methods_t power_module_methods = {
    .open = NULL,
};

struct power_module HAL_MODULE_INFO_SYM = {
    .common = {
        .tag = HARDWARE_MODULE_TAG,
        .module_api_version = POWER_MODULE_API_VERSION_0_2,
        .hal_api_version = HARDWARE_HAL_API_VERSION,
        .id = POWER_HARDWARE_MODULE_ID,
        .name = "klimtwifi Power HAL",
        .author = "The CyanogenMod Project",
        .methods = &power_module_methods,
    },

    .init = power_init,
    .setInteractive = power_set_interactive,
    .powerHint = power_hint,
};
