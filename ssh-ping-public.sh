source /root/openrc

admin_centos_ip=`nova list --all-tenant | grep 'admin_admin_node-1' | grep CentOS | grep Init | awk -F '|' '{print $7}' | awk -F ',' '{print $2}'`


echo "--------------------PING PUBLIC----------------------"
failed_result=""

for ip in `nova list --all-tenant | grep HA | grep ACTIVE | awk -F '|' '{print $7}' | awk '{print $2}'`
do
  name=`nova list --all-tenant | grep $ip | awk -F '|' '{print $3}'`
  echo "Ping instance $name with ip $ip"
  #ssh -o ConnectTimeout=3 $admin_centos_ip "ping -c 2 $ip"
  ping -c 2 $ip
  
  if [ $? != 0 ]; then
    failed_result=$ip" "$failed_result
  fi

  echo "******************************"
done

if [ x"$failed_result" == "x" ]; then
  failed_result="None"
fi

echo ""
echo "Failed: "$failed_result
echo ""

