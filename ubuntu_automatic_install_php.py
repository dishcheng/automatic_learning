# coding=utf-8
import os
import sys
import platform

print(sys.version)
if 'Ubuntu' not in platform.version():
    print('只能在ubuntu系统中运行')
    exit(1)
# # print(os)
# # if os.getuid() != 0:
# #     print('请使用root账户')
# #     exit(1)

py_version = sys.version_info[0]  # 获取py大版本号

# os.rename('/etc/apt/sources.list', 'sources.list.bak')
# shutil.move('./sources.list', '/etc/apt/')
os.system('sudo mv /etc/apt/sources.list /etc/apt/sources.list.bak')
os.system('sudo mv ./sources.list /etc/apt/sources.list')


# py2 input获取的输入类型是float、或变量名，在python2中需要使用raw_input()获取输入的字符串
# py3 input获取的输入类型是字符
def input_str(str, is_confirm=False):
    if is_confirm:
        str2 = '是否安装' + str + '？（y/n）' + '?'
    else:
        str2 = str
    if py_version == 3:
        install = input(str2)
    else:
        install = raw_input(str2)

    if is_confirm:
        while install not in ['y', 'n']:
            return input_str(str, is_confirm)
        return install
    else:
        return install


def is_php_version_in_enum():
    php_ver = input_str('请输入您想要的php版本(7.3/7.2/7.1/7.0):', False)
    if (php_ver in ['7.3', '7.2', '7.1', '7.0']):
        return php_ver
    else:
        print('输入值不合法')
        return is_php_version_in_enum()


php_version_input = is_php_version_in_enum()
print(php_version_input)
install_php_mysql = input_str('php' + php_version_input + '-mysql', True)
install_php_fpm = input_str('php' + php_version_input + '-fpm', True)
install_php_moudle = input_str(
    'php' + php_version_input + '-curl php' + php_version_input + '-xml php' + php_version_input + '-bcmath php' + php_version_input + '-json php' + php_version_input + '-gd php' + php_version_input + '-mbstring php' + php_version_input + '-intl php' + php_version_input + '-zip',
    True)

install_nginx = input_str('nginx', True)
install_mysql_server = input_str('mysql-server-5.7', True)
install_composer = input_str('composer', True)
install_zip = input_str('zip', True)
install_redis_server = input_str('redis-server', True)


def install_cmd(name, need_install):
    if need_install == 'y':
        res = os.system('sudo apt-get -y install ' + name + '')
        if res != 0:
            print(name + ' 安装失败')
        else:
            print(name + ' 安装成功')
    else:
        print(name + '未安装')


install_cmd('php' + php_version_input, 'y')

install_cmd('php' + php_version_input + '-mysql', install_php_mysql)

install_cmd('php' + php_version_input + '-fpm', install_php_fpm)

install_cmd(
    'php' + php_version_input + '-curl php' + php_version_input + '-xml php' + php_version_input + '-bcmath php' + php_version_input + '-json php' + php_version_input + '-gd php' + php_version_input + '-mbstring php' + php_version_input + '-intl php' + php_version_input + '-zip',
    install_php_moudle)

# tips:有的ubuntu系统默认安装的是apache2，先卸载apache
os.system('sudo apt-get remove --purge apache2')
# 安装nginx
install_cmd('nginx', install_nginx)

# 安装mysql
install_cmd('mysql-server-5.7', install_mysql_server)

# 安装composer
if install_composer == 'y':
    res = os.system('sudo wget https://dl.laravel-china.org/composer.phar -O /usr/local/bin/composer')
    if res == 0:
        os.system('sudo chmod a+x /usr/local/bin/composer')
        os.system('composer config -g repo.packagist composer https://packagist.laravel-china.org')
    else:
        print('composer 安装失败')
else:
    print('composer 未安装')

# 安装zip
install_cmd('zip', install_zip)

# 安装redis
install_cmd('redis-server', install_redis_server)
