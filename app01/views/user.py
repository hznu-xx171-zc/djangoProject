from django.shortcuts import render,redirect
from app01.models import Department,UserInfo
from app01.utils.pagination import Pagination
from app01.utils.forms import UserModelForm
def user_list(request):
    queryset=UserInfo.objects.all()
    page_object = Pagination(request, queryset)
    context={
        "queryset":page_object.page_queryset,
        'page_string': page_object.html()
    }
    return render(request,'user_list.html',context)

def user_add(request):
    if request.method=='GET':
        context={
            'gender_choices':UserInfo.gender_choices,
            'depart_list':Department.objects.all(),
        }
        return render(request,'user_add.html',context)
    user=request.POST.get("user")
    password = request.POST.get("pwd")
    age=request.POST.get("age")
    account=request.POST.get("ac")
    ctime = request.POST.get("ctime")
    gender_id = request.POST.get("gd")
    depart_id = request.POST.get("dp")
    UserInfo.objects.create(name=user,password=password,age=age,account=account,create_time=ctime,gender=gender_id,depart_id=depart_id)
    return redirect('/user/list')

def user_model_form_add(request):
    if request.method=="GET":
        form=UserModelForm()
        return render(request,"user_model_form_add.html",{"form":form})
    form=UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, "user_model_form_add.html", {"form": form})

def user_edit(request,nid):
    row_object = UserInfo.objects.filter(id=nid).first()
    if request.method=="GET":
        form=UserModelForm(instance=row_object)
        return render(request,'user_edit.html',{"form":form})
    form = UserModelForm(data=request.POST,instance=row_object)
    print(form.is_valid())
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, "user_edit.html", {"form": form})

def user_delete(request,nid):
    UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')
