##grains jinja模板编排；
##1.目录结构
[root@local-dev-251 base]# pwd
/srv/salt/base
├── graints
│   ├── dns.sls
│   ├── files
│   │   ├── hosts
│   │   └── resolv.conf
│   └── init.sls
├── top.sls

##2.grains 操作；
[root@local-dev-251 base]# salt 'dev_253' grains.item fqdn_ip4
dev_253:
    ----------
    fqdn_ip4:
        - 172.20.32.253

salt 'dev_253' grains.items
salt 'dev_253' grains.ls
#获取内存；
salt 'dev_253' grains.item mem_total

##3.top.sls编排；
#cat top.sls
base:
  'dev_253':
    - graints.init

##3.init.sls编排；
#cat init.sls
include:
  - graints.dns

##4.dns.sls编排；
[root@local-dev-251 graints]# cat dns.sls 
/etc/resolv.conf:
  file.managed:
    - source: salt://graints/files/resolv.conf
    - backup: minion
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - defaults:
      DNS: 114.114.114.114

/etc/hosts:
  file.managed:
    - source: salt://graints/files/hosts
    - backup: minion
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - defaults:
      IPADDR: {{ grains [ 'fqdn_ip4'][0] }}

##5. 模板文件；
[root@local-dev-251 files]# cat hosts 
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
####Key position
172.20.32.252 local-dev-252 linux-dev252.example.com
{{ IPADDR }} local-dev-253 linux-dev253.example.com
172.20.32.251 local-dev-251 linux-dev251.example.com
[root@local-dev-251 files]# cat resolv.conf 
# Generated by NetworkManager
###Key2position
nameserver {{ DNS }}

##6.执行；
salt '*' state.highstate test=True
salt '*' state.highstate