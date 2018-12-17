from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def savepath(instance, fielname):
	""" 存储路径 """
	return '/'.join(['data', instance.uuid]) + '.png'

class UploadRecord(models.Model):
	""" 图片上传记录表 """

	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	uuid = models.UUIDField(verbose_name="uuid")
	image = models.ImageField(upload_to = savepath)
	createDateTime = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('createDateTime', )
		db_table = 'uploadrecord'

	def __str__(self):
		return self.uuid


class ImageVertor(models.Model):
	""" 图片向量表 """

	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	uuid = models.UUIDField(verbose_name="uuid")
	vecjson = models.TextField(blank=True, null=True, verbose_name='json')
	vectype = models.CharField(max_length=20, verbose_name='function')
	veccode = models.CharField(max_length=20, verbose_name='code')
	createDateTime = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('createDateTime', )
		db_table = 'imagevertor'

	def __str__(self):
		return self.uuid

