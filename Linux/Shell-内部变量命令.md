

#### bash内部变量命令 

1. echo args
    将echo命令后面的args指定的字符串及变量等显示到标准输出

2. eval args
    当Shell程序执行到eval语句时，Shell读入参数args，并将它们组合成一个新的命令，然后执行。

3. exec 命令参数
    当Shell执行到exec语句时，不会去创建新的子进程，而是去执行指定的命令，当指定的命令执行完时，该进程就终止了，所以Shell程序中exec后面的语句将不再被执行。 

4. export 变量名[=变量值]
    Shell可以用export把它的变量向下带入子Shell，从而让子进程继承父进程中的的环境变量。但子Shell不能用export把它的变量带入父Shell。
> 不带任何参数的export语句将显示当前所有的export变量。

5. readonly 变量名（很少用）
    将一个用户定义的Shell变量标识为不可变。不带任何参数的readonly命令将显示所有只读的Shell变量。

6. read 变量名表
    从标准输入读字符串等信息，传给Shell程序内部定义的变量。
    可以在函数中用local变量名的方式声明局部变量。

7. shift

8. wait
    使Shell等待在后台启动的所有子进程结束。wait的返回值总是真。

9. exit
    退出Shell程序。在exit之后可指定返回状态。

10. `.` Shell程序
    使Shell读入制定的Shell程序文件并依次执行文件中的所有语句


#### 变量子串的常用操作（了解）

```bash
${#string} 返回$string的长度
${string:position} 在$string中，从位置$position之后开始提取子串
${string:position:length} 在$string 中，从位置$position 之后开始提取长度为$length的子串。
${string#substring} 从变量$string开头开始删除最短匹配$substring子串。
${string##substring} 从变量$string 开头开始删除最长匹配$substring子串。
${string%substring} 从变量$string结尾开始删除最短匹配$substring 子串
${string%%substring} 从变量$string 结尾开始删除最长匹配$substring子串
${string/substring/replace} 使用 $replace 来替换第一个匹配的 $substring。
${string/#substring/replace} 如果$string 前缀匹配$substring ，就用 $replace 来替换 $substring。(使用通配符 最短匹配)
${string/%substring/replace} 如果 $string 后缀匹配 $substring，就用 $replace 替换 $substring。(使用通配符 最长匹配)
```
> `#` 表示开头，`%` 表示结尾。

```bash
[root@master rename]# A="hhhi hi logsave ha ha"
[root@master rename]# echo ${A#h*i}
hi logsave ha ha
[root@master rename]# echo ${A##h*i}
logsave ha ha
```

> 其他相关操作
```bash
[root@master ~]# echo "Hello WOrld"|wc -L
11
[root@master ~]# echo "hello world "| cut -c 3-6
llo 

```
> 批量改名
```bash
[root@master rename]# touch a.txt b.txt c.txt
[root@master rename]# ls
a.txt  b.txt  c.txt
[root@master rename]# for i in `ls`; do
>   mv $i "${i%txt}md"
> done
[root@master rename]# ls
a.md  b.md  c.md
```

> 创建文件并批量修改文件名
```bash
[root@master rename]# cat file.log 
a.txt
b.txt
c.txt
t.txt
[root@master rename]# touch `cat file.log|tr "\n" " "`
# str 为要删除的子串，也可以使用替换等操作
[root@master rename]# for file in `ls *.txt`;do
> mv $file "${file%str}"
> done

```

### 变量替换

1. `${value:-word}`
    当变量未定义或者为空时，返回 `:-` 后面的值
2. `${value:=word}`
    当变量不存在的时候，返回后面的值，并给变量赋值后面的内容
3. `${value:?"word"}`
    捕获由于变量未定义导致的错误，并推出程序
4. `${value:+word}`
    用于测试变量是否存在，存在返回word
5. `${value-word}` 
    当变量未定义时，返回后面的值

### 变量替换应用

    在删除、寻找的时候进行验证、替换
```bash
find ${path-/tmp} -type f -name "*.log" -mtime +7
```

### 命令性能比较
> 一般内置命令性能更高，管道等操作耗时较大
```bash
chars=`seq -s " " 100`
echo ${#chars}
echo $chars| wc -L
echo $(expr length "$chars")

[root@master a]# time for i in $(seq 11111);do count=${#chars};done
real    0m0.281s
user    0m0.276s
sys     0m0.005s
[root@master a]# time for i in $(seq 11111);do count=`echo ${chars}|wc -L` ;done
real    0m50.982s
user    0m13.174s
sys     0m51.523s
[root@master a]# time for i in $(seq 11111); do count=`echo $(expr length "$chars")`; done

real    1m4.266s
user    0m13.845s
sys     0m52.615s
```

### 变量的数值（整数）计算
> 20201103 21点53分 L81-25

变量的数值计算常见的有如下几个命令：
(())、let、expr、bc、$[]

