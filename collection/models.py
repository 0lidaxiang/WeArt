#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from tool.tools import createId
from time import localtime,strftime
# from author.models import author
from book.models import book
from book.models import reader

# Create your models here.
class collection(models.Model):
    class Meta:
        app_label = "collection"
        db_table = 'collection'

    id = models.CharField(max_length=30,primary_key=True)
    idReader = models.ForeignKey(reader)  # in database,this variable is named "idReader_id"
    idBook = models.ForeignKey(book)  # in database,this variable is named "idBook_id"
    createTime = models.DateTimeField(max_length=50)

    @classmethod
    def getValue(self, idReader, returnArg):
        try:
            obj = self.objects.get(idBook_id=bookIdArg)
            if returnArg == "id":
                return True, 170000, obj.id
            elif returnArg == "idReader":
                return True, 170000, obj.name
            elif returnArg == "idBook":
                return True, 170000, obj.fileName
            elif returnArg == "createTime":
                return True, 170000, obj.chapterOrder
            else:
                return False, 170001, "錯誤 : getValue　讀取 collection 表錯誤。collection 表中不存在該屬性，returnArg錯誤。"
        except self.DoesNotExist:
                return False, 170002, "錯誤 : getValue　讀取 collection 表錯誤。collection 表不存在該數據。"
        except Exception as e:
                return False, 170003, str(e)

    @classmethod
    def getAll(self, idReaderArg):
        try:
            obj = self.objects.all().filter(idReader_id=idReaderArg)
            return True, 170100, obj
        except self.DoesNotExist:
            return False, 170101, "錯誤: getAll 讀取 collection 表錯誤。"
        except Exception as e:
            return False, 170102, str(e)

    @classmethod
    def add(self, idReader_id, idBook_id):

        try:
            nowTime = strftime("%Y-%m-%d %H:%M:%S", localtime())
            idVal = createId(20, idReader_id + idBook_id)

            obj = self(id=idVal, idReader_id=idReader_id, idBook_id = idBook_id, createTime=nowTime)
            obj.save()
            return True,170200, ""
        except Exception as e:
            print str(e)
            return False,170201, str(e)

    @classmethod
    def deleteObj(self, idArg, idReaderArg):
        try:
            obj = self.objects.get(id=idArg)
            if obj.idReader_id == idReaderArg:
                obj.delete()
                return True,170300, ""
            else:
                return True,170301, "錯誤：　您沒有權限刪除該收藏記錄！"

        except self.DoesNotExist:
            return False, 170302, "錯誤: delete 讀取 collection 表錯誤。"
        except Exception as e:
            return False,170303, str(e)
