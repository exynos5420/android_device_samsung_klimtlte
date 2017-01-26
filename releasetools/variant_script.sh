#!/sbin/sh

set -e

modelid=`getprop ro.bootloader`

case $modelid in
	T705Y)		variant="do" ;;
	T705M)		variant="ub" ;;
	T705W)		variant="can" ;;
	*)		variant="lte" ;;
esac

basedir="/system/blobs/$variant/"
cd $basedir
chmod 755 bin/*
find . -type f | while read file; do ln -s $basedir$file /system/$file ; done