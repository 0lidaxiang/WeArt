#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from tool.tools import createId
from time import localtime,strftime
from chapter.models import chapter
from reader.models import reader
from book.models import book

# Create your models here.
class version(models.Model):
    class Meta:
        app_label = "version"
        db_table = 'version'

    id = models.CharField(max_length=50,primary_key=True)
    idChapter_id = models.CharField(max_length=30)
    voteCount = models.FloatField(max_length=11)
    score = models.FloatField(max_length=11)
    idAuthor_id = models.CharField(max_length=20)  
    createTime = models.DateTimeField(max_length=50)
    modifyTime = models.DateTimeField(max_length=50)

    @classmethod
    def getValueById(self, idVersion, returnArg):
        try:
            obj = self.objects.get(id=idVersion)

            if returnArg == "id":
                return True, 160400, obj.id
            elif returnArg == "idChapter":
                return True, 160400, obj.idChapter
            elif returnArg == "voteCount":
                return True, 160400, obj.voteCount
            elif returnArg == "score":
                return True, 160400, obj.score
            elif returnArg == "idAuthor":
                return True, 160400, obj.idAuthor
            elif returnArg == "createTime":
                return True, 160400, obj.createTime
            elif returnArg == "modifyTime":
                return True, 160400, obj.modifyTime
            elif returnArg == "all":
                return True, 160400, obj
            else:
                return False, 160401, "錯誤 : version 表中不存在該屬性，returnArg錯誤。"
        except self.DoesNotExist:
                return False, 160402, "錯誤 : version 表不存在該數據。"
        except Exception as e:
                return False, 160403, str(e)

    @classmethod
    def getValuesByIdChapter(self, idChapterArg, idAuthorArg, returnArg):
        try:
            obj = self.objects.get(idChapter_id=idChapterArg, idAuthor_id=idAuthorArg)

            if returnArg == "id":
                return True, 160000, obj.id
            elif returnArg == "idChapter":
                return True, 160000, obj.idChapter
            elif returnArg == "voteCount":
                return True, 160000, obj.voteCount
            elif returnArg == "score":
                return True, 160000, obj.score
            elif returnArg == "idAuthor":
                return True, 160000, obj.idAuthor
            elif returnArg == "createTime":
                return True, 160000, obj.createTime
            elif returnArg == "modifyTime":
                return True, 160000, obj.modifyTime
            else:
                return False, 160001, "錯誤 : version 表中不存在該屬性，returnArg錯誤。"
        except self.DoesNotExist:
                return False, 160002, "錯誤 : version 表不存在該數據。"
        except Exception as e:
                return False, 160003, str(e)

    @classmethod
    def getVersionsByIdChapter(self, idChapterArg):
        try:
            obj = self.objects.filter(idChapter_id=idChapterArg)
            return True, 160200, obj
        except self.DoesNotExist:
                return False, 160202, "錯誤 : version 表不存在該數據。"
        except Exception as e:
                return False, 160203, str(e)

    @classmethod
    def add(self, idChapter, voteCount, score, idAuthor):
        try:
            nowTime = strftime("%Y-%m-%d %H:%M:%S", localtime())
            idVal = createId(50, idChapter + idAuthor) # every author writeing is a version
            # idVal = createId(50, idChapter + idAuthor + nowTime) # every update is a version
            obj = self(id=idVal, idChapter_id=idChapter, voteCount = voteCount, score=score, idAuthor_id = idAuthor, createTime=nowTime, modifyTime=nowTime,)
            obj.save()
            return True,160101, ""
        except Exception as e:
            return False,160102, str(e)

    @classmethod
    # def modifyObj(self, idChapter, voteCount, score, idAuthor):
    def modifyObj(self, idVersion, argName, value):
        try:
            obj = self.objects.get(id=idVersion)
            if argName == "voteCount":
                obj.voteCount = value;
                obj.save()
            elif argName == "score":
                obj.score = value;
                obj.save()
            elif argName == "modifyTime":
                obj.modifyTime = value;
                obj.save()
            else:
                return False, 160301, "modify 讀取 reader 表錯誤"

            return True,160300, ""
        except self.DoesNotExist:
            return False, 160302, "modify 讀取 reader 表錯誤"
        except Exception as e:
            print str(e)
            return False,160303, str(e)
