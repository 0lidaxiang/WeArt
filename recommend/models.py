#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
class recommend(models.Model):
    class Meta:
        app_label = "recommend"
        db_table = 'recommend'
        verbose_name = "書籍推薦"
        verbose_name_plural = "書籍推薦列表管理"

    STATUS_CHOICES = (
        ("allowed", 'allowed'),
        ("abuse", 'abuse'),
        ("locked", 'locked'),
    )

    id = models.AutoField(primary_key=True)
    idBook_id = models.CharField("書籍Id", max_length=20,blank=False,null=False) # a book can be added much times and we can analysis this history data
    status = models.CharField("狀態", max_length=20,blank=False,null=False, choices = STATUS_CHOICES)
    createTime = models.DateTimeField("申請時間", auto_now=False, auto_now_add=True, max_length=50,blank=False,null=False)
    # modifyTime = models.DateTimeField("修改時間", auto_now=True, auto_now_add=False, max_length=50,blank=False,null=False)

    def accountStatus(self):
        return self.status == 'allowed'
    accountStatus.boolean = True
    accountStatus.short_description = "允許展示"

    def accountCreateTime(self):
        return self.createTime.strftime('%Y-%m-%d %H:%M:%S')
    accountCreateTime.short_description = '申請時間'

    @classmethod
    def getValueByStatus(self, statusArg, returnArg):
        try:
            obj = self.objects.get(status=statusArg)
            if returnArg == "id":
                return True, 190000, obj.id
            elif returnArg == "idBook_id":
                return True, 190000, obj.idBook_id
            elif returnArg == "createTime":
                return True, 190000, obj.createTime
            # elif returnArg == "modifyTime":
                # return True, 190000, obj.modifyTime
            else:
                return False, 190001, "recommend 表中不存在該屬性，returnArg錯誤。"
        except self.DoesNotExist:
                return False, 190002, "recommend 表不存在該數據。"
        except Exception as e:
                return False, 190003, str(e)

    @classmethod
    def getAll(self, amount):
        try:
            # get all data when amount=0
            if amount == 0:
                obj = self.objects.all()
                return True, 190100, obj

            obj = self.objects.all()[:amount]
            return True, 190100, obj
        except self.DoesNotExist:
            return False, 190101, "recommend 表不存在該數值"
        except Exception as e:
            return False, 191202, str(e)
