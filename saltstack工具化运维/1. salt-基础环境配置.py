###salt安装；
	1.Master安装：
		1.1. 安装依赖和key; 
			sudo yum install https://repo.saltstack.com/py3/redhat/salt-py3-repo-latest-2.el7.noarch.rpm
			sudo yum clean expire-cache
			sudo yum install salt-master
		1.2. 配置文件配置；配置文件在/etc/salt/master
			1.2.1 环境准备；开发、测试、预生产、生产
				file_roots base: /srv/salt/base
				file_roots prod: /srv/salt/prod
				pillar_roots bash: /srv/pillar/base
				pillar_roots prod: /srv/pillar/prod
			1.2.2 操作；
				# 创建相关目录
				mkdir -p /srv/salt/base
				mkdir -p /srv/salt/prod
				mkdir -p /srv/pillar/base
				mkdir -p /srv/pillar/prod
				#修改 /etc/salt/master 配置文件
				vim /etc/salt/master
				interface: 172.20.32.251
				auto_accept: True
				file_roots:
				  base:
					- /srv/salt/base
				  prod:
					- /srv/salt/prod
				pillar_roots:
				  base:
					- /srv/pillar/base
				  prod:
					- /srv/pillar/prod
				nodegroups:
				  CMN-NC-FC: 'L@dev_251,dev_252,dev_253'
				  CMN-JN-FS: 'dev_251'

				#启动服务
				systemctl restart salt-master
				systemctl enable salt-master

	2.Minion安装；
		2.1. 安装依赖和key
			sudo yum install https://repo.saltstack.com/py3/redhat/salt-py3-repo-latest-2.el7.noarch.rpm
			sudo yum clean expire-cache
			sudo yum install salt-minion
		2.2. 配置文件配置；配置文件在/etc/salt/minion
			vim /etc/salt/minion
			master: 172.20.32.251
			id: dev_252
	3. salt操作命令：
		salt-key -L
		salt-key -A
		salt-key -d dev_252
		salt '*' cmd.run 'pwd'
		salt '*' test.ping
		salt -E 'dev_(251|252)' test.ping
		salt -L 'dev_253,dev_252' test.ping
		salt -C '* and not G@os:Ubuntu' test.ping
		#任务管理；
		salt-run jobs.active #查看在执行的任务
		salt 'dev_251' saltutil.kill_all_jobs #删除全部任务
		salt '*' saltutil.kill_job 20210111112835944941 #删除单个任务

		##组；
		salt '*' state.highstate test=True
		salt -N 'CMN-JN-FS' state.highstate test=True
		salt -N 'CMN-JN-FS' state.highstate
	4. Salt base 基础环境规划及配置
		4.1 系统初始化在 base 环境下面配置，以下列出系统初始化要配置的部分：
		init 目录
		DNS 配置
		history 记录时间
		记录命令操作
		内核参数优化
		安装 YUM 仓库
		安装 zabbix-agent
		4.2 目录结构；
		# /srv/salt/base 最终目录结构如下：
		/srv/salt/base/
		├── init
		│   ├── audit.sls
		│   ├── dns.sls
		│   ├── epel.sls
		│   ├── files
		│   │   ├── resolv.conf
		│   │   └── zabbix_agentd.conf
		│   ├── history.sls
		│   ├── init.sls
		│   ├── sysctl.sls
		│   └── zabbix-agent.sls
		└── top.sls
		4.3 操作；
		cd /srv/salt/base && mkdir init
		cd init && mkdir files
		cp -rp /etc/resolv.conf /srv/salt/base/init/files
		#DNS配置；
		vim dns.sls
		/etc/resolv.conf:
		  file.managed:
			- source: salt://init/files/resolv.conf
			- backup: minion
			- user: root
			- group: root
			- mode: 644
		#history 记录时间 
		vim history.sls
		/etc/profile:
		  file.append:
			- text:
			  - export HISTTIMEFORMAT="%F %T `whoami` "
		#记录命令操作；
		vim audit.sls
		/etc/bashrc:
		  file.append:
			- text:
			  - export PROMPT_COMMAND='{ msg=$(history 1 | { read x y; echo $y; });logger "[euid=$(whoami)]":$(who am i):[`pwd`]"$msg"; }'
		#内核参数优化；
		vim sysctl.sls
		net.ipv4.ip_local_port_range:
		  sysctl.present:
			- value: 10000 65000
		fs.file-max:
		  sysctl.present:
			- value: 2000000
		net.ipv4.ip_forward:
		  sysctl.present:
			- value: 1
		vm.swappiness:
		  sysctl.present:
			- value: 0
		#安装yum仓库；
		cat epel.sls
		yum_repo_release:
		  pkg.installed:
			- sources:
			  - epel-release: http://mirrors.aliyun.com/epel/epel-release-latest-7.noarch.rpm
		#安装配置 zabbix-agent;
		##yum.repo
		/etc/yum.repos.d/epel-7.repo:
		  file.managed:
			- source: salt://init/files/epel-7.repo
			- user: root
			- group: root
			- mode: 644

		##zabbix_agent.sls
		vim zabbix-agent.sls
		include:
		  - init.yum-repo
		zabbix-agent:
		  pkg.installed:
			- name: zabbix40-agent
			- require: 
			  - file: /etc/yum.repos.d/epel-7.repo
		  file.managed:
			- name: /etc/zabbix/zabbix_agentd.conf
			- source: salt://init/files/zabbix_agentd.conf
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
			- name: /etc/zabbix/zabbix_agentd.d
			- watch_in:
			  - service: zabbix-agent
			- require:
			  - pkg: zabbix-agent
			  - file: zabbix-agent
			
			#参数配置；
			1.将 zabbix_agentd.conf 放置在 /srv/salt/base/init/files
			cp -rp /etc/zabbix/zabbix_agentd.conf /srv/salt/base/init/files
			cd /srv/salt/base/init/files && wget http://mirrors.aliyun.com/repo/epel-7.repo
			#查看zabbix_agent版本：yum list |grep zabbix-agent
			##配置模板；
			[root@linux-node1 files]# grep ^[a-Z] zabbix_agentd.conf
			PidFile=/run/zabbix/zabbix_agentd.pid
			LogFile=/var/log/zabbix/zabbix_agentd.log
			LogFileSize=0
			Server={{ ZABBIX_SERVER }} 
			Hostname={{ AGENT_HOSTNAME }}
			Include=/etc/zabbix/zabbix_agentd.d/
			
		#配置 init.sls include 以上各个系统初始化模块
		cd /srv/salt/base/init
		vim init.sls
		include:
		  - init.dns
		  - init.history
		  - init.audit
		  - init.sysctl
		  - init.epel
		  - init.zabbix-agent
		#base 环境根目录配置 top file
		cd /srv/salt/base
		vim top.sls
		base:
		  '*':
			- init.init
		#测试并执行状态
		salt -N 'CMN-JN-FS' state.highstate test=True
		salt -N 'CMN-JN-FS' state.highstate







####################################################A&Q
使用 jinja 模板，使用 pillar 设置 Zabbix_Server，使用 grains 设置 Hostname
#操作配置 Zabbix_Server Pillar 的过程
mkdir -p /srv/pillar/base/zabbix
cd /srv/pillar/base/zabbix
#配置 Zabbix_Server 的 pillar  SLS
vim agent.sls
Zabbix_Server: 172.20.32.251

创建 pillar 的 top file
cd /srv/pillar/base/
vim top.sls
base:
  '*':
	- zabbix.agent
	
# 刷新 pillar
salt '*' saltutil.refresh_pillar

# 获取 pillar
salt '*' pillar.items Zabbix_Server