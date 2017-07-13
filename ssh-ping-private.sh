source /root/openrc

admin_centos_ip=`nova list --all-tenant | grep 'admin_admin' | grep CentOS |grep ',' |awk -F '|' '{print $7}' | awk -F ',' '{print $2}' | head -n 1`
vdc00_centos_ip=`nova list --all-tenant | grep 'vdc00' | grep CentOS |grep ',' |awk -F '|' '{print $7}' | awk -F ',' '{print $2}' | head -n 1`
vdc01_centos_ip=`nova list --all-tenant | grep 'vdc01' | grep CentOS |grep ',' |awk -F '|' '{print $7}' | awk -F ',' '{print $2}' | head -n 1`
vdc10_centos_ip=`nova list --all-tenant | grep 'vdc10' | grep CentOS |grep ',' |awk -F '|' '{print $7}' | awk -F ',' '{print $2}' | head -n 1`
echo "ADMIN $admin_centos_ip"
echo "VDC00 $vdc00_centos_ip"
echo "VDC01 $vdc01_centos_ip"
echo "VDC10 $vdc10_centos_ip"

admin_failed_result=""
vdc00_failed_result=""
vdc01_failed_result=""
vdc10_failed_result=""

echo "----------------------------PRIVATE---------------------------------"

for private_ip in `nova list --all-tenant | grep HA |grep 'admin_'| grep ACTIVE | awk -F '|' '{print $7}' | awk -F ',' '{print $1}' |awk -F '=' '{print $2}'`
do
  name=`nova list --all-tenant | grep $private_ip | awk -F '|' '{print $3}'`
  echo "ADMIN Ping instance with ip $private_ip"
  ssh -o ConnectTimeout=3 $admin_centos_ip "ping -c 2 $private_ip"
  
  if [ $? != 0 ]; then
    admin_failed_result=$private_ip" "$admin_failed_result
  fi

  echo "**************************************"
done

for private_ip in `nova list --all-tenant | grep HA |grep 'vdc00'| grep ACTIVE | awk -F '|' '{print $7}' | awk -F ',' '{print $1}' |awk -F '=' '{print $2}'`

do
  name=`nova list --all-tenant | grep $private_ip | awk -F '|' '{print $3}'`
  echo "VDC00 Ping instance with ip $private_ip"
  ssh -o ConnectTimeout=3 $vdc00_centos_ip "ping -c 2 $private_ip"
  
  if [ $? != 0 ]; then
    vdc00_failed_result=$private_ip" "$vdc00_failed_result
  fi

  echo "**************************************"
done

for private_ip in `nova list --all-tenant | grep HA |grep 'vdc01'| grep ACTIVE | awk -F '|' '{print $7}' | awk -F ',' '{print $1}' |awk -F '=' '{print $2}'`
do
  name=`nova list --all-tenant | grep $private_ip | awk -F '|' '{print $3}'`
  echo "VDC01 Ping instance with ip $private_ip"
  ssh -o ConnectTimeout=3 $vdc01_centos_ip "ping -c 2 $private_ip"
  
  if [ $? != 0 ]; then
    vdc01_failed_result=$private_ip" "$vdc01_failed_result
  fi

  echo "**************************************"
done

for private_ip in `nova list --all-tenant | grep HA |grep 'vdc10'| grep ACTIVE | awk -F '|' '{print $7}' | awk -F ',' '{print $1}' |awk -F '=' '{print $2}'`
do
  name=`nova list --all-tenant | grep $private_ip | awk -F '|' '{print $3}'`
  echo "VDC10 Ping instance with ip $private_ip"
  ssh -o ConnectTimeout=3 $vdc10_centos_ip "ping -c 2 $private_ip"
  
  if [ $? != 0 ]; then
    vdc10_failed_result=$private_ip" "$vdc10_failed_result
  fi

  echo "**************************************"
done

if [ x"$admin_failed_result" == "x" ]; then
  admin_failed_result="None"
fi

if [ x"$vdc00_failed_result" == "x" ]; then
  vdc00_failed_result="None"
fi

if [ x"$vdc01_failed_result" == "x" ]; then
  vdc01_failed_result="None"
fi

if [ x"$vdc10_failed_result" == "x" ]; then
  vdc10_failed_result="None"
fi

echo ""
echo "admin Failed: "$admin_failed_result
echo "vdc00 Failed: "$vdc00_failed_result
echo "vdc01 Failed: "$vdc01_failed_result
echo "vdc10 Failed: "$vdc10_failed_result
echo ""



