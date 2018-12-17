
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework import generics
from django.contrib.auth.models import User

import uuid
import json
from PIL import Image

from train.models import UploadRecord, ImageVertor
from train.serializers import UploadRecordSerializer, ImageVertorSerializer
from train.precheck import PreImage
from train.PQmodel import ProductQuantization
from train.faceCom import SamePerson

# 模型预加载
# 0 人脸检索
PREDEAL = PreImage()

# 1 向量搜索
PQC = ProductQuantization(8,16,4)
PQC.loadModel('train/model/pqt/')

# 2 相似度比较
SP = SamePerson()

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')

def upload_view(request):
	return render(request, 'upload.html')

class UploadRecordAPI(generics.CreateAPIView):
    """ 图片上传API """

    queryset = UploadRecord.objects.all()
    serializer_class = UploadRecordSerializer

    def __init__(self,**args):
        super(UploadRecordAPI, self).__init__(**args)
        self.predeal = PREDEAL

    def create(self, request):
        imagelist = request.FILES.getlist('file[]')
        username = request.POST.get('username')
        if imagelist and username:
            checklist = [self.predeal.faceCheck(image) for image in imagelist]
            if all([item[2] for item in checklist]):
                arraylist = [self.predeal.faceVec(image_new, shape) for image_new, shape, hasface in checklist]
                close, cl = self.predeal.closeCheck(arraylist)
                if close:
                    user = User.objects.get_or_create(username=username)
                    for image, array in zip(imagelist, arraylist):
                        #计算code
                        veccode = PQC.fit(array)
                        vecjson = json.dumps({'params': list(array)})

                        # 保存数据
                        uuids = uuid.uuid4().hex
                        urfile = UploadRecord(user=user[0], uuid=uuids,image=image)
                        urfile.save()
                        imgver = ImageVertor(user=user[0], uuid=uuids, vecjson=vecjson, vectype='dlib-128', veccode=veccode)
                        imgver.save()

                    return JsonResponse({'info': 'user register success'}, status=200)
                else:
                    nosame = ','.join([str(x) for x in cl])
                    return JsonResponse({'info': 'not same faces!({})'.format(nosame)}, status=200)
            else:
                noface = ','.join([str(i) for i, item in enumerate(checklist) if not item[2]])
                return JsonResponse({'info': 'not find faces!({})'.format(noface)}, status=200)
        else:
            return JsonResponse({'info': 'file none'}, status=200)


class AddVertorAPI(generics.CreateAPIView):
    """ 图片向量API """

    queryset = ImageVertor.objects.all()
    serializer_class = ImageVertorSerializer

    def create(self, request):
        username = request.POST.get('username')
        uuid = request.POST.get('uuid')
        vecjson = request.POST.get('vecjson')
        vectype = request.POST.get('vectype')
        veccode = request.POST.get('veccode')
        if username and uuid and vecjson and vectype and veccode:

            user = User.objects.get_or_create(username=username)
            imgver = ImageVertor(user=user[0], uuid=uuid, vecjson=vecjson, vectype=vectype, veccode=veccode)
            imgver.save()

            return JsonResponse({'info': 'record upload success'}, status=200)
        else:
            return JsonResponse({'info': 'params not correct!'}, status=200)

class ImageLoginApi(generics.CreateAPIView):
    """ 头像登录API """

    queryset = ImageVertor.objects.all()
    serializer_class = ImageVertorSerializer

    def __init__(self,**args):
        super(ImageLoginApi, self).__init__(**args)
        self.predeal = PREDEAL

    def create(self, request):
        image = request.FILES.get('img')
        if image:
            # img = Image.open(image)
            # img.save('temp.png')
            img, shape, hasface = self.predeal.faceCheck(image)
            if hasface:
                img_arr = self.predeal.faceVec(img, shape)
                veccode = PQC.query(img_arr, 'adc')
                vercodelist = [x[0] for x in veccode]
                waitvers = ImageVertor.objects.filter(veccode__in=vercodelist)
                datalist = [(item.user,eval(item.vecjson)['params']) for item in waitvers]
                # print([item[0] for item in datalist])
                if datalist:
                    who = SP.isWho(img_arr, datalist)
                    if who is None:
                        with open('datalog.txt', 'a') as f:
                            f.write('1, I dont know who you are!\n')
                        return JsonResponse({'info': 'I dont know who you are!'}, status=200)
                    else:
                        with open('datalog.txt', 'a') as f:
                            f.write('1, {}\n'.format(who.username))
                        return JsonResponse({'info': who.username}, status=200)
                else:
                    with open('datalog.txt', 'a') as f:
                        f.write('1, who you are!\n')
                    return JsonResponse({'info': 'who you are!'}, status=200)
            else:
                return JsonResponse({'info': 'have no face!'}, status=200)
        else:
            return JsonResponse({'info': 'file none!'}, status=200)

