###salt模块练习；
#1.cmd.run模块
salt '*' cmd.run 'w'

#2.network模块
salt -S '172.20.32.251' network.active_tcp
salt '*' network.arp
salt -S '172.20.32.251' network.connect www.baidu.com 80

salt '*' network.dig www.baidu.com
salt '*' network.get_hostname
salt '*' network.hw_addr eth0
salt '*' network.interface eth0
salt '*' network.interface_ip eth0
salt '*' network.is_loopback 127.0.0.1
salt '*' network.netstat

salt '*' network.ping www.baidu.com
salt '*' network.ping archlinux.org timeout=3

#3.service模块
salt '*' service.get_all
salt '*' service.available sshd
salt '*' service.reload httpd
salt '*' service.status httpd

#4.执行模块state
salt '*' state.apply
salt 'dev_*' state.show_top #查看minion的top.sls配置；
salt 'dev_251' state.single pkg.installed name=vim-enhanced #单独执行pkg模块，执行模块直接就执行 ，状态模块先检查

#5.salt-run
salt-run manage.status #mange检查节点状态
salt-run manage.versions #mange检查minion版本

salt "*" state.highstate test=True #安全执行测试 test=True，没有问题在应用到服务器
salt-cp   'dev_253' /etc/rc.local  /mnt/ #salt-cp拷贝文件