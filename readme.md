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