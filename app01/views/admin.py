from django.shortcuts import render,redirect
from app01.models import Admin
from app01.utils.pagination import Pagination
def admin_list(request):
    search_data = request.GET.get('q', '')
    data_dict = {}
    if search_data:
        data_dict['username__contains'] = search_data
    queryset=Admin.objects.filter(**data_dict)
    page_object = Pagination(request, queryset)
    context = {
        'search_data': search_data,
        "queryset": page_object.page_queryset,
        'page_string': page_object.html()
    }
    return render(request,'admin_list.html',context)

from django import  forms
from app01.utils.bootstrap import BootStrapModelForm
from django.core.exceptions import ValidationError
from app01.utils.encrypt import md5
class AdminModelForm(BootStrapModelForm):
    confirm_password=forms.CharField(label='确认密码',widget=forms.PasswordInput(render_value=True))
    class Meta:
        model=Admin
        fields=["username","password",'confirm_password']
        widgets={
            "password":forms.PasswordInput(render_value=True)
        }
    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

    def clean_confirm_password(self):
        pwd=self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm


def admin_add(request):
    title='新建管理员'
    if request.method=='GET':
        form=AdminModelForm()
        return render(request, 'change.html',{"title":title,"form":form})
    form=AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, 'change.html', {"title": title, "form": form})

class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = Admin
        fields = ["username"]


def admin_edit(request,nid):
    title = '编辑管理员'
    row_object=Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect("/admin/list/")
    if request.method=='GET':
        form=AdminEditModelForm(instance=row_object)
        return render(request, 'change.html', {"title": title, "form": form})
    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {"title": title, "form": form})

def admin_delete(request,nid):
    Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')

class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput(render_value=True))
    class Meta:
        model = Admin
        fields = ["password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }
    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        md5_pwd=md5(pwd)
        exists=Admin.objects.filter(id=self.instance.pk,password=md5_pwd).exists()
        if exists:
            raise ValidationError('密码不能与以前的相同')
        return md5_pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm

def admin_reset(request,nid):
    row_object = Admin.objects.filter(id=nid).first()
    title = '重置密码 - {}'.format(row_object.username)
    if not row_object:
        return redirect("/admin/list/")
    if request.method=='GET':
        form=AdminResetModelForm()
        return render(request, 'change.html', {"title": title, "form": form})
    form=AdminResetModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {"title": title, "form": form})