#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from tool.tools import createId
from time import localtime,strftime
from reader.models import reader

# Create your models here.
class book(models.Model):
    class Meta:
        app_label = "book"
        db_table = 'book'
        verbose_name = "書籍"
        verbose_name_plural = "書籍列表管理"

    STATUS_CHOICES = (
        ("active", 'active'),
        ("inactive", 'inactive'),
        ("locked", 'locked'),
    )

    id = models.CharField("編號", max_length=20,primary_key=True,blank=False,null=False)
    name = models.CharField("書名", max_length=100,blank=False,null=False)
    # remoteIP = models.CharField("遠端倉庫IP", max_length=20)
    remoteIP = models.GenericIPAddressField("遠端倉庫IP",default='192.168.0.1',blank=False,null=False)
    location = models.CharField("存儲位置",  max_length=100,blank=False,null=False)
    chapterCount = models.IntegerField("章節數量",blank=False,null=False)
    status = models.CharField("書籍狀態", max_length=20,blank=False,null=False, choices = STATUS_CHOICES)
    createTime = models.DateTimeField("創建時間", max_length=50,blank=False,null=False)
    idReader_id = models.CharField("作者編號", max_length=30,blank=False,null=False)

    def accountStatus(self):
        return self.status == 'active'
    accountStatus.boolean = True
    accountStatus.short_description = "允許讀者查看"

    def accountCreateTime(self):
        return self.createTime.strftime('%Y-%m-%d %H:%M:%S')
    accountCreateTime.short_description = '申請時間'

    @classmethod
    def getIdByNameAndAuthor(self, nameArg, idReaderArg):
        try:
            obj = self.objects.get(name = nameArg, idReader_id = idReaderArg)
            return True, 130000, obj.id
        except self.DoesNotExist:
            return False, 130004, "錯誤: getIdByNameAndAuthor 讀取 book 表錯誤。"
        except Exception as e:
            return False, 130005, str(e)
    @classmethod
    def getValue(self, idBookArg, returnArg):
        try:
            obj = self.objects.get(id=idBookArg)
            if returnArg == "id":
                return True, 130000, obj.id
            elif returnArg == "name":
                return True, 130000, obj.name
            elif returnArg == "remoteIP":
                return True, 130000, obj.remoteIP
            elif returnArg == "location":
                return True, 130000, obj.location
            elif returnArg == "status":
                return True, 130000, obj.status
            elif returnArg == "chapterCount":
                return True, 130000, obj.chapterCount
            elif returnArg == "createTime":
                return True, 130000, obj.createTime
            elif returnArg == "idReader_id":
                return True, 130000, obj.idReader_id
            elif returnArg == "all":
                return True, 130000, obj
            else:
                return False, 130001, "錯誤: book 表中不存在該屬性，returnArg錯誤。"
        except self.DoesNotExist:
                return False, 130002, "錯誤: book 表不存在該數據。"
        except Exception as e:
                return False, 130003, str(e)

    @classmethod
    def add(self, bookName, remoteIP, location, idReader_id):
        try:
            nowTime = strftime("%Y-%m-%d %H:%M:%S", localtime())
            idVal = createId(20, bookName)

            obj = self(id=idVal, name=bookName, remoteIP = remoteIP, location=location, chapterCount = 0, status = "active", createTime=nowTime, idReader_id=idReader_id)
            obj.save()
            return True, idVal
        except Exception as e:
            return False, str(e)

    @classmethod
    def modify(self, idBookArg, property, value):
        try:
            obj = self.objects.get(id=idBookArg)
            if property == "id":
                obj = self(id=idBookArg)
                obj.id = value
                obj.save(update_fields=["id"])
                return True, obj.id
            elif property == "name":
                obj = self(id=idBookArg)
                obj.name = value
                obj.save(update_fields=["name"])
                return True, obj.name
            elif property == "remoteIP":
                obj = self(id=idBookArg)
                obj.remoteIP = remoteIP
                obj.save(update_fields=["remoteIP"])
                return True, obj.remoteIP
            elif property == "location":
                obj = self(id=idBookArg)
                obj.location = value
                obj.save(update_fields=["location"])
                return True, obj.location
            elif property == "status":
                obj = self(id=idBookArg)
                obj.status = value
                obj.save(update_fields=["status"])
                return True, obj.status
            elif property == "chapterCount":
                obj = self(id=idBookArg)
                obj.chapterCount = value
                obj.save(update_fields=["chapterCount"])
                return True, obj.chapterCount
            elif property == "createTime":
                obj = self(id=idBookArg)
                obj.createTime = value
                obj.save(update_fields=["createTime"])
                return True, obj.createTime
            elif property == "idReader_id":
                obj = self(id=idBookArg)
                obj.idReader_id = value
                obj.save(update_fields=["idReader_id"])
                return True, obj.idReader_id
            else:
                return False, "錯誤1001: book表中不存在該屬性，returnArg錯誤。"
        except self.DoesNotExist:
                return False, "錯誤1002: 讀取book表錯誤。"

    @classmethod
    def deleteObj(self, idBookArg):
        try:
            obj = self.objects.get(id=idBookArg)
            location = obj.location
            obj.delete()
            return True,130100, location
        except self.DoesNotExist:
            return False, 130102, "delete 讀取 book 表錯誤"
        except Exception as e:
            return False, 130103, str(e)

    @classmethod
    def getAll(self, amount):
        try:
            # get all data when amount=0
            if amount == 0:
                obj = self.objects.all()
                return True, 130200, obj

            obj = self.objects.all()[:amount]
            return True, 130200, obj
        except self.DoesNotExist:
            return False, 130201, "book 表不存在該數值"
        except Exception as e:
            return False, 130202, str(e)

    @classmethod
    def getAllByAuthor(self, idReaderArg):
        try:
            obj = self.objects.all().filter(idReader_id=idReaderArg)
            return True, 130300, obj
        except self.DoesNotExist:
            return False, 130301, "book 表不存在該數值"
        except Exception as e:
            return False, 130302, str(e)