1. `(())` 用法
如果要执行简单的整数运算，只需要将特定的算术表达式用 `$((` 和 `))` 括起来。
Shell 的算数运算符号常置于 `$((  ))` 的语法中。这一语法如同双引号功能，除了内嵌双引号无需转义。

| 运算符    |  意义           |
|-----------|----------------|
| __++  --__    | 增加及减少，可前置也可放在结尾
| __+ - ! ~__   | 一元的正号与负号；逻辑与 取反
| __* / %__     | 乘法、除法、取余
| __+ -__       | 加法、减法
| __< <= > >=__ | 比较符号
| __== !=__     | 相等、不相等，一个 `=` 赋值
| &         | 位运算 AND
| ^         | 位运算 异或
| `|`       | 位运算 或
| &&        | 逻辑 AND `make && make install`
| `||`      | 逻辑 OR
| ?:        | 条件表达式
| `= += -= *= /= %= &= ^= <<= >>= |=` | 赋值运算符 a+=1 都相当于 a=a+1

范例1：Shell的算术运算
```bash
[root@master ~]# ((a=1+2**3-4%3))     
[root@master ~]# echo $a
8
[root@master ~]# b=$((1+2**3-4%3))  
[root@master ~]# echo $b
8


[root@master ~]# unset a
[root@master ~]# echo $((a+=1))
1
[root@master ~]# echo $((a++))
1
[root@master ~]# echo $a
2
[root@master ~]# echo $((a--))
2
[root@master ~]# echo $((3>2))
1
[root@master ~]# echo $((3<2))
0

```
> 1. ** 为幂运算：% 为取模运算
> 2. 上面设计到的参数变量必须为整数（整型）。不能是小数（浮点数）或者字符串。后面的 `bc` 命令可以进行浮点数运算，但一般使用较少。可以直接在 Shell 脚本中使用上述命令进行计算。
> 3. `echo $((a++))` 和 `echo $((a--))` 表示先输出 a 自身的值，然后再进行运算；`echo $((++a))` 和 `echo $((--a))` 表示先进行运算，再输出 a 自身的值。

范例2：计算 1 到 100 的和 
```bash
[root@master ~]# echo $((100*(100+1)/2))
5050
[root@master ~]# sum=0; for i in `seq 100`; do ((sum+=$i)); done
[root@master ~]# echo $sum
5050
```

范例3：各种 `(( ))` 的计算命令行
```bash
[root@master ~]# echo $(( 100 / 5 ))
20
[root@master ~]# echo $(( 100 + 5 ))
105
[root@master ~]# echo $(( 100 * 5 ))
500
[root@master ~]# echo $(( 100 - 5 ))
95
[root@master ~]# echo $(( 100 ** 5 )) # 幂运算
10000000000
[root@master ~]# echo $(( 100 % 5 )) # 取余
0
```
范例4：各种 `(( ))` 运算的 Shell 脚本
```bash
#!/bin/bash

a=6
b=2

echo "a-b = $(( $a - $b ))"
echo "a+b = $(( $a + $b ))"
echo "a*b = $(( $a * $b ))"
echo "a/b = $(( $a / $b ))"
echo "a**b = $(( $a ** $b ))"
echo "a%b = $(( $a %% $b ))"
```
执行结果：
```
[root@master Desktop]# sh test.sh 
a-b = 4
a+b = 8
a*b = 12
a/b = 3
a**b = 36
a%b = 0
```

范例5：将变量通过命令行脚本传参的方式实现上述运算
```bash
#!/bin/bash

a=$1
b=$2

echo "a-b = $(( $a - $b ))"
echo "$(($1$2$3))"
```
双括号建议使用，效率很高。最重要的一个用法。

```
# L81-26 19:30 读取计算
read -p "输入" foo
if [ -n ""]; then
    print_usage
fi

read -p "sss" bar

```
网上搜索 Shell 计算实现方式

----

2. let 命令的用法

格式：`let 赋值表达式`
> let 赋值表达式功能等同于： `((赋值表达式))`

范例1：给自变量 i 加 8
```bash
[root@master ~]# i=2
[root@master ~]# let i=i+8
[root@master ~]# echo $i
10
[root@master ~]# i=i+8
[root@master ~]# echo $i
i+8
```
> `let i=i+8 等同于 `((i=i+8))`，但后者效率更高

范例2：利用 let 计数监控 web 服务状态(守护进程)
```
# 监控服务状态
SerferMonitor() {
    timeout=10
    fails=0
    success=0
    while true; do
        /usr/bin/wget --timeout=$timeout --tries=1 http://192.168.20.84 -q -O /dev/null
        if [ $? -ne 0 ]; then
            let fails=fails+1
            success=0
        else
            fails=0
            let success=1
        fi
        if [ $success -ge 1]; then
            exit 0
        fi
        if [ $fails -ge 2 ]; then
            Critical="TMS 应用服务出现故障，请紧急处理！"
            echo $Critical | mutt -s "服务down" yan1ei@126.com
            exit
        fi
    done
}
```

3.  expr（evaluate expressions）命令的用法
    expr 命令一般用于整数值，但也可用于字符串，用来求表达式变量的值，同时 expr 也是一个手工命令行计算器。
 ```
 [root@master ~]# expr 2 + 2
