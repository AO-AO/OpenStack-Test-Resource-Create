source /root/openrc

set -x

for router in `neutron router-list --all-tenant | grep router | awk -F '|' '{print $2}'`;
do
  subnet=`neutron router-port-list $router | grep subnet_id | awk -F ':' '{print $7}' | awk -F ',' '{print $1}' |awk -F '"' '{print $2}'`
  for subnet_id in $subnet;
  do
    neutron subnet-list | grep $subnet_id | grep rec
    if [ $? == 0 ]; then
      neutron router-interface-delete $router $subnet_id
      break
    fi
  done
done

for subnet in `neutron subnet-list --all-tenant | grep -v ext | grep rec | grep start | awk -F '|' '{print $2}'`
do
  neutron subnet-delete $subnet
done

for net in `neutron net-list --all-tenant | grep -v ext | grep rec | awk -F '|' '{print $2}'`
do
  neutron net-delete $net
done

set +x
