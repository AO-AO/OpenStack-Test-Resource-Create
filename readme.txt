1.在WEB页面提前预置好 域·VDC·用户，结构如下图：
        -- default -- admin -- admin
        |- dom0 -- vdc00 -- admin000
        |        |        |- user001
        |        |
        |        |-vdc01 -- user010
        |
        |- dom1 -- vdc10 -- admin100

2.配置vdc 的配额（虚拟机数量：40，CPU：60，内存：51200，磁盘个数：100，磁盘大小：10000）

3.配置所有的default 安全组，新建icmp 规则用于ping，新建ssh 规则用于 ssh。

4.配置config.py 文件
（1）根据keystone endpoint-list -- publicURL 配置manage_ip
（2）云管界面 -- 用户管理 -- VDC 查看VDC_ID，填入project_*_id
（3）云管界面 -- 用户管理 -- 用户 查看用户ID，并将对应密码填入user_*_id, user_*_pa

5.配置0-upload-img.sh 文件，上传镜像：
（1）将Windows 镜像路径填入win_path
（2）将Linux 镜像路径填入lin_path
（3）执行0-upload-img.sh，上传镜像

6.关于脚本执行顺序
（1）数字1-4开头的脚本用于初始化资源，1-* ---> 4-*
（2）英文del开头的脚本用于资源清理，del-4-* ---> del-1-*
（3）英文rec开头的为故障恢复后的测试创建删除脚本
（4）ssh-* 脚本为测试ping脚本和测试dd脚本
