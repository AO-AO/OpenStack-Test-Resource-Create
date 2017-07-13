source /root/openrc

set -x
for router in `neutron router-list --all-tenant | grep router | awk -F '|' '{print $2}'`;
do
  neutron router-gateway-clear $router net_external
  subnet=`neutron router-port-list $router | grep subnet_id | awk -F ':' '{print $7}' | awk -F ',' '{print $1}' |awk -F '"' '{print $2}'`
  neutron router-interface-delete $router $subnet
  neutron router-delete $router
done

for subnet in `neutron subnet-list --all-tenant | grep -v ext | grep start | awk -F '|' '{print $2}'`
do
  neutron subnet-delete $subnet
done

for net in `neutron net-list --all-tenant | grep -v ext  |awk -F '|' '{print $2}'`
do
  neutron net-delete $net
done

set +x
