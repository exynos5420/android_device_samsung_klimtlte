
products="chagalllte chagallwifi klimtlte klimtwifi"

WDIR=`pwd`

for product in $products; do
  echo "Converting tinyucm.conf and default_gain.conf to mixer_paths.xml for device $product"
  cd ../../$product/audio
  
  echo "In `pwd`"
  ls -al
  
  $WDIR/tinyucm2mixerpaths.py > mixer_paths.xml
  
  echo "  Changes are:"
  git diff mixer_paths.xml
  
  read -p "  Press any key to continue"
  cd $WDIR
done

