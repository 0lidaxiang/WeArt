#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from tool.tools import createId
from time import localtime,strftime
# from author.models import author
from book.models import book

# Create your models here.
class chapter(models.Model):
    class Meta:
        app_label = "chapter"
        db_table = 'chapter'

    id = models.CharField(max_length=30,primary_key=True,blank=False,null=False)
    name = models.CharField(max_length=100,blank=False,null=False)
    fileName = models.CharField(max_length=32,blank=False,null=False)
    chapterOrder = models.CharField(max_length=20,blank=False,null=False)
    status = models.CharField(max_length=20,blank=False,null=False)
    createTime = models.DateTimeField(max_length=50,blank=False,null=False)
    idBook_id = models.CharField(max_length=20,blank=False,null=False)

    @classmethod
    def getValueByIdBookAndOrder(self, bookIdArg, orderArg, returnArg):
        try:
            obj = self.objects.get(idBook_id=bookIdArg, chapterOrder=orderArg)
            if returnArg == "id":
                return True, 140000, obj.id
            elif returnArg == "name":
                return True, 140000, obj.name
            elif returnArg == "fileName":
                return True, 140000, obj.fileName
            elif returnArg == "chapterOrder":
                return True, 140000, obj.chapterOrder
            elif returnArg == "status":
                return True, 140000, obj.status
            elif returnArg == "createTime":
                return True, 140000, obj.createTime
            elif returnArg == "idReader_id":
                return True, 140000, obj.idReader_id
            else:
                return False, 140003, "錯誤 : chapter 表中不存在該屬性，returnArg錯誤。"
        except self.DoesNotExist:
                return False, 140004, "錯誤 : chapter 表不存在該數據。"
        except Exception as e:
                return False, 140005, str(e)

    @classmethod
    def add(self, name, fileName, chapterOrder, idBook_id):
        try:
            nowTime = strftime("%Y-%m-%d %H:%M:%S", localtime())
            idVal = createId(20, name)

            obj = self(id=idVal, name=name, fileName = fileName, chapterOrder=chapterOrder, status = "active", createTime=nowTime, idBook_id=idBook_id)
            obj.save()
            return True, str(idVal)
        except Exception as e:
            return False, str(e)

    # @classmethod
    # def modify(self, name, remoteIP, location, idReader_id):
    #     try:
    #         nowTime = strftime("%Y-%m-%d %H:%M:%S", localtime())
    #         idVal = createId(20, name)
    #
    #         obj = self(id=idVal, name=name, remoteIP = remoteIP, location=location, status = "active", createTime=nowTime, idReader_id=idReader_id)
    #         obj.save()
    #         return True, ""
    #     except Exception as e:
    #         return False, str(e)

    @classmethod
    def delete(self, bookIdArg):
        try:
            obj = self.objects.get(id=bookIdArg)
            obj.delete()
            return True, ""
        except Exception as e:
            return False, str(e)

    @classmethod
    def getAll(self, idBookArg):
        try:
            obj = self.objects.all().filter(idBook_id=idBookArg)
            return True, 140006, obj
        except self.DoesNotExist:
            return False, 140007, "錯誤: getAll 讀取 chapter 表錯誤。"
        except Exception as e:
            return False, 140008, str(e)
