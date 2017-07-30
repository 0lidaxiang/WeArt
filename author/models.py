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
    status = models.CharField(max_length=20)
    # idReader = models.CharField(max_length=20)
    createTime = models.DateTimeField(max_length=50)
    idReader = models.ForeignKey(reader)

    @classmethod
    def isExistIdReader(self, idReaderArg):
        try:
            result = self.objects.get(idReader_id=idReaderArg)
            return True
        except self.DoesNotExist:
            return False

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
            readObj = reader.objects.get(id=idReaderArg)
            authorObj = self(id=createId(15, idReaderArg), status = "active", idReader_id = idReaderArg, createTime=nowTime)
            authorObj.save()
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
