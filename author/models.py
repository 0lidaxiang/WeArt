from django.db import models
from reader.models import reader
from tool.tools import createId
from time import gmtime, strftime

# Create your models here.
class author(models.Model):
    class Meta:
        app_label = "author"
        db_table = 'author'

    id = models.CharField(max_length=15,primary_key=True)
    passwd = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    createTime = models.DateTimeField(max_length=50)
    idReader = models.ForeignKey(reader)

    @classmethod
    def isExist(self, idReaderArg):
        try:
            result = self.objects.get(idReader_id=idReaderArg)
            return True
        except self.DoesNotExist:
            return False

    @classmethod
    def getId(self, idReaderArg):
        try:
            authorObj = self.objects.get(idReader_id=idReaderArg)
            return authorObj.id
        except self.DoesNotExist:
            return ""

    @classmethod
    def getPasswd(self, idArg):
        try:
            authorObj = self.objects.get(id=idArg)
            return authorObj.passwd
        except self.DoesNotExist:
            return ""

    @classmethod
    def getStatus(self, idReaderArg):
        try:
            authorObj = self.objects.get(idReader_id=idReaderArg)
            return authorObj.status
        except self.DoesNotExist:
            return ""

    @classmethod
    def addAuthor(self, idReaderArg):
        try:
            nowTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            # readObj = reader.objects.get(id=idReaderArg)
            idVal = createId(15, idReaderArg)
            passwdVal = createId(15, idVal)
            authorObj = self(id=idVal,passwd=passwdVal, status = "active", idReader_id = idReaderArg, createTime=nowTime)
            authorObj.save()
            return True
        except Exception as e:
            print e
            return False

    @classmethod
    def deleteRecord(self, idReaderArg):
        try:
            authorObj = self.objects.get(idReader_id=idReaderArg)
            authorObj.delete()
            return True
        except self.DoesNotExist:
            return False

    @classmethod
    def modifyStatus(self, idReaderArg, statusArg):
        try:
            authorObj = self.objects.get(idReader_id=idReaderArg)
            authorObj.status = statusArg
            authorObj.save()
            return True
        except self.DoesNotExist:
            return False
