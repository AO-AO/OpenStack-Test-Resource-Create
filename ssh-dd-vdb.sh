source /root/openrc


failed_result=""

for ip in `nova list --all-tenant | grep HA |grep CentOS| grep ACTIVE | awk -F '|' '{print $7}' | awk '{print $2}'`
do
  echo "*********read $ip vdb*********"
  ssh -o ConnectTimeout=3 $ip "dd if=/dev/vdb of=/dev/zero bs=4K count=256 iflag=direct"
  if [ $? == 0 ]; then
    echo "*********write $ip vdb*********"
    ssh -o ConnectTimeout=3 $ip "dd if=/dev/zero of=/dev/vdb bs=4K count=256 oflag=direct" 
    
    if [ $? != 0 ]; then
      failed_result=$ip" "$failed_result
    fi
  else
    echo "*********Connect fail*********"
    failed_result=$ip" "$failed_result
  fi
done

if [ x"$failed_result" == "x" ]; then
  failed_result="None"
fi

echo ""
echo "Failed: $failed_result"
echo ""
