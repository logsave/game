## 模式匹配：Case
1. case 语法结构
```bash
case 变量 in
模式1)
    命令1
    ;;
模式2)
    命令2
    ;;
模式3)
    命令3
    ;;
*)
    无匹配命令
esac
```
> type 查看是否是关键字
> 删除当前行到结尾 `dG`

### Case多系统配置 yum 源
```bash
#!/bin/bash
yum_server=10.0.0.11
os_version=`cat /etc/redhat-release | awk '{print $4}' \
|awk -F"." '{print $1"."$2}'`

[ -d /etc/yum.repos.d ] || mkdir /etc/yum.repos.d/bak
mv /etc/yum.repos.d/*.repo /etc/yum.repos.d/bak &> /dev/null

case "$os_version" in
7.3)
    cat > /etc/repos.d/centos7u3.repo <<-EOF
    [centos7u3]
    name=centos7u3
    baseurl=ftp://$yum_server/centos7u3
    gpgcheck=0
    EOF
    echo "7.3 yum configure."
    ;;
6.8)
    curl -o /etc/yum.repos.d/centos6u8.repo ftp://$yum_server/centos6u8.repo
    ;;
5.9)
    curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-5.repo
    ;;
*)
    echo "error"
esac
```

### Case 删除用户判断
范例1: 简单的模式匹配（确认操作）
```bash
#!/bin/bash
# delete user
# V1.0 by logsave 2020-11-27
read -p "Please input a username: "user

id $user &> /dev/null
if [ $? -ne 0 ]; then
    echo "No such user: $user"
    exit 1 # 返回 0 表示脚本执行成功，执行异常给出错误返回值
fi

read -p "Are you sure? [y/n]: " action
if [ "$action" = "y" -o "$sction" = "Y"]; then
    # 删除用户
    userdel -r $user
    echo "$user is delete!"
else
    echo "Exit.!"
fi
```
范例2: 将上述范例 `if` 修改为 `case` 
```bash
case "$action" in
y|Y|yes|YES)
    userdel -r $user
    echo "$user is deleted!"
    ;;
*)
    echo "Input is Error"
esac
```
> `case` 只适合模式匹配，针对条件判断还是需要使用 `if` 语句进行实现。

> 针对条件判断中变量是否使用 `"`，多个添加逻辑或。
> VIM 注释 CTRL + V ；选择；SHIFT + I 前面插入的内容； ESC


### Case 实现 Jump Server
系统登录自动执行脚本
    - /etc/profile 全局
    - /etc/bashrc 公用
    - /home/user1/.profile
    - /home/user1/.bashrc

1. 密码认证
```bash
#!/bin/bash
# JumpServer
while :
do
    cat <<-EOF
    1. web1
    2. web2
    3. mysql1
    EOF

    read -p "Input number: " num
    case "$num" in
    1)
        ssh alice@slave1
        ;;
    2)
        ssh alice@slave2
        ;;
    3)
        ssh alice@slave3
        ;;
    "")
        ;;
    *)
        echo "Error"
    esac
done
```

2. 密钥认证
    ```
    # 查看当前用户
    whoami
    # 生成公私钥
    ssh-keygen
    # 将私钥拷贝到目标主机
    ssh-copy-id 192.168.0.11
    # 将 jumpServer.sh 脚本执行命令追加到 /home/alice/.bash_profile
    ```
    用户进入跳板机后，可以进行操作。此时使用 `CTRL + C` 退出后，能够在跳板机操作。
    需要捕捉用户退出的信号。   
    `trap "" HUP INT OUIT TSTP`   
    echo 默认换行，使用 `echo -n` 不换行。
    `echo -e` 可以设置打印字体颜色。

> 生产环境
> 1. 业务服务器不允许直接连接，通过允许从跳板机连接
> 2. 业务服务器不允许 root 用户直接登录

https://www.bilibili.com/video/BV1g4411Y75K?p=28

### Case 实现简单的系统工具箱
```bash
#!/bin/bash
# System Mange
menu() {
cat <<-EOF
    h. help
    f. disk partition
    d. filesystem mount
    u. system load
    q. exit
EOF
}

menu

while :
do
    read -p "please Input [h] for help: " action
    case "$action" in
    h)
        clear
        menu
        ;;
    f)
        fdisk -l
        ;;
    d)
        df -Th
        ;;
    m)
        free -m
        ;;
    u)
        uptime
    q)
        # exit
        break
        ;;
    *)
        echo "error"
    esac
done
```

-------------------

```bash
# 判断是否为一个命令
command -v /etc/hosts 
echo $?  # 1

# if 语句中除了条件判断，还可以执行命令，判断是否执行成功。
cmd1=/bin/date
if command -v $cmd1 &>/dev/null; then
    :
else
    # yum -y install
    echo "Instal Xxxx"
fi

命令 `:` 返回值为真，和 `true` 等价。

# 账号管理
$ useradd logsave
$ passwd logsave


`while :` or `until false`
exit 强制退出，循环中使用 break 较好。
```







