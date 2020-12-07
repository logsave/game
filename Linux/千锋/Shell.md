# Shell

### 1. Bash中调用Python

```bash
#!/usr/bin/bash
ping -c1 192.168.0.1 &> /dev/null && echo "UP" || echo "Down"

/usr/bin/python << EOF
print("Hello Python")
EOF

echo "Hello Bash"

```

```python
#!usr/bin/python3

import os

print("Hello Python")

os.system("""

echo "Hello Bash!"
cat << EOF
Hello Bash - cat01
Hello Bash - cat02
EOF

""")
```

### 2. 脚本执行方式

```bash
# Sub Shell 中执行
bash demo.sh

./demo.sh

# 当前Shell中执行

. demo.sh

source demo.sh
```
### 3. 查看Linux支持的Shell
    cat /etc/shells

    su alice

    usermod -s /bin/bash alice


expect

## 1. Shell特性

```
    login Shell
        su - name 
    nologin Shell
        su name
    
    # 系统级
    /etc/profile
    /etc/bashrc

    # 用户级
    ~/.bash_profile
    ~/.bashrc
    ~/.bash_logout
    ~/.bash_history

    login Shell会执行上面的文件
    nologin Shell 只会执行 /etc/bashrc 、 ~/.bashrc
```


命令记忆

    !number  执行历史命令
    !string 执行上一条匹配的命令
    !$
    !! 执行上一条命令

别名
    # 查看、定义别名 
    alias
    # 取消别名
    unalias
    不执行别名 `\cp -r /etc/hosts .`

快捷键
    ^R 命令搜索
    ^D 退出 logout、exit
    ^A 光标移动到最前面
    ^E 光标移动到最后面
    ^L clear
    ^U
    ^K
    ^S 锁屏，可以执行命令
    ^Q 可以退出锁屏

前后台作业控制
    nohup
    &
    ^C
    ^Z
    bg %1
    fg %1
    kill %3
    screen
    ```
    screen -S install_software

    screen -list

    screen -r id
    ```
    bg、fg 命令 % 可以省略，但是kill 命令的 % 不能省略。
    此处 `%` 表示作业号。


输入输出重定向
    0 输入
    1 输出
    2 错误输出

    ```bash
    cat << EOF > file
    Hello 
    EOF
    ```
管道 | tee
    # 使用 -a 参数进行追加
    date | tee -a a.tmp


2020-912 p5 - p7 学习完成
## 2. Shell 变量

## 3. Shell 条件测试
    判断某一条件是否成立   
    调试脚本的时候使用 `bash -vx *.sh` 进行执行。
    1. 文件测试
        判断文件是否存在、文件类型、是否具有权限

        ```bash
        test -d /mysql_bak
        echo $?

        # 一般使用 [ 替代 test 命令，此时必须带 ] 参数
        [ -d /mysql_bak ]; echo $?
        ```
    2. 数值比较

        ```bash
        #!/bin/usr/bash
        if [ $UID -ne 0 ]; then
            echo "你没有权限！"
            exit
        fi
        ```

    3. 字符串比较

        ```bash
        #!/bin/usr/bash
        if [ $USER == "root" ]; then
            echo "root"
        fi
        ```

    ```
    条件测试的格式：
    test 条件表达世
    [ 条件表达式 ]
    [[ 条件表达式 ]]

    # 两个表达式都为 true 结果为 true
    EXPRESSION1 -a EXPRESSION2 
    # or
    EXPRESSION1 -o EXPRESSION2
    # 长度不为 0 字符串
    -n STRING
    
    # 等于
    INTEGER1 -eq INTEGER2
    # 大于等于
    INTEGER1 -ge INTEGER2
    # 大于
    INTEGER1 -gt INTEGER2
    # 小于等于
    INTEGER1 -le INTEGER2
    # 小于
    INTEGER1 -lt INTEGER2
    # 不等于
    INTEGER1 -ne INTEGER2

    # 新
    FILE1 -nt FILE2
    # 旧
    FILE1 -ot FILE2
    # 块设备
    -b FILE
    # 目录
    -d FILE
    # 存在
    -e FILE
    # 普通文件
    -f FILE
    # 特殊权限
    -g FILE

    # 当前用户对该文件是否有读权限
    -r FILE

    [ ! -d /ccc ] && mkdir /ccc
    [ -d /ccc ] || mkdir /ccc
    ```
```bash
查看文件是否是命令、关键字
type -a file_name

# 查看目录中文件中是否含有某个内容
grep 'cat $1' *

# 查看用户是否存在
id root
```

```bash
#!/usr/bin/bash
# 磁盘使用量
disk_use=`df -Th|grep '/$'|awk '{print $(NF-1)}'|awk -F "%" '{print $1}'`
echo $disk_use

mail_user=root
if [ $disk_use -ge 90 ];then
    echo "`date +%F-%H` disk: ${disk_use}%" | mail -s "disk war ..." $mail_user
fi
```

2020 0916 学习19-21节11分钟

## 4. Shell 数值运算

## 5. 流程控制


## 6. 项目




