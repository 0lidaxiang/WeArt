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
    idChapter = models.ForeignKey(chapter) # in database,this variable is named "idChapter_id"
    vote = models.IntegerField(max_length=11)
    socre = models.IntegerField(max_length=11)
    idAuthor = models.ForeignKey(reader)  # in database,this variable is named "idAuthor_id"
    createTime = models.DateTimeField(max_length=50)
    modifyTime = models.DateTimeField(max_length=50)

    @classmethod
    def getValuesByIdChapter(self, idChapterArg, idAuthorArg, returnArg):
        try:
            obj = self.objects.get(idChapter_id=idChapterArg, idAuthor_id=idAuthorArg)

            if returnArg == "id":
                return True, 160000, obj.id
            elif returnArg == "idChapter":
                return True, 160000, obj.idChapter
            elif returnArg == "vote":
                return True, 160000, obj.vote
            elif returnArg == "socre":
                return True, 160000, obj.socre
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
    def add(self, idChapter, vote, socre, idAuthor):
        try:
            nowTime = strftime("%Y-%m-%d %H:%M:%S", localtime())
            idVal = createId(50, idChapter)
            obj = self(id=idVal, idChapter_id=idChapter, vote = vote, socre=socre, idAuthor_id = idAuthor, createTime=nowTime, modifyTime=nowTime,)
            obj.save()
            return True,160101, ""
        except Exception as e:
            return False,160102, str(e)
