source /root/openrc

set -x

for volume in `cinder list --all-tenant | grep HA | awk -F '|' '{print $2}'`
do
  instance=`cinder list --all-tenant| grep $volume | awk -F '|' '{print $9}'`
  nova volume-detach $instance $volume
done

while [[ `cinder list --all-tenant | grep HA| grep -v 'in-use' | wc -l` != 2 ]]
do
    cinder delete `cinder list --all-tenant| grep HA |grep 'node'| grep available | awk -F '|' '{print $2}'`
done

set +x
