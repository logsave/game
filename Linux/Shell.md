
# Shell脚本


## L080 Shell脚本编程
> 03

### 变量

使用一个固定名称名称表示具有某种意义的值，这个名称就是变量。

变量可分为两类：环境变量（全局变量）、局部变量。

环境变量可以在创建它们的Shell及派生出来的任意子进程Shell中使用。
局部变量只能在创建它们的Shell函数或脚本中使用。
还有一些变量是用户创建的，其它的则是专用Shell变量。

#### 环境变量

环境变量用于定义Shell的运行环境，保证Shell的正确执行，Shell通过环境变量来确定登录用户名、命令路径、终端类型、登录目录等，所有的环境变量都是系统全局变量，可以用于所有子进程中，着包括编辑器、Shell脚本和各类应用（crond任务使用使用 `export` 导入）。

环境变量可以在命令行中设置，但是用户退出时这些变量值也会丢失，因此最好在用户家目录下的 `.bash_profile` 文件中或全局配置 `/etc/bashrc` , `/etc/profile` 文件或 `/etc/profile.d` 中定义。 
将环境变量放入上述文件中，每次用户登录时这些变量值都会被初始化。

传统上，所有 __环境变量均为大写__。
环境变量应用于用户进程前，都应该用 `export` 命令导入。

```bash
# 用户家目录
[root@master /]# echo $HOME
/root
# 当前用户
[root@master /]# echo $USER
root
# 用户ID
[root@master /]# echo $UID
0
```

使用 `env` 命令查看当前系统的环境变量。
```bash
_  ：上一条命令的最后一个参数
BASH ：调用bash使用的全路径名

```

#### 自定义环境变量

##### 设置环境变量

给变量赋值的时候使用 `export` 命令，就可以设置为环境变量。

带 `-x` 选项的 `declare` 内置命令也可完成同样的功能。

```bash
[root@master /]# declare -x A=12345
[root@master /]# export B=hello
[root@master /]# C=shell; export C
[root@master /]# env | grep '^\w='   
A=12345
B=hello
C=shell
_=/usr/bin/env
```

环境变量设置的文件及区别：
1. 用户的环境变量配置
    `/root/.bashrc` 、 `/root/.bash_profile`
2. 全局环境变量
    `/etc/bashrc` 、`/etc/profile`
3. 登录执行脚本 `/etc/profile.d/`
    ```bash
    [root@master /]# cd /etc/profile.d/
    [root@master profile.d]# vi yanlei.sh 
    echo "======= profile.d/yanlei  ========="

    [root@master profile.d]# exit
    exit
    [yanlei@master ~]$ su root
    Password: 
    ======= profile.d/yanlei  =========
    ```
> `/etc/motd` 中的文本为登录后显示内容，在 `/etc/profile.d/` 之前。

> 启动后执行 `/etc/rc.d/rc.local`

##### 显示与取消环境变量
1. 使用 `echo`、 `printf`输出环境变量
```bash
[root@master ~]# printf "$HOME\n"
/root
[root@master ~]# echo $HOME
/root
```
2. 用`env`（`printenv`）或 `set`显示环境变量
```bash
[root@master ~]# printenv
XDG_SESSION_ID=249
HOSTNAME=master
...

```
3. 用 `unset` 取消本地变量和环境变量
```bash
[root@master ~]# AAA="hello world" 
[root@master ~]# echo $AAA
hello world
[root@master ~]# unset AAA
[root@master ~]# echo $AAA

```
> 和PHP中的 `unset`、Python中的 `del` 作用相同。

#### 局部变量

本地变量在Shell脚本生存周期中使用。
```bash
[root@master scripts]# cat test_var.sh 
#/bin/bash
user="yanlei"
[root@master scripts]# sh test_var.sh 
[root@master scripts]# echo $user

# 上述输出为空 
```
> 上述脚本使用bash进行执行，即使使用 `export` 执行，在执行结束后，`user`变量就不存在了。
> 但是使用 `source *.sh` 或 `. *.sh` 执行，变量在当前连接的终端存在。

#### 变量定义

