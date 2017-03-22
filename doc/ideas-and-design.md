# 专题技术构想与设计(Updating)
> Author: 李大祥
StartTime : 2017-2-25-22：40
ModifyTime :  2017-3-22

## 1. System Model
**User  -  WebServer   -  GitServer**
**(a)** User 在Web 界面操作，提交内容,原则上只要提交就通过并展示在最上方。
**(b)** WebServer 负责 manage Accounts and control control  Permission of Access Folder In GitServer ，可能对User提交的内容进行初步check，保证内容符合 our base writing principle（比如不含某些关键词以及内容不是大量重复无用文字，比如字数不能过少)
**(c)** GitServer 负责git repository 的 manage and restore. If the content commited by user of git group , git server will restore and dont prevent it.

## 2. Develop Tools and Enviroment
Programming Language : Python , HTML , Javascript , CSS , And maybe some linux shell scripts.
Reasons :  Easy to use git commands directly , and also develop a Web Application easily

Server Enviroment : Centos 7
Develop Enviroment : Fedora  25
Database : Mariadb 10.1.21

## 3. Limition of Users 'Number on Linux
Maximum user number by logging via SSH  IS NOT 
Maximum number of users on Linux.

(In these case below , but maybe these **user's data will over Hundreds GB** and maybe use too much memory . So it needs tests.)
How to know it : 
```
$ cat /proc/sys/kernel/pty/max
```
How to modify it : 
```
vi /etc/sysctl.conf
kernel.pty.max = 5120
sysctl -p
```
[资料来源1 - maximum user number by logging via SSH](http://unix.stackexchange.com/questions/73033/how-many-users-does-linux-support-being-logged-in-at-the-same-time-via-ssh)  
[资料来源2 - Solution to modify](https://www.cyberciti.biz/tips/howto-linux-increase-pty-session.html)

Maximum number of users on Linux : 
**65.000 for 2.4 kernels, and 4 billion for 2.6 kernels.**
[资料来源1](http://www.linuxquestions.org/questions/linux-newbie-8/what%27s-the-maximum-number-of-users-on-linux-258198/) 
[资料来源2](http://serverfault.com/questions/201136/maximum-number-of-users-on-linux) 

Maximum number of  groups on Linux : 2.6 kernels ,  65000

## 4.How much hard disk space NEED
Maybe people here have other own things like working, and playing computer games or dating . So it will write about 5000 chars during 10 days . 

The result is that if we assume that a novel has 5.2 million chinese words(maybe some of these words are different version of same chapters) , we need about **100 days**  to finish a novel by  **one hundred** people. Assuming that there will be 10000 people joing this web site and writing something sometimes, it will be **create 300 novels in a year**. 

10 Megabytes have about 5.2 million chinese words. In a year,it needs 3000 Megabytes, meaning 3GB.

## 5. Web View Design Draft(Updating)
[Design By Fluidui](https://www.fluidui.com/editor/live/)

## 6. Use Git By Python(Updating)
The process of git server use:   
[link1](https://www.linux.com/learn/how-run-your-own-git-server) OR [link2](http://toyroom.bruceli.net/tw/2011/02/04/install-git-server-on-ubuntu-linux.html)
On git server, we can put repository under this user's home folder , named ' system give name and must not repeat AND it will be restore in database'.
Crete repository : Every time Need to modify   repository name in commands  ,according by user gave.
Crete repository & Other operations : need verify user's identity and permisstion before logging in git server.

Git Server Commands : 
```
su
yum install git-core
groupadd git
useradd -g/G  git  "username"
passwd  "user login name"(this name must be single in database)
input "user's gave password" , press Enter
input "user's gave password" , press Enter
su "username"
cd ~

mkdir -p  /home/"username"/repository name.git
cd /home/"username"/repository name.git
git init --bare
```

Web Server Commands:
```
ssh-keygen -t rsa
cat ~/.ssh/id_rsa.pub | ssh git@remote-server "mkdir -p ~/.ssh && cat >>  ~/.ssh/authorized_keys"
```

Other Commands:





