#利用Salt-API获取想要的信息；
##1.安装salt-api; 
#采集版本；
rpm -qa |grep salt-master
more /etc/redhat-release 

yum -y install salt-api
rpm -qa |grep  cherry

#安装pyOpenSSL包
yum list |grep -i pyOpenSSL
yum install pyOpenSSL

##2.自签名证书；
#2.1 在salt-master上，打开include功能方便管理
[root@local-dev-251 ~]# egrep -v "^#|^$" /etc/salt/master
default_include: ./master.d/*.conf
...
#签名证书；
[root@local-dev-251 ~]# salt-call --local tls.create_self_signed_cert
local:
    Created Private Key: "/etc/pki/tls/certs/localhost.key." Created Certificate: "/etc/pki/tls/certs/localhost.crt."
	
##3.添加api配置到salt-master配置文件
cd /etc/salt && mkdir master.d
[root@local-dev-251 master.d]# cat api.conf 
rest_cherrypy:
  host: 172.20.32.251
  port: 8000
  ssl_crt: /etc/pki/tls/certs/localhost.crt
  ssl_key: /etc/pki/tls/certs/localhost.key

##4.创建用户 -M不创建家目录 ，并设置密码
useradd -M -s /sbin/nologin saltapi
echo "saltapi" | passwd saltapi --stdin


##5.在salt-master配置文件里添加验证，在include的目录下创建新文件
[root@local-dev-251 master.d]# pwd
/etc/salt/master.d
[root@local-dev-251 master.d]# cat auth.conf 
external_auth:
  pam:
    saltapi:
      - .*
      - '@wheel'
      - '@runner'
      - '@jobs' 

##6.重启salt-master和启动salt-api
systemctl  restart salt-master
systemctl start salt-api

[root@local-dev-251 master.d]# netstat -an|grep 8000
tcp        0      0 127.0.0.1:8000          0.0.0.0:*               LISTEN     
tcp        0      0 172.20.32.251:8000      0.0.0.0:*               LISTEN 

##7.验证login登陆，获取token字符串
[root@local-dev-251 master.d]# curl -sSk https://172.20.32.251:8000/login -H 'Accept: application/x-yaml' -d username='saltapi' -d password='saltapi' -d eauth='pam'
return:
- eauth: pam
  expire: 1628860734.3964713
  perms:
  - .*
  - '@wheel'
  - '@runner'
  - '@jobs'
  start: 1628817534.3964705
  token: 71cece05589c325c7c2ab8a4b92f9ea1a51ddfa6
  user: saltapi

##8.通过api执行test.ping测试连通性
[root@local-dev-251 master.d]# curl -sSk https://172.20.32.251:8000 -H 'Accept: application/x-yaml' -H 'X-Auth-Token: 71cece05589c325c7c2ab8a4b92f9ea1a51ddfa6' -d client=local -d tgt='*' -d fun=test.ping
return:
- dev_251: true
  dev_252: true
  dev_253: true

#9.执行cmd.run
[root@local-dev-251 master.d]# curl -sSk https://172.20.32.251:8000 -H 'Accept: application/x-yaml' -H 'X-Auth-Token: 71cece05589c325c7c2ab8a4b92f9ea1a51ddfa6' -d client=local -d tgt='*' -d fun='cmd.run' -d arg='date'
return:
- dev_251: Fri Aug 13 09:21:46 CST 2021
  dev_252: Fri Aug 13 09:21:46 CST 2021
  dev_253: Fri Aug 13 09:21:46 CST 2021

##10.执行状态模块
[root@local-dev-251 master.d]# curl -sSk https://172.20.32.251:8000 -H 'Accept: application/x-yaml' -H 'X-Auth-Token: 71cece05589c325c7c2ab8a4b92f9ea1a51ddfa6' -d client=local -d tgt='*' -d fun='state.highstate'
return:
- dev_251:
    no_|-states_|-states_|-None:
      __run_num__: 0
      changes: {}
      comment: No Top file or master_tops data matches found. Please see master log
        for details.
      name: No States
      result: false
  dev_252:
    no_|-states_|-states_|-None:
      __run_num__: 0
      changes: {}
      comment: No Top file or master_tops data matches found. Please see master log
        for details.
      name: No States
      result: false
  dev_253:
    file_|-/etc/hosts_|-/etc/hosts_|-managed:
      __id__: /etc/hosts
      __run_num__: 1
      __sls__: graints.dns
      changes: {}
      comment: File /etc/hosts is in the correct state
      duration: 24.01
      name: /etc/hosts
      result: true
      start_time: '09:23:44.559919'
    file_|-/etc/resolv.conf_|-/etc/resolv.conf_|-managed:
      __id__: /etc/resolv.conf
      __run_num__: 0
      __sls__: graints.dns
      changes: {}
      comment: File /etc/resolv.conf is in the correct state
      duration: 63.767
      name: /etc/resolv.conf
      result: true
      start_time: '09:23:44.495976'

##11.以json格式输出
[root@local-dev-252 ~]# curl -sSk https://172.20.32.251:8000 -H 'Accept: application/json' -H 'X-Auth-Token: 71cece05589c325c7c2ab8a4b92f9ea1a51ddfa6' -d client=local -d tgt='*' -d fun='cmd.run' -d arg='w'
{"return": [{"dev_251": " 09:25:23 up 51 min,  2 users,  load average: 0.02, 0.04, 0.05\nUSER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT\nroot     pts/0    172.20.32.56     08:49    1:47   0.44s  0.44s -bash\nroot     pts/1    172.20.32.56     09:24   40.00s  0.08s  0.08s -bash", "dev_252": " 09:25:23 up 51 min,  1 user,  load average: 0.02, 0.02, 0.05\nUSER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT\nroot     pts/0    172.20.32.56     08:49    3.00s  0.35s  0.12s curl -sSk https://172.20.32.251:8000 -H Accept: application/json -H X-Auth-Token: 71cece05589c325c7c2ab8a4b92f9ea1a51ddfa6 -d client=local -d tgt=* -d fun=cmd.run -d arg=w", "dev_253": " 09:25:23 up  1:23,  0 users,  load average: 0.01, 0.01, 0.00\nUSER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT"}]}

##12.获取grains信息
[root@local-dev-251 ~]# curl -sSk https://172.20.32.251:8000/minions/dev_253 -H 'Accept: application/x-yaml' -H 'X-Auth-Token: 71cece05589c325c7c2ab8a4b92f9ea1a51ddfa6'
return:
- dev_253:
    biosreleasedate: 06/24/2014
    biosversion: 2.8.0
    cpu_flags:
    - fpu
    - vme
    - de
    - pse
    - tsc
    - msr
    - pae
    - mce
    - cx8
    - apic
    - sep
    - mtrr
    - pge
    - mca
    - cmov
    - pat
    - pse36
    - clflush
    - dts
    - acpi
    - mmx
    - fxsr
    - sse
    - sse2
    - ss
    - ht
    - tm
    - pbe
    - syscall
    - nx
    - rdtscp
    - lm
    - constant_tsc
    - arch_perfmon
    - pebs
    - bts
    - rep_good
    - nopl
    - xtopology
    - nonstop_tsc
    - cpuid
    - aperfmperf
    - pni
    - pclmulqdq
    - dtes64
    - monitor
    - ds_cpl
    - vmx
    - smx
    - est
    - tm2
    - ssse3
    - cx16
    - xtpr
    - pdcm
    - pcid
    - sse4_1
    - sse4_2
    - x2apic
    - popcnt
    - tsc_deadline_timer
    - aes
    - xsave
    - avx
    - f16c
    - rdrand
    - lahf_lm
    - cpuid_fault
    - epb
    - pti
    - ssbd
    - ibrs
    - ibpb
    - stibp
    - tpr_shadow
    - vnmi
    - flexpriority
    - ept
    - vpid
    - fsgsbase
    - smep
    - erms
    - xsaveopt
    - dtherm
    - ida
    - arat
    - pln
    - pts
    - flush_l1d
    cpu_model: Intel(R) Xeon(R) CPU E3-1220 V2 @ 3.10GHz
    cpuarch: x86_64
    cwd: /
    disks:
    - sr0
    - sda
    dns:
      domain: ''
      ip4_nameservers:
      - 114.114.114.114
      ip6_nameservers: []
      nameservers:
      - 114.114.114.114
      options: []
      search: []
      sortlist: []
    domain: ''
    fqdn: local-dev-253
    fqdn_ip4:
    - 172.20.32.253
    fqdn_ip6: []
    fqdns:
    - linux-dev253.example.com
    gid: 0
    gpus:
    - model: MGA G200eW WPCM450
      vendor: matrox
    groupname: root
    host: local-dev-253
    hwaddr_interfaces:
      em1: 20:47:47:99:6c:b0
      lo: 00:00:00:00:00:00
    id: dev_253
    init: systemd
    ip4_gw: 172.20.32.1
    ip4_interfaces:
      em1:
      - 172.20.32.253
      lo:
      - 127.0.0.1
    ip6_gw: false
    ip6_interfaces:
      em1: []
      lo: []
    ip_gw: true
    ip_interfaces:
      em1:
      - 172.20.32.253
      lo:
      - 127.0.0.1
    ipv4:
    - 127.0.0.1
    - 172.16.200.1
    - 172.17.0.1
    - 172.20.32.253
    ipv6: []
    kernel: Linux
    kernelparams:
    - - BOOT_IMAGE
      - /vmlinuz-4.14.35-1902.2.0.el7uek.x86_64
    - - root
      - /dev/mapper/centos-root
    - - ro
      - null
    - - crashkernel
      - auto
    - - rd.lvm.lv
      - centos/root
    - - rd.lvm.lv
      - centos/swap
    - - rhgb
      - null
    - - quiet
      - null
    - - numa
      - 'off'
    - - transparent_hugepage
      - never
    kernelrelease: 4.14.35-1902.2.0.el7uek.x86_64
    kernelversion: '#2 SMP Fri Jun 14 21:15:44 PDT 2019'
    locale_info:
      defaultencoding: UTF-8
      defaultlanguage: en_US
      detectedencoding: UTF-8
      timezone: unknown
    localhost: local-dev-253
    lsb_distrib_codename: CentOS Linux 7 (Core)
    lsb_distrib_id: CentOS Linux
    lvm:
      centos:
      - home
      - root
      - swap
    machine_id: 8e5311c95148414086c1a4a2fe4c2511
    manufacturer: Dell Inc.
    master: 172.20.32.251
    mdadm: []
    mem_total: 15806
    nodename: local-dev-253
    num_cpus: 4
    num_gpus: 1
    os: CentOS
    os_family: RedHat
    osarch: x86_64
    oscodename: CentOS Linux 7 (Core)
    osfinger: CentOS Linux-7
    osfullname: CentOS Linux
    osmajorrelease: 7
    osrelease: 7.6.1810
    osrelease_info:
    - 7
    - 6
    - 1810
    path: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin
    pid: 4480
    productname: PowerEdge T110 II
    ps: ps -efHww
    pythonexecutable: /usr/bin/python3
    pythonpath:
    - /usr/bin
    - /usr/lib64/python36.zip
    - /usr/lib64/python3.6
    - /usr/lib64/python3.6/lib-dynload
    - /usr/lib64/python3.6/site-packages
    - /usr/lib/python3.6/site-packages
    pythonversion:
    - 3
    - 6
    - 8
    - final
    - 0
    saltpath: /usr/lib/python3.6/site-packages/salt
    saltversion: '3003.1'
    saltversioninfo:
    - 3003
    - 1
    selinux:
      enabled: false
      enforced: Disabled
    serialnumber: 8YR0BC2
    server_id: 623953176
    shell: /bin/sh
    ssds: []
    swap_total: 0
    systemd:
      features: +PAM +AUDIT +SELINUX +IMA -APPARMOR +SMACK +SYSVINIT +UTMP +LIBCRYPTSETUP
        +GCRYPT +GNUTLS +ACL +XZ +LZ4 -SECCOMP +BLKID +ELFUTILS +KMOD +IDN
      version: '219'
    systempath:
    - /usr/local/sbin
    - /usr/local/bin
    - /usr/sbin
    - /usr/bin
    uid: 0
    username: root
    uuid: 4c4c4544-0059-5210-8030-b8c04f424332
    virtual: physical
    zfs_feature_flags: false
    zfs_support: false
    zmqversion: 4.1.4

##使用job; 
salt-run jobs.active #获取job串码；
curl -k -s https://172.20.32.251:8000/jobs/“JOB_ID” -H "Accept: application/x-yaml" -H "X-Auth-Token: 71cece05589c325c7c2ab8a4b92f9ea1a51ddfa6" 



