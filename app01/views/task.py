from  django.shortcuts import render,HttpResponse
from  django.views.decorators.csrf import csrf_exempt
from  django.http import JsonResponse
from app01.utils.bootstrap import BootStrapModelForm
from app01.models import Task
from django import forms
from app01.utils.pagination import Pagination

@csrf_exempt
def task_ajax(request):
    print(request.POST)
    data_dict={"status":True,'data':[11,22,33,44]}
    return JsonResponse(data_dict)

class TaskModelForm(BootStrapModelForm):
    class Meta:
        model=Task
        fields="__all__"
        widgets={
            "detail":forms.TextInput
        }

def task_list(request):
    queryset=Task.objects.all().order_by('-id')
    page_object=Pagination(request,queryset)
    form=TaskModelForm()
    context={
        'form':form,
        "queryset":page_object.page_queryset,  #分完页的数据
        'page_string':page_object.html() ,       #生成页码
    }
    return render(request,"task_list.html",context)

@csrf_exempt
def task_add(request):
    form=TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict={"status":True}
        return JsonResponse(data_dict)
    data_dict={"status":False,'error':form.errors}
    return JsonResponse(data_dict)



