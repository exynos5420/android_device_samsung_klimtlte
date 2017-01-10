#!/bin/sh
#
# applypatch.sh
# apply patches
#


dir=`cd $(dirname $0) && pwd`
top=$dir/../../../..

echo "*** Patching ***"
for patch in `ls $dir/*.patch` ; do
    echo ""
    echo "==> patch file: ${patch##*/}"
    patch -p1 -N -i $patch -r - -d $top
done

find . -name "*.orig" -delete