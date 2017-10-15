#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from reader.models import reader
from tool.tools import createId
from time import localtime, strftime

# Create your models here.
class author(models.Model):
    class Meta:
        app_label = "author"
        db_table = 'author'
        verbose_name = "作者"
        verbose_name_plural = "作者列表管理"

    STATUS_CHOICES = (
        ("active", 'active'),
        ("inactive", 'inactive'),
        ("locked", 'locked'),
    )

    id = models.CharField("編號", max_length=20,primary_key=True,blank=False,null=False)
    status = models.CharField("賬號狀態", max_length=20,blank=False,null=False, choices = STATUS_CHOICES)
    createTime = models.DateTimeField("申請時間", max_length=50,blank=False,null=False)
    idReader_id = models.CharField("讀者編號", max_length=20,blank=False,null=False,unique=True)

    def authorStatus(self):
        return self.status == 'active'
    authorStatus.boolean = True
    authorStatus.short_description = "允許寫作"

    def accountCreateTime(self):
        return self.createTime.strftime('%Y-%m-%d %H:%M:%S')
    accountCreateTime.short_description = '申請時間'

    @classmethod
    def isExist(self, idReaderArg):
        try:
            result = self.objects.get(idReader_id=idReaderArg)
            return True
        except self.DoesNotExist:
            return False

    @classmethod
    def getId(self, idReaderArg):
        try:
            authorObj = self.objects.get(idReader_id=idReaderArg)
            return authorObj.id
        except self.DoesNotExist:
            return ""

    # @classmethod
    # def getPasswd(self, idArg):
    #     try:
    #         authorObj = self.objects.get(id=idArg)
    #         return authorObj.passwd
    #     except self.DoesNotExist:
    #         return ""

    @classmethod
    def getStatus(self, idReaderArg):
        try:
            authorObj = self.objects.get(idReader_id=idReaderArg)
            return authorObj.status
        except self.DoesNotExist:
            return ""

    @classmethod
    def addAuthor(self, idReaderArg):
        try:
            nowTime = strftime("%Y-%m-%d %H:%M:%S", localtime())
            # readObj = reader.objects.get(id=idReaderArg)
            idVal = createId(15, idReaderArg)
            # passwdVal = createId(15, idVal)
            authorObj = self(id=idVal, status = "active", idReader_id = idReaderArg, createTime=nowTime)
            # authorObj = self(id=idVal,passwd=passwdVal, status = "active", idReader_id = idReaderArg, createTime=nowTime)
            authorObj.save()
            return True
        except Exception as e:
            print e
            return False

    @classmethod
    def deleteRecord(self, idReaderArg):
        try:
            authorObj = self.objects.get(idReader_id=idReaderArg)
            authorObj.delete()
            return True
        except self.DoesNotExist:
            return False

    @classmethod
    def modifyStatus(self, idReaderArg, statusArg):
        try:
            authorObj = self.objects.get(idReader_id=idReaderArg)
            authorObj.status = statusArg
            authorObj.save()
            return True
        except self.DoesNotExist:
            return False