1. 普通字符串变量定义
    ```bash
    name=value
    name='value'
    name="value"
    ```
    
    ```bash
    # 命令
    name=``
    name=$()
    ```

> 连续字符串按原样输出；   
> 直接定义变量内容（简单连续数字、字符串）会将变量解析；使用`''`（纯字符串）会按原样输出；使用 `""` （字符串带有变量）也会将变量解析。 

> 建议：数字不加引号，其它默认使用 `""`。

1. 单引号原样显示
2. 双引号里面的变量会进行解析；命令需要使用 ` `` ` 或 `$( )` 进行执行。


__grep__ 命令中变量测试：
```bash
[root@master test]# cat grep.log 
hello
world
hello world  
[root@master test]# H=hello
[root@master test]# echo $H
hello
[root@master test]# grep "$H" grep.log 
hello
hello world
```

__awk__ 命令中变量测试：
```bash
[root@master test]# ETT=123
[root@master test]# awk 'BEGIN {print "$ETT"}'
$ETT
[root@master test]# awk 'BEGIN {print '$ETT'}'
123
[root@master test]# awk 'BEGIN {print $ETT}'  

[root@master test]# awk "BEGIN {print $ETT}" 
123
```

#### 变量命名规范

1. 变量命名统一
    使用 `${}` 、`"${}"` 方式使用。  
2. 避免无含义字符或数字

3. 全局变量和局部变量命名   
    1. 全局变量使用大写
    2. 脚本中局部变量使用 `local` 声明，使其只在本函数中生效。
    ```
    function testVar()
    {
        local i
        for((i=0;i<n;i++))
        do
         echo "do something"
        done
    }
    ``` 

    ```bash
    function testVar()
    {
        local i
        for i in $*; do
            [ -d "/proc/$i" ] && return 0
        done
        return 1
    }
    ```
    3. 变量较长时，可以进行拼接。
    ```bash
    DIR="/root/"
    FILE="test.log"
    FILENAME="${DIR}${FILE}"
    ```
    4. 变量定义常见命名方式
    - `HelloWorld=1`
    - `hello_world=1`
    - `helloWorld=1`

##### 把命令结果作为变量

1. `DIR= `pwd ，使用 ` `` ` 
2. 使用 `$` 或 `${}` 获取变量的值，对变量、字符连续的必须使用 `${}`
3. 字符串变量使用双引号，减少错误。

```bash
[root@master test]# DATE=$(date +%F)
[root@master test]# echo ${DATE}.tar.gz
2020-06-03.tar.gz

[root@master test]# ls -l `which cat`
-rwxr-xr-x. 1 root root 54080 Apr 11  2018 /usr/bin/cat
```

```bash
[root@master ~]# find ./test/ -type f -name "*.log"       ./test/grep.log
[root@master ~]# sed -i 's#hello#hihihi#g' `find ./test/ -type f -name "*.log"`

[root@master ~]# find ./test/ -type f -name "*.log"|xargs cat
hihihi
world
hihihi world
```

#### Shell特殊变量

1. 位置变量

```bash
$0 获取当前执行Shell脚本的文件名，如果执行带有路径，就包括路径名
$n 获取当前执行Shell脚本的第n个参数值，n大于10 使用 `{}` 表示
$* 获取当前Shell的所有参数，将所有命令参数视为单个字符串，相当于`"$1$2$3..."`
$# 获取当前Shell命令行中参数的总个数
$@ 获取这个程序的所有参数 `"$1" "$2" "$3" "..."`，这是将参数传递给其它程序的最佳方式。
```

> 范例：`dirname` `basename`
```bash
[root@master scripts]# cat pos_var.sh 
#!/bin/bash
dirname $0
basename $0
[root@master scripts]# sh pos_var.sh 
.
pos_var.sh
```

> 查看系统服务 portmap 脚本

```bash
[root@master scripts]# seq 5|sed 's#^#$#g' | tr "\n" " "
$1 $2 $3 $4 $5 
```

```bash
[root@master scripts]# seq -s " " 10 | sed 's# # $#g'    
1 $2 $3 $4 $5 $6 $7 $8 $9 $10
[root@master scripts]# echo {a..z} 
a b c d e f g h i j k l m n o p q r s t u v w x y z

[root@master scripts]# cat q.sh 
echo $1 $2 $3 $4 $5 $6 $7 $8 $9 $10
[root@master scripts]# sh q.sh {a..z}
a b c d e f g h i a0

```
> `{a..z}` 生成序列
> `seq 10` -s 参数指定分割符
> `$10` 如果不加 `{}` 处理为 `$1` 和 `0` 拼接

> 范例：参数个数判断
```bash
[root@master scripts]# cat t1.sh 
[ $# -ne 2 ] && {
  echo "param is not equal two"
  exit 1 # 可以通过 $? 获取
}
echo "end"
[root@master scripts]# bash t1.sh 1 
param is not equal two
[root@master scripts]# bash t1.sh 1 2
end
```

2. 进程状态变量

```bash
$$ 获取当前Shell的进程编号（PID）
$! 执行上一个指令的PID
$? 获取执行上一个指令的返回值（0为成功，非0为失败） 【常用】
$_ 在此之前执行的命令或脚本的最后一个参数
```
> 范例：`$?` 
```bash
[root@master scripts]# ls /exist
ls: cannot access /exist: No such file or directory
[root@master scripts]# echo $?
2
```

> 范例：`$$`
```bash
[root@master scripts]# cat test_pid.sh 
echo $$ > /tmp/a.pid
sleep 100
[root@master scripts]# bash test_pid.sh &
[1] 9149
[root@master scripts]# ps -ef|grep test_pid.sh |grep -v grep
root       9149   8917  0 00:50 pts/2    00:00:00 bash test_pid.sh
[root@master scripts]# cat /tmp/a.pid 
9149
[root@master scripts]# kill -USR2 `cat /tmp/a.pid`

```

> 当系统中某个脚本只能运行一个时
```bash
#!/bin/bash

PID_PATH=/tmp/a.pid
if [ -f "$PID_PATH" ]; then
  kill -USR2 `cat $PID_PATH` >/dev/null 2>&1
  rm -f $PID_PATH
fi

echo $$ > $PID_PATH
sleep 100
```

> 返回值
```
1 - 125 运行失败
126 无法执行
127 未找到要运行的命令
>128 命令被强制结束
```

> 脚本调用一般用 `exit 0`，函数使用 `return 0`。


#### *学习系统脚本

开源软件启动脚本，例如：
- 系统默认脚本
- Hadoop

```bash
# 传入三个参数
[root@master ~]# set -- "ni hao" hello world
[root@master ~]# echo $#
3
# $* 将参数作为一个字符串输出
[root@master ~]# for i in "$*"; do
> echo $i
> done
ni hao hello world
# $@ 带双引号，每个参数独立输出
[root@master ~]# for i in "$@"; do
> echo $i
> done
ni hao
hello
world
[root@master ~]# for i in $@; do
> echo $i
> done
ni
hao
hello
world
# 简写：不使用 in 变量列表，相当于 "$@"
[root@master ~]# for i ;do
> echo $i
> done
ni hao
hello
worldw

```

3. 移动位置变量的命令 `shift` 

将位置变量向前移动，默认为 1，可以加参数指定移动数量。

> 使用频率
```
$? $n $# $0 $$
```




 `$*` 和 `$@` 的区别？
```
$* 获取当前Shell脚本所有参数，将所有参数视为单个字符串，`$1 $2 $3`
$@ 将每个参数视为单个单个字符串，等同于 `"$1" "$2" "$3"`,将参数传递给其它程序的最佳方式。
```




```bash
df -h 查看磁盘挂载信息
du -sh 查看文件及目录大小
tune2fs
dump2fs
time
uniq 去重
zip 
unzip

kill -9 进程号
killall -9 进程名
pkill 进程名

dirname 文件路径
basename 文件名字
printf   格式化打印

alias vi="vim"


内置命令总结：
echo
exec
eval
export
readonly
read
shift
wait
exit
time
expr 

```
