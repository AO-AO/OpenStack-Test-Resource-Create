source /root/openrc

set -x

for instance in `nova list --all-tenant | grep HA | grep ACTIVE | awk -F '|' '{print $2}'`
do
    ext_ip=`nova show $instance | grep 'net network' | awk -F '|' '{print $3}'| awk -F ',' '{print $2}'`
    nova floating-ip-disassociate $instance $ext_ip
done

for fip in `neutron floatingip-list --all-tenant | grep '\.' |awk -F '|' '{print $2}'`
do
  neutron floatingip-delete $fip
done


set +x
