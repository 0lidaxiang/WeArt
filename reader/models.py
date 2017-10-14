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
    # def getAll(self, amount):
    #     try:
    #         if amount == 0:
    #             obj = self.objects.all()[:amount]
    #             return True, 110100, obj
    #         elif amount >= 0:
    #             obj = self.objects.all()[:amount]
    #             return True, 110100, obj
    #         else:
    #             obj = self.objects.all()
    #             return True, 110100, obj
    #     except self.DoesNotExist:
    #             return False, 110102, "reader 表不存在該數據"
    #     except Exception as e:
    #             return False, 110103, str(e)

    @classmethod
    def getValueById(self, idReaderArg, returnArg):
        try:
            obj = self.objects.get(id=idReaderArg)
            if returnArg == "id":
                return True, 110000, obj.id
            elif returnArg == "name":
                return True, 110000, obj.name
            elif returnArg == "passwd":
                return True, 110000, obj.passwd
            elif returnArg == "email":
                return True, 110000, obj.email
            elif returnArg == "status":
                return True, 110000, obj.status
            elif returnArg == "createTime":
                return True, 110000, obj.createTime
            elif returnArg == "all":
                return True, 110000, obj
            else:
                return False, 110001, "reader 表中不存在該屬性，returnArg 錯誤"
        except self.DoesNotExist:
                return False, 110002, "reader 表不存在該數據"
        except Exception as e:
                return False, 110003, str(e)

    @classmethod
    def getValueByEmail(self, emailArg, returnArg):
        try:
            obj = self.objects.get(email=emailArg)
            if returnArg == "id":
                return True, 110000, obj.id
            elif returnArg == "name":
                return True, 110000, obj.name
            elif returnArg == "passwd":
                return True, 110000, obj.passwd
            elif returnArg == "email":
                return True, 110000, obj.email
            elif returnArg == "status":
                return True, 110000, obj.status
            elif returnArg == "createTime":
                return True, 110000, obj.createTime
            elif returnArg == "all":
                return True, 110000, obj
            else:
                return False, 110001, "reader 表中不存在該屬性，returnArg 錯誤"
        except self.DoesNotExist:
                return False, 110002, "reader 表不存在該數據"
        except Exception as e:
                return False, 110003, str(e)

    @classmethod
    def add(self, idArg, readerNameArg, passwdArg, emailArg, statusArg, createTimeArg):
        try:
            obj = self(id=idArg, name=readerNameArg, passwd = passwdArg, email=emailArg, status = statusArg,  createTime=createTimeArg)
            obj.save()
            return True,110100, idArg
        except Exception as e:
            return False,110101, str(e)

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
                return False, 110301, "modify 讀取 reader 表錯誤"

            return True,110300, ""
        except self.DoesNotExist:
            return False, 110302, "modify 讀取 reader 表錯誤"
        except Exception as e:
            print str(e)
            return False,110303, str(e)

    @classmethod
    def deleteObj(self, argName, value):
        try:
            if argName == "id":
                obj = self.objects.get(id = value)
            elif argName == "name":
                obj = self.objects.get(name = value)
            elif argName == "email":
                obj = self.objects.get(email = value)

            obj.delete()
            return True,110200, ""
        except self.DoesNotExist:
            return False, 110201, "delete reader by | " + argName + " : " + value + " | 表錯誤"
        except Exception as e:
            return False, 110202, str(e)
