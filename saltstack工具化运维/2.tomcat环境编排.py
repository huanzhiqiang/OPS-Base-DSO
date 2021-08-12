####tomcat编排；
#1.目录层级；
[root@local-dev-251 base]# pwd
/srv/salt/base
|—— top.sls
├── tomcat
│   ├── files
│   │   ├── apache-tomcat-8.5.49.tar.gz
│   │   └── jdk-8u201-linux-x64.tar.gz
│   ├── jdk.sls
│   └── tomcat.sls
#2. top.sls编排；
base:
  'dev_253':
    - tomcat.tomcat

#3.jdk.sls编排；
j-install:
  file.managed:
    - name: /usr/local/share/jdk-8u201-linux-x64.tar.gz
    - source: salt://tomcat/files/jdk-8u201-linux-x64.tar.gz
    - user: root
    - group: root
    - mode: 644
  cmd.run:
    - name: cd /usr/local/share && tar -xf jdk-8u201-linux-x64.tar.gz && ln -s /usr/local/share/jdk1.8.0_201 /usr/local/jdk && sed -i.ori '$a \#jdk_env\nexport JAVA_HOME=/usr/local/jdk\nexport PATH=$JAVA_HOME/bin:$JAVA_HOME/jre/bin:$PATH\nexport CLASSPATH=.$CLASSPATH:$JAVA_HOME/lib:$JAVA_HOME/jre/lib:$JAVA_HOME/lib/tools.jar' /etc/profile && source /etc/profile

#4.tomcat.sls编排
include:
  - tomcat.jdk

tomcat-install:
  file.managed:
    - name: /usr/local/src/apache-tomcat-8.5.49.tar.gz
    - source: salt://tomcat/files/apache-tomcat-8.5.49.tar.gz
    - user: root
    - group: root
    - mode: 644
  cmd.run:
    - name: cd /usr/local/src && tar zxf apache-tomcat-8.5.49.tar.gz && mv apache-tomcat-8.5.49 /usr/local/ && ln -s /usr/local/apache-tomcat-8.5.49 /usr/local/tomcat
    - unless: test -L /usr/local/tomcat && test -d /usr/local/apache-tomcat-8.5.49

#5.执行
salt '*' state.highstate test=True
salt '*' state.highstate