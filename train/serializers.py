from rest_framework import serializers

from train.models import UploadRecord, ImageVertor

class UploadRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadRecord
        fields = ('user', 'uuid', 'image', 'createDateTime')

class ImageVertorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageVertor
        fields = ('user', 'uuid', 'vecjson', 'vectype', 'veccode', 'createDateTime')

		