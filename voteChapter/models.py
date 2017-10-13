#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from tool.tools import createId
from time import localtime,strftime
# from author.models import author
from book.models import book
from book.models import reader

# Create your models here.
class voteChapter(models.Model):
    class Meta:
        app_label = "voteChapter"
        db_table = 'voteChapter'

    id = models.CharField(max_length=50,primary_key=True)
    idReader_id = models.CharField(max_length=20)
    idVersion = models.CharField(max_length=50)
    rating = models.FloatField()
    createTime = models.DateTimeField()
    modifyTime = models.DateTimeField()

    @classmethod
    def getValue(self, idReaderArg, idVersionArg, returnArg):
        try:
            obj = self.objects.get(idReader_id=idReaderArg, idVersion_id = idVersionArg)
            if returnArg == "id":
                return True, 180000, obj.id
            # elif returnArg == "idReader":
            #     return True, 180000, obj.name
            # elif returnArg == "idVersion":
            #     return True, 180000, obj.fileName
            elif returnArg == "rating":
                return True, 180000, obj.rating
            elif returnArg == "createTime":
                return True, 180000, obj.createTime
            elif returnArg == "modifyTime":
                return True, 180000, obj.modifyTime
            elif returnArg == "all":
                return True, 180000, obj
            else:
                return False, 180001, "錯誤 : getValue　讀取 voteChapter 表錯誤。voteChapter 表中不存在該屬性，returnArg錯誤。"
        except self.DoesNotExist:
                return False, 180002, "錯誤 : getValue　讀取 voteChapter 表錯誤。voteChapter 表不存在該數據。"
        except Exception as e:
                return False, 180003, str(e)

    @classmethod
    def getAllByIdReader(self, idReaderArg):
        try:
            obj = self.objects.all().filter(idReader_id=idReaderArg)
            return True, 180100, obj
        except self.DoesNotExist:
            return False, 180101, "錯誤: getAllByIdReader 讀取 voteChapter 表錯誤。"
        except Exception as e:
            return False, 180102, str(e)

    @classmethod
    def add(self, idReaderArg, idVersionArg, ratingArg):

        try:
            nowTime = strftime("%Y-%m-%d %H:%M:%S", localtime())
            idVal = createId(50, idReaderArg + idVersionArg + str(ratingArg))

            obj = self(id=idVal, idReader_id=idReaderArg, idVersion = idVersionArg, rating = ratingArg, createTime=nowTime, modifyTime=nowTime)
            obj.save()
            return True,180200, ""
        except Exception as e:
            print str(e)
            return False,180201, str(e)

    @classmethod
    def deleteObj(self, idArg):
        try:
            obj = self.objects.get(id=idArg)
            obj.delete()
            return True,180300, ""
        except self.DoesNotExist:
            return False, 180301, "deleteObj 讀取 voteChapter 表錯誤"
        except Exception as e:
            return False,180302, str(e)
