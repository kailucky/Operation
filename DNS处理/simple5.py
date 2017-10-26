'''
    大部分的DNS解析都是一个域名对应一个IP地址，但是通过DNS轮询技术可以做到
一个域名对应多个IP，从而实现最简单且高效的负载均衡，此方案的弊端是目标主机
不可用时无法被自动剔除，因此做好业务主机的服务可用性监控至关重要。
    本方案通过分析当前域名的解析IP，再结合服务端口探测来实现自动监控，在域
名解析中添加、删除IP时，无需对监控脚本进行更改。
    此脚本放到crontab中定时运行，再结合告警程序，基于域名轮循的业务监控即可
完成。
1.步骤
1）实现域名的解析，获取域名所有的A记录解析IP列表
2）对IP列表进行HTTP级别的探测
'''
#!/usr/bin/python

import dns.resolver
import os
import httplib

iplist=[]    #定义域名IP列表变量
appdomain="www.google.com.hk"    #定义业务域名

def get_iplist(domain=""):    #域名解析函数，解析成功IP将追加到iplist
    try:
        A = dns.resolver.query(domain, 'A')    #解析A记录类型
    except Exception,e:
        print "dns resolver error:"+str(e)
        return
    for i in A.response.answer:
        for j in i.items:
            iplist.append(j.address)    #追加到iplist
    return True

def checkip(ip):
    checkurl=ip+":80"
    getcontent=""
    httplib.socket.setdefaulttimeout(5)    #定义http连接超时时间(5秒)
    conn=httplib.HTTPConnection(checkurl)    #创建http连接对象

    try:
        conn.request("GET", "/",headers = {"Host": appdomain})  #发起URL请求，添加host主机头
        r=conn.getresponse()
        getcontent =r.read(15)   #获取URL页面前15个字符，以便做可用性校验
    finally:
        if getcontent=="<!doctype html>":  #监控URL页的内容一般是事先定义好，比如“HTTP200”等
            print ip+" [OK]"
        else:
            print ip+" [Error]"    #此处可放告警程序，可以是邮件、短信通知

if __name__=="__main__":
    if get_iplist(appdomain) and len(iplist)>0:    #条件：域名解析正确且至少要返回一个IP
        for ip in iplist:
            checkip(ip)
    else:
        print "dns resolver error."