4
[root@master ~]# expr 2+2  
2+2
[root@master ~]# expr 2 \* 2
4
[root@master ~]# expr 4 / 2 
2
[root@master ~]# expr 5 % 2
1
 ```   
> 1. 运算符及数字两边都有空格
> 2. 使用乘号时，必须使用反斜线转义。

expr 在循环中可用于增量计算。首先，循环初始化为 0，然后循环值加 1，反引号的用法为命令替代。最基本的一种是从 expr 命令接受输出并将之放入循环变量。
范例：给自变量加 1
```
[root@master ~]# i=0
[root@master ~]# i=`expr $i + 1`
[root@master ~]# echo $i
1
```

`expr $[$a+$b]` 表达式形式，其中 $a $b 可为整数值
```
[root@master ~]# expr $[2+3]
5
[root@master ~]# expr $[2*3]
6
[root@master ~]# expr $[2**3]
8
[root@master ~]# expr $[2/3]
0
[root@master ~]# expr $[2%3]
2
```

expr 特殊用法：
expr 用法 ssh-copy-id 脚本
```bash
if expr "$1" : ".*\.pub"; then

# expr id_dsa.pub : '.*\.pub',匹配 *.pub 格式文件如果是则为真
[root@master ~]# expr "id_rsa.pub" : ".*\.pub"
10
```

判断扩展名：
```bash
#!/bin/sh
if expr "$1" : ".*\.pub" &> /dev/null; then
    echo "you are using $1"
else
    echo "pleas use *.pub fail."
fi

# [root@master ~]# file initial-setup-ks.cfg |grep "ASCII text$"> /dev/null && echo 1 || echo 0
# 1
```

通过 expr 判断变量是否为整数
```bash
#!/bin/bash

expr 1 + $1 &> /dev/null 
[ $? -eq 0 ] && echo int || echo chars

#!/bin/sh
while true; do
    read -p "input:" a
    expr $a + 0 > /dev/null 2>&1
    [ $? -eq 0 ] && echo int || echo chars
done
```

通过 expr 计算字符串的长度
```bash
[root@master ~]# chars=`seq -s" " 100`
[root@master ~]# echo ${#chars}
291
[root@master ~]# echo $(expr length "$chars")
291
```

4. bc 命令的用法
bc 是 UNIX 下的计算器，它可以用在命令行：
范例：给自变量 i 加 1
```
i=2
i=`echo $i + 1 | bc` # 效率低
```
因为支持科学计算，所以这种方法功能强大
```
[root@master ~]# echo "10/3"|bc         
3
[root@master ~]# echo "scale=4; 10/3"|bc
3.3333
[root@master ~]# echo "obase=2; 8"|bc # 十进制转换为二进制
1000

[root@master ~]# echo `seq -s '+' 10`=`seq -s '+' 10|bc`
1+2+3+4+5+6+7+8+9+10=55
[root@master ~]# echo `seq -s '+' 10`="$((`seq -s '+' 10`))"
1+2+3+4+5+6+7+8+9+10=55

[root@master ~]# echo `echo {1..10}|sed -e 's/ /+/g'`=`echo {1..10}|sed -e "s# #+#g"|bc`
1+2+3+4+5+6+7+8+9+10=55
[root@master ~]# echo `seq -s '+' 10`=`seq -s ' + ' 10|xargs expr`
1+2+3+4+5+6+7+8+9+10=55
```
bc 的独有特点是支持小数运算，当然也可以整数运算。

> xargs 用法

5. typeset 命令的用法
```
[root@master ~]# typeset -i A=1 B=3
[root@master ~]# A=A+B
[root@master ~]# echo $A
4
```

6. $[] 的用法
```
[root@master ~]# echo $[ 2 + 3 ]
5
[root@master ~]# echo $[ 2 * 3 ]
6
[root@master ~]# echo $[3+2]
5
[root@master ~]# echo $[2**3]
8
```

[shell 打印杨辉三角](https://www.cnblogs.com/xieshengsen/p/7146637.html)




---------
### Shell 变量的输入
Shell 变量除了可以直接赋值或脚本传参外，还可以使用 `read` 命令(内置命令)从标准输入获得。
语法格式：`read [参数] [变量名]`
常用参数：
```
-p prompt:设置提示信息
-t timeout 设置输入等待的时间，单位默认为秒。
```

范例1：`read` 的基本读入
```
[root@master ~]# read -p "Input:" a b c
Input:1 2 3 4 
[root@master ~]# echo $a
1
[root@master ~]# echo $b
2
[root@master ~]# echo $c
3 4

[root@master ~]# echo -n "Input:"; read a
Input:123 
[root@master ~]# echo $a
123
```

L82-2





