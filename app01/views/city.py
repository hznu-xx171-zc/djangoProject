from django.shortcuts import render,redirect
from app01.models import City
from app01.utils.bootstrap import BootStrapModelForm
def city_list(request):
    queryset=City.objects.all()
    return render(request,'city_list.html',{'queryset':queryset})

class UpModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['img']
    class Meta:
        model=City
        fields='__all__'
def city_add(request):
    if request.method=='GET':
        form=UpModelForm()
        return render(request,'upload_form.html',{'form':form,'title': '新建城市'})
    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect('/city/list/')
    return render(request, 'upload_form.html', {'form': form, 'title': '新建城市'})