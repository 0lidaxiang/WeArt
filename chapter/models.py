#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from tool.tools import createId
from time import gmtime,strftime
from author.models import author

# Create your models here.
class book(models.Model):
    class Meta:
        app_label = "book"
        db_table = 'book'

    id = models.CharField(max_length=20,primary_key=True)
    name = models.CharField(max_length=100)
    remoteIP = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    createTime = models.DateTimeField(max_length=50)
    idAuthor = models.ForeignKey(author)

    @classmethod
    def getValue(self, bookIdArg, returnArg):
        try:
            obj = self.objects.get(id=bookIdArg)
            if returnArg == "id":
                return obj.id
            elif returnArg == "name":
                return obj.name
            elif returnArg == "fileName":
                return obj.fileName
            elif returnArg == "chapterOrder":
                return obj.chapterOrder
            elif returnArg == "status":
                return obj.status
            elif returnArg == "createTime":
                return obj.createTime
            elif returnArg == "idAuthor_id":
                return obj.idAuthor_id
            else:
                return "fail", "錯誤1001: book表中不存在該屬性，returnArg錯誤。"
        except self.DoesNotExist:
                return "fail", "錯誤1002: 讀取book表錯誤。"

    @classmethod
    def add(self, name, remoteIP, location, idAuthor_id):
        try:
            nowTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            idVal = createId(20, name)

            obj = self(id=idVal, name=name, remoteIP = remoteIP, location=location, status = "active", createTime=nowTime, idAuthor_id=idAuthor_id)
            obj.save()
            return True, ""
        except Exception as e:
            return False, str(e)


    @classmethod
    def delete(self, bookIdArg):
        try:
            obj = self.objects.get(id=bookIdArg)
            obj.delete()
            return True, ""
        except Exception as e:
            return False, str(e)
