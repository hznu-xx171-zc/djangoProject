import os
from  django.shortcuts import render,HttpResponse
from  app01.models import Boss,City
def upload_list(request):
    if request.method=='GET':
        return render(request,'upload_list.html')
    file_object=request.FILES.get('avatar')
    f=open('t1.txt',mode='wb')
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()
    return HttpResponse('...')

from  django import forms
from app01.utils.bootstrap import BootStrapForm,BootStrapModelForm
from  django.conf import settings
class UpForm(BootStrapForm):
    bootstrap_exclude_fields = ['img']
    name=forms.CharField(label='姓名')
    age=forms.IntegerField(label='年龄')
    img=forms.FileField(label='头像')

def upload_form(request):
    if request.method=='GET':
        form=UpForm()
        return render(request,'upload_form.html',{'form':form,'title':'Form上传'})
    form=UpForm(data=request.POST,files=request.FILES)
    if form.is_valid():
        img_object=form.cleaned_data.get('img')
        media_path=os.path.join(settings.MEDIA_ROOT,img_object.name)
        f=open(media_path,mode='wb')
        for chunk in img_object.chunks():
            f.write(chunk)
        f.close()
        Boss.objects.create(name=form.cleaned_data.get('name'),age=form.cleaned_data.get('age'),img=media_path)
        return HttpResponse('...')
    return render(request, 'upload_form.html', {'form': form, 'title': 'Form上传'})

class UpModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['img']
    class Meta:
        model=City
        fields='__all__'

def upload_modelform(request):
    if request.method=='GET':
        form=UpModelForm()
        return render(request,'upload_form.html',{'form':form,'title': 'ModelForm上传'})
    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponse('...')
    return render(request, 'upload_form.html', {'form': form, 'title': 'ModelForm上传'})