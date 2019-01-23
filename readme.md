# python自动化学习

# ubuntu_automatic_install_php.py
使用python自动化脚本安装php环境（限ubuntu环境）

# ansible
## 安装卸载方式
### pip安装：
* pip install ansible

pip查找：
* pip list|grep ansible

pip卸载：
* pip uninstall ansible

### mac安装
* brew instsall ansible


### 源码安装：
centos
* yum install ansible

ubuntu
* apt-get install software-proerties-common
* apt-add-repository ppa:ansible/ansible
* apt-get update
* apt-get install ansible

## 运行方式
ansible->ssh->ssh->shell

## ansible配置文件路径排序（优先级，高的在前）
* export ANSIBLE_CONFIG
* ./ansible.cfg (当前目录下的)
* ~/.ansible.cfg (根目录下的)
* /etc/ansible/ansible.cfg (系统安装路径下)


## 配置项
* ask_pass && ask_sudo_pass

ask_pass可以控制Ansible剧本playbook是否会自动默认弹出密码

ask_sudo_pass用户使用的系统平台开起来了sudo密码的化应该设置该参为true

* gather_subst

设置收集的内容包括：all，network，hardware，virtual(虚拟环境)，facter,ohai

* remote_port && remote_tmp && remote_user

客户机的设置，分别对登陆的端口，临时目录及其用户

* sudo_exe && sudo_flags && sudo_user

sudo命令相关设置，sudo命令的路径，sudo参数，能够使用sudo的user

* 插件

    * action_plugins 激活事件
    * callback_plugins 回调
    * connection_plugins 连接
    * filter_plugins 过滤器
    * lookup_plugins 加载路径
    * vars_plugins 任何地方加载
    
* forks

最大开辟的进程数，这个进程数不宜过大，过大耗费性能，不宜过小，过小并发性能低，一般是cpu数*2

* vault_password_file

代填密码（确保可执行）

* pattern

如果没有配置"hosts"节点，这时playbook默认通知所有主机（很可怕），最好设置单个选项

* inventory & library

分别为存放可通信主机的目录和ansible默认搜索模块的路径（不要改）


# 操作
* sudo ln -s /Library/Frameworks/Python.framework/Versions/3.7/bin/ansible /usr/local/bin

* ansible --version


# 新建机器
* 本机创建/etc/ansible/hosts文件，将目标服务器ip放置到这个文件中
* 将本机公钥放置到目标服务器authorized_keys中，（ssh-copy-id root@目标服务器ip）
* 测试连通 ansible all -m ping
  一般是过不了，因为默认用的是本机的用户名称
失败事例(ansible all -m ping)
```
94.191.29.229 | UNREACHABLE! => {
    "changed": false,
    "msg": "Failed to connect to the host via ssh: caicheng@94.191.29.229: Permission denied (publickey,password).\r\n",
    "unreachable": true
}
```
成功事例：(ansible all -m ping -u deploy)
```
94.191.29.229 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

# ansible命令格式
   ansible            all             -m ping                        -u deploy
（ansible主体，必须） （all目标，必须）  （模块，选填,默认使用commond模块）    (参数，选填)


例：
> ansible all -u deploy -a 'ls' 

将ls命令传入commend模块

| 参数 | 意义 |
| :------: | :------: | 
| -a | 传入模块的参数 |
| -C -D | 两个一起使用，检测hosts规则文件的修改|
| -l | 限制规则匹配的主机数量|
| --list-hosts | 显示所有匹配规则的主机数|
| -m -M | 一起用指定所使用的模块和模块路径|
| -u | ssh连接的用户名，默认用root，ansible.cfg中可以配置|
| -k | 提示输入ssh登录密码。当使用密码验证的时候用|
| -s | sudo运行|
| -C | 只是测试一下会改变什么内容，不会真正去执行|
| -c | 连接类型（default=smart）|
| -f | fork多少个进程并发处理，默认为5个|
| -i | 指定hosts文件路径，默认default=/etc/ansible/hosts|
| -M | 要执行的模块路径，默认为/usr/share/ansible|
| -o | 压缩输出，摘要输出|
| -T | ssh连接超时时间，默认10秒|
| -t | 日志输出到该目录，日志文件名以主机名命名|
| --syntax-check | 检查语法|

运行
* 显示匹配结果
> ansible all -a 'ls' --list-hosts -u deploy
```
hosts (1):
    94.191.29.229
```

# 分组（inventory）
修改hosts如下所示

```
94.191.29.229
[qianhu]
47.107.244.138
94.191.29.229
[hooook_test]
39.106.39.179
94.191.29.229
```
[]括号中包含的就是组名，一台机器可以属于多个组，一个组可以有多个机器
测试
> ansible qianhu -a 'ls' -u deploy

返回
```
47.107.244.138 | CHANGED | rc=0 >>
authorized_keys

94.191.29.229 | CHANGED | rc=0 >>
auto.py
```

还可以
> ansible 94.191.29.229 -a 'ls' -u deploy

## 自定义连接端口
如果有几台服务器ssh端口不是22可以在hosts中定义
```
94.191.29.229:2000
[qianhu]
47.107.244.138
94.191.29.229
[hooook_test]
39.106.39.179:2009
94.191.29.229
```

## 机器太多但是连续可以这样使用
```
[vim]
vim[1:50].example.com
vim[a-f].example.com
```
匹配
vim1.example.com到vim2.example.com

## 指定一组相关机器，匹配地址段
> ansible 47.107.244.* -a 'ls' -u deploy

## 指定一组不相关机器(冒号分割)
> ansible 47.107.244.138:39.106.39.179 -a 'ls' -u deploy

```
47.107.244.138 | CHANGED | rc=0 >>
authorized_keys

39.106.39.179 | CHANGED | rc=0 >>
```

## 匹配group_one组
> ansible group_one -a 'ls' -u deploy

## 匹配group_one和group_two组
> ansible group_one:group_two -a 'ls' -u deploy

## 指定在group_one组中但不再group_two组中
> ansible group_one:!group_two -a 'ls' -u deploy

## 指定同时在group_one组中和group_two组中
> ansible group_one:&group_two -a 'ls' -u deploy

## ad-Hoc
### 在group_one中的所有机器会fork十个子进程并以并行方式执行重启命令（即每次重启十个）
> ansible group_one -a "/sbin/reboot" -f 10 

### 使用sudo
> ansible group_one -a "/sbin/reboot"  -u username --sudo 

### 文件管理（file模块）
#### 创建文件夹（根目录下创建test_dir文件夹）
> ansible 94.191.29.229 -m file -a "dest=/test_dir mode=755 owner=deploy group=deploy state=directory" -u deploy
```
94.191.29.229 | CHANGED => {
    "changed": true,
    "gid": 1000,
    "group": "deploy",
    "mode": "0755",
    "owner": "deploy",
    "path": "/test_dir",
    "size": 4096,
    "state": "directory",
    "uid": 1000
}
```

### 拷贝文件（copy模块）
force 如果内容不同，是否启用强制覆盖.（(Choices: yes, no) [Default: yes]）
owner 文件/目录所有者
dest  远端的绝对路径。如果 src 是一个目录，那么 dest 的地址也必须是一个目录(如果前面加了'/'路径，标示复制到服务器的根目录)
src   本地路径（如果以'/'结尾，则 copy 文件夹内的内容，不包含文件夹本身，如果没有以'/'结尾，则会包含文件夹本身。）
> ansible 94.191.29.229 -m copy -a "src=/etc/hosts dest=/tmp/hosts" -u deploy
```
94.191.29.229 | CHANGED => {
    "changed": true,
    "checksum": "6635034a9924c8deca789fee4c59120538eda790",
    "dest": "/tmp/hosts",
    "gid": 1000,
    "group": "deploy",
    "md5sum": "dad8a484ffaa6dd51db785dc59aae0d8",
    "mode": "0664",
    "owner": "deploy",
    "size": 242,
    "src": "/home/deploy/.ansible/tmp/ansible-tmp-1548244990.59584-169057950898527/source",
    "state": "file",
    "uid": 1000
}
```

### 软件包管理（centos使用-m yum ,ubuntu使用-m apt）
#### 确认一个软件包已经安装，但不去升级它
> ansible 94.191.29.229 -m apt -a 'name=nginx state=present' -u deploy --sudo

没有找到这个包
```
94.191.29.229 | FAILED! => {
    "changed": false,
    "msg": "No package matching 'acme' is available"
}
```

找到这个包
```
94.191.29.229 | SUCCESS => {
    "cache_update_time": 1548245737,
    "cache_updated": false,
    "changed": false
}
```

#### 确认一个软件包没有安装
> ansible 94.191.29.229 -m apt -a 'name=nginx state=absent' -u deploy --sudo

确认这个包没有安装
```
94.191.29.229 | SUCCESS => {
    "changed": false
}
```

找到这个包
```
94.191.29.229 | CHANGED => {
    "changed": true,
    "stderr": "",
    "stderr_lines": [],
    "stdout": "Reading package lists...\nBuilding dependency tree...\nReading state information...\nThe following packages were automatically installed and are no longer required:\n  nginx-common nginx-core ssl-cert\nUse 'sudo apt autoremove' to remove them.\nThe following packages will be REMOVED:\n  nginx\n0 upgraded, 0 newly installed, 1 to remove and 26 not upgraded.\nAfter this operation, 37.9 kB disk space will be freed.\n(Reading database ... \r(Reading database ... 5%\r(Reading database ... 10%\r(Reading database ... 15%\r(Reading database ... 20%\r(Reading database ... 25%\r(Reading database ... 30%\r(Reading database ... 35%\r(Reading database ... 40%\r(Reading database ... 45%\r(Reading database ... 50%\r(Reading database ... 55%\r(Reading database ... 60%\r(Reading database ... 65%\r(Reading database ... 70%\r(Reading database ... 75%\r(Reading database ... 80%\r(Reading database ... 85%\r(Reading database ... 90%\r(Reading database ... 95%\r(Reading database ... 100%\r(Reading database ... 101468 files and directories currently installed.)\r\nRemoving nginx (1.10.3-0ubuntu0.16.04.3) ...\r\n",
    "stdout_lines": [
        "Reading package lists...",
        "Building dependency tree...",
        "Reading state information...",
        "The following packages were automatically installed and are no longer required:",
        "  nginx-common nginx-core ssl-cert",
        "Use 'sudo apt autoremove' to remove them.",
        "The following packages will be REMOVED:",
        "  nginx",
        "0 upgraded, 0 newly installed, 1 to remove and 26 not upgraded.",
        "After this operation, 37.9 kB disk space will be freed.",
        "(Reading database ... ",
        "(Reading database ... 5%",
        "(Reading database ... 10%",
        "(Reading database ... 15%",
        "(Reading database ... 20%",
        "(Reading database ... 25%",
        "(Reading database ... 30%",
        "(Reading database ... 35%",
        "(Reading database ... 40%",
        "(Reading database ... 45%",
        "(Reading database ... 50%",
        "(Reading database ... 55%",
        "(Reading database ... 60%",
        "(Reading database ... 65%",
        "(Reading database ... 70%",
        "(Reading database ... 75%",
        "(Reading database ... 80%",
        "(Reading database ... 85%",
        "(Reading database ... 90%",
        "(Reading database ... 95%",
        "(Reading database ... 100%",
        "(Reading database ... 101468 files and directories currently installed.)",
        "Removing nginx (1.10.3-0ubuntu0.16.04.3) ..."
    ]
}
```

### git模块（拉代码，提交代码）
...

### service模块（系统服务相关） 
...

### 执行耗时任务
-B 3600  表示最多执行60分钟
-P 0     表示不获取状态
-P 60    表示每隔1分钟一次状态
> ansible 94.191.29.229 -B 3600 -P 0 -a 'some_long_time_running'