source /root/openrc
win_path='/root/img/windows7_x64_hasvs.qcow2'
lin_path='/root/img/Centos6.5_zabbix.qcow2'

echo "Uploading images"


glance image-create --name 'Windows-HA' --is-public true --container-format=bare --disk-format=qcow2 --min-ram=1024 --property architecture=x86_64 --property os_distro=Windows --property os_version=Win7 --property vol_size=100 --file $win_path &

glance image-create --progress --name 'CentOS-HA' --is-public true --container-format=bare --disk-format=qcow2 --min-ram=1024 --property architecture=x86_64 --property os_distro=CentOS --property os_version=6.5 --property vol_size=100 --file $lin_path &

while [[ `glance image-list | grep 'active' | grep -c 'Windows-HA \| CentOS-HA'` != 2 ]];
do 
    echo "Waiting for images uploading"
    sleep 10
done

set -x
win_id=`glance image-list | grep "Windows-HA" | awk -F '|' '{print $2}'`
cen_id=`glance image-list | grep "CentOS-HA" | awk -F '|' '{print $2}'`
   
echo "Creating image-volumes"
cinder create --image-id $win_id --display-name "Windows-HA" 100 --metadata awcloud_public_image=yes
cinder create --image-id $cen_id --display-name "CentOS-HA" 100 --metadata awcloud_public_image=yes

    while [[ `cinder list | grep 'available' | grep -c 'Windows-HA \| CentOS-HA'` != 2 ]];
    do
        echo "Waiting for image-volumes creating"
        sleep 10
    done

echo "Finished!"

set +x
