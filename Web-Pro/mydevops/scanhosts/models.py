#-*- coding:utf-8 -*-#
from django.db import models


class UserIPInfo(models.Model):
    ip = models.CharField(max_length=40, default='', verbose_name='ip地址', null=True)
    time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name = '用户访问地址信息表'
        verbose_name_plural = verbose_name
        db_table = 'useripinfo'


class BrowseInfo(models.Model):
    useragent = models.CharField(max_length=100, default='', verbose_name='用户浏览器agent信息', null=True)


    class Meta:
        verbose_name = '用户浏览器信息表'
        verbose_name_plural = verbose_name
        db_table = 'browseinfo'

# Create your models here.
# 扫描后资产设备基础信息表
class HostLoginInof(models.Model):
    TYPE_CHIOCE = (
        ('0', 'kvm'),
        ('1', 'docker'),
        ('2', 'vmx'),
    )
    ip = models.CharField(max_length=64, null=False, verbose_name="主机IP信息")
    ssh_port = models.CharField(max_length=32, null=True, verbose_name="ssh登录的端口")
    ssh_user = models.CharField(max_length=32, null=True, verbose_name="ssh登录的用户")
    ssh_passwd = models.CharField(max_length=64, null=True, verbose_name="ssh登录的用户", default="")
    ssh_rsa = models.CharField(max_length=64, null=True, verbose_name="登录使用的私钥", default="")
    rsa_pass = models.CharField(max_length=64, null=True, verbose_name="私钥的秘药", default="")
    system_ver = models.CharField(max_length=256, null=True, verbose_name="操作系统版本", default="")
    hostname = models.CharField(max_length=256, null=True, verbose_name="操作系统主机名", default="")
    ssh_status = models.IntegerField(verbose_name="0-登录失败,1-登录成功", default=0)
    ssh_type = models.IntegerField(verbose_name="1-rsa登录,2-dsa登录,3-普通用户rsa登录,4-docker成功,5-docker无法登录", default=0)
    mac_address = models.CharField(max_length=512, verbose_name="mac地址列表", default="")
    sn = models.CharField(max_length=256, verbose_name="SN－主机的唯一标示", default="")
    machine_type = models.CharField(max_length=256, verbose_name="机器的类型 1=物理服务器,2=虚拟资产,3=网络设备 0=其他类型(未知)", default="")
    sn_key = models.CharField(max_length=256, verbose_name="唯一设备ID", default="")
    host_type = models.CharField(max_length=256, verbose_name="虚拟机上宿主机的类型", default="", null=True)

    class Meta:
        verbose_name = '初始化扫描信息表'
        verbose_name_plural = verbose_name
        db_table = 'hostloginfo'
