import random
from datetime import  datetime
from  django.shortcuts import render
from  django.http import JsonResponse
from  app01.utils.bootstrap import BootStrapModelForm
from  app01.models import Order
from  django.views.decorators.csrf import csrf_exempt
from app01.utils.pagination import Pagination

class OrderModelForm(BootStrapModelForm):
    class Meta:
        model=Order
        exclude=['oid','admin']
def order_list(request):
    queryset=Order.objects.all().order_by('-id')
    page_object = Pagination(request, queryset)
    form = OrderModelForm()
    context = {
        'form': form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        'page_string': page_object.html()  # 生成页码
    }
    return render(request,'order_list.html',context)

@csrf_exempt
def order_add(request):
    form = OrderModelForm(data=request.POST)
    print(request.POST)
    if form.is_valid():
        form.instance.oid=datetime.now().strftime('%Y%m%d%H%M%S')+str(random.randint(1000,9999))
        form.instance.admin_id=request.session['info']['id']
        form.save()
        return JsonResponse({'status':True})
    return JsonResponse({'status':False,'error':form.errors})

def order_delete(request):
    uid=request.GET.get('uid')
    exists=Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({'status':False,'error':'删除失败，数据不存在'})
    Order.objects.filter(id=uid).delete()
    return JsonResponse({'status': True})

def order_detail(request):
    uid = request.GET.get('uid')
    row_dict=Order.objects.filter(id=uid).values('title','price','status').first()
    if not row_dict:
        return JsonResponse({'status': False, 'error': '数据不存在'})
    return JsonResponse({'status':True,'data':row_dict})

@csrf_exempt
def order_edit(request):
    uid=request.GET.get('uid')
    row_object=Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({'status': False, 'tips': '数据不存在'})
    form=OrderModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})