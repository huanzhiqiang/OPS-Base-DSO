####zabbix_agent编排；
##1.目录层级；
[root@local-dev-251 base]# pwd
/srv/salt/base
[root@local-dev-251 base]# tree
.
├── top.sls
├── init
│   ├── files
│   │   └── epel-7.repo
│   └── yum-repo.sls
│── zabbix
│   ├── files
│   │   └── zabbix_agentd.conf
│   └── zabbix-agent.sls
##2. top.sls编排；
#2.1 配置top.sls
base:
  'dev_253':
    - zabbix.zabbix-agent
#2.2 环境初始化；
mkdir /srv/salt/base/zabbix -p
mkdir /srv/salt/base/init/files -p
cd /srv/salt/base/init/files
wget http://mirrors.aliyun.com/repo/epel-7.repo

#2.3 采集配置文件；
yum list |grep zabbix22-agent
yum install zabbix22-agent
mkdir /srv/salt/base/zabbix/files
cp /etc/zabbix_agentd.conf /srv/salt/base/zabbix/files

#2.4 配置zabbix-agent文件模板；
[root@local-dev-251 base]# grep ^[a-Z] zabbix_agentd.conf
PidFile=/run/zabbix/zabbix_agentd.pid
LogFile=/var/log/zabbix/zabbix_agentd.log
LogFileSize=0
Server={{ ZABBIX_SERVER }} 
Hostname={{ AGENT_HOSTNAME }}
Include=/etc/zabbix_agentd.conf.d/

##3 配置epel状态文件管理
cd /srv/salt/base/init
cat yum-repo.sls 
/etc/yum.repos.d/epel-7.repo:
  file.managed:
    - source: salt://init/files/epel-7.repo
    - user: root
    - group: root
    - mode: 644

##4.zabbix-agent.sls编排
cd /srv/salt/base/zabbix
cat zabbix-agent.sls 
include:   #支持include功能
  - init.yum-repo

zabbix-agent:
  pkg.installed:
    - name: zabbix22-agent
    - require: 
      - file: /etc/yum.repos.d/epel-7.repo
  file.managed:
    - name: /etc/zabbix_agentd.conf
    - source: salt://zabbix/files/zabbix_agentd.conf
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - defaults:
      ZABBIX_SERVER: 172.20.32.251
      AGENT_HOSTNAME: {{ grains['fqdn'] }}
    - require:
      - pkg: zabbix-agent
  service.running:
    - name: zabbix-agent
    - enable: True
    - watch:
      - file: zabbix-agent
      - pkg: zabbix-agent

zabbix_agentd.conf.d:
  file.directory:
    - name: /etc/zabbix_agentd.conf.d
    - watch_in:
      - service: zabbix-agent
    - require:
      - pkg: zabbix-agent
      - file: zabbix-agent

##5.执行
salt '*' state.highstate test=True
salt '*' state.highstate

#&&注意事项；
1.Jinja模板变量名不支持中横线 -