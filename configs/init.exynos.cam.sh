#!/system/bin/sh

"init.exynos.cam.sh: start" > /dev/kmsg

file="/data/CameraID.txt"
if [ -f "$file" ]
then
    echo "init.exynos.cam.sh: $file exists" > /dev/kmsg
else
    echo "init.exynos.cam.sh: $file does not exist, creating" > /dev/kmsg
    touch "$file"
fi
chown media:audio "$file"
chmod 600 "$file"

file="/data/cal_data.bin"
if [ -f "$file" ]
then
    echo "init.exynos.cam.sh: $file exists" > /dev/kmsg
else
    echo "init.exynos.cam.sh: $file does not exist, creating" > /dev/kmsg
    touch "$file"
fi
chown media:audio "$file"
chmod 600 "$file"

mkdir -p /data/camera
