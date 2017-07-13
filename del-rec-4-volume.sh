source /root/openrc

set -x

for volume in `cinder list --all-tenant | grep HA| grep rec | awk -F '|' '{print $2}'`
do
  instance=`cinder list --all-tenant| grep $volume | awk -F '|' '{print $9}'`
  nova volume-detach $instance $volume
done

while [[ `cinder list --all-tenant | grep HA|grep rec | grep -v 'in-use' | wc -l` != 0 ]]
do
    cinder delete `cinder list --all-tenant| grep HA |grep 'node'|grep rec| grep available | awk -F '|' '{print $2}'`
done

set +x
