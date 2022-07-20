from django.shortcuts import render,redirect
from app01.models import PrettyNum
from app01.utils.pagination import Pagination
from app01.utils.forms import PrettyModelForm

def pretty_list(request):
    search_data = request.GET.get('q', '')
    data_dict = {}
    if search_data:
        data_dict['mobile__contains']=search_data
    queryset = PrettyNum.objects.filter(**data_dict).order_by("id")
    page_object=Pagination(request,queryset)
    context={
        "queryset":page_object.page_queryset,
        'search_data':search_data,
        'page_string':page_object.html()
    }
    return render(request,'pretty_list.html',context)

def pretty_add(request):
    if request.method=="GET":
        form=PrettyModelForm()
        return render(request,"pretty_add.html",{"form":form})
    form=PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, "pretty_add.html", {"form": form})

def pretty_edit(request,nid):
    row_object = PrettyNum.objects.filter(id=nid).first()
    if request.method=="GET":
        form=PrettyModelForm(instance=row_object)
        return render(request,'pretty_edit.html',{"form":form})
    form = PrettyModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, "pretty_edit.html", {"form": form})

def pretty_delete(request,nid):
    PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')