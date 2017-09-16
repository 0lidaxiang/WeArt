#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from tool.tools import createId
from time import localtime,strftime
from author.models import author

# Create your models here.
class book(models.Model):
    class Meta:
        app_label = "book"
        db_table = 'book'

    id = models.CharField(max_length=20,primary_key=True)
    name = models.CharField(max_length=100)
    remoteIP = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    chapterCount = models.IntegerField(max_length=11)
    status = models.CharField(max_length=20)
    createTime = models.DateTimeField(max_length=50)
    idAuthor = models.ForeignKey(author)

    @classmethod
    def getIdByNameAndAuthor(self, nameArg, idAuthorArg):
        try:
            obj = self.objects.get(name = nameArg, idAuthor_id = idAuthorArg)
            return True, 130003, obj.id
        except self.DoesNotExist:
            return False, 130004, "錯誤: getIdByNameAndAuthor 讀取book表錯誤。"
        except Exception as e:
            return False, 130005, str(e)
    @classmethod
    def getValue(self, idBookArg, returnArg):
        try:
            obj = self.objects.get(id=idBookArg)
            if returnArg == "id":
                return True, obj.id
            elif returnArg == "name":
                return True, obj.name
            elif returnArg == "remoteIP":
                return True, obj.remoteIP
            elif returnArg == "location":
                return True, obj.location
            elif returnArg == "status":
                return True, obj.status
            elif returnArg == "chapterCount":
                return True, obj.chapterCount
            elif returnArg == "createTime":
                return True, obj.createTime
            elif returnArg == "idAuthor_id":
                return True, obj.idAuthor_id
            else:
                return False, "錯誤1001: book表中不存在該屬性，returnArg錯誤。"
        except self.DoesNotExist:
                return False, "錯誤1002: 讀取book表錯誤。"

    @classmethod
    def add(self, bookName, remoteIP, location, idAuthor_id):
        try:
            nowTime = strftime("%Y-%m-%d %H:%M:%S", localtime())
            idVal = createId(20, bookName)

            obj = self(id=idVal, name=bookName, remoteIP = remoteIP, location=location, chapterCount = 0, status = "active", createTime=nowTime, idAuthor_id=idAuthor_id)
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
            elif property == "idAuthor_id":
                obj = self(id=idBookArg)
                obj.idAuthor_id = value
                obj.save(update_fields=["idAuthor_id"])
                return True, obj.idAuthor_id
            else:
                return False, "錯誤1001: book表中不存在該屬性，returnArg錯誤。"
        except self.DoesNotExist:
                return False, "錯誤1002: 讀取book表錯誤。"

    @classmethod
    def delete(self, bookIdArg):
        try:
            obj = self.objects.get(id=bookIdArg)
            obj.delete()
            return True, ""
        except Exception as e:
            return False, str(e)
