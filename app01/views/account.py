from django.shortcuts import render,redirect,HttpResponse
from django import forms
from app01.utils.bootstrap import BootStrapForm
from app01.utils.encrypt import md5
from app01.models import Admin
from app01.utils.code import check_code
from io import BytesIO
class LoginForm(BootStrapForm):
    username=forms.CharField(
        label='用户名',
        widget=forms.TextInput()
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(render_value=True)
    )
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput()
    )

    def clean_password(self):
        pwd=self.cleaned_data.get("password")
        return md5(pwd)

def login(request):
    if request.method=='GET':
        form=LoginForm()
        return render(request,'login.html',{"form":form})
    form=LoginForm(data=request.POST)
    if form.is_valid():
        user_input_code=form.cleaned_data.pop('code')
        code=request.session.get('img_code','')
        if user_input_code.upper()!=code:
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {"form": form})
        admin_object=Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password","用户名或密码错误")
            return render(request, 'login.html', {"form": form})
        request.session['info']={"id":admin_object.id,"username":admin_object.username}
        request.session.set_expiry(60*60*24*7)
        return redirect('/admin/list/')
    return render(request, 'login.html', {"form": form})

def logout(request):
    request.session.clear()
    return redirect('/login/')

def image_code(request):
    img,code_string=check_code()
    request.session['img_code'] = code_string
    # 给session设置60s超时
    request.session.set_expiry(60)
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())
