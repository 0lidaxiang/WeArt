#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
class reader(models.Model):
    class Meta:
        app_label = "reader"
        db_table = 'reader'
    id = models.CharField(max_length=20,primary_key=True)
    name = models.CharField(max_length=100)
    passwd = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    createTime = models.DateTimeField(max_length=50)

    @classmethod
    def modifyObj(self, idReaderArg, argName, value):
        try:
            obj = self.objects.get(id=idReaderArg)
            if argName == "name":
                obj.name = value;
                obj.save()
            elif argName == "passwd":
                obj.passwd = value;
                obj.save()
            elif argName == "status":
                obj.status = value;
                obj.save()
            else:
                return False, 130301, "modify 讀取 reader 表錯誤"

            return True,130300, ""
        except self.DoesNotExist:
            return False, 130302, "modify 讀取 reader 表錯誤"
        except Exception as e:
            print str(e)
            return False,130303, str(e)
