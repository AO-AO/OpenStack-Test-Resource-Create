source /root/openrc

set -x

nova delete `nova list --all-tenant | grep HA |awk -F '|' '{print $2}'`

while [[ `nova list --all-tenant | grep HA | wc -l` != 0 ]];
do
    echo "Waiting for instances soft-deleting"
done

for instance in `nova list --all-tenant --status=SOFT_DELETED | grep HA |awk -F '|' '{print $2}'`
do
  nova force-delete $instance
done

while [[ `nova list --all-tenant --status=SOFT_DELETED | grep HA | wc -l` != 0 ]];
do
    echo "Waiting for instances deleting"
done

while [[ `cinder list --all-tenant| grep instance | grep -e 'available' -e 'error' | wc -l` != 0 ]];
do
  cinder delete `cinder list --all-tenant| grep instance | grep -e 'available' -e 'error' | awk -F '|' '{print $2}'`
done

while [[ `cinder list --all-tenant | grep deleting | grep -v error_deleting | wc -l` != 0 ]];
do
    echo "Waiting for volume deleting"
done

for volume in `cinder list --all-tenant | grep instance |awk -F '|' '{print $2}'`
do
  cinder force-delete $volume
done


set +x
