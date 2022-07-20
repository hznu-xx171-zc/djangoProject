from  django.shortcuts import render
from  django.http import JsonResponse
def chart_list(request):
    return render(request,'chart_list.html')

def chart_bar(request):
    legend=['张三', '李四']
    xAxis=['1月', '2月', '3月', '4月', '5月', '6月']
    series=[
          {
            'name': '张三',
            'type': 'bar',
            'data': [5, 20, 36, 10, 10, 20]
          },
          {
            'name': '李四',
            'type': 'bar',
            'data': [15, 24, 31, 40, 15, 44]
          }
        ]
    result={
        'status':True,
        'data':{
            'legend':legend,
            'xAxis':xAxis,
            'series':series,
    }
    }
    return JsonResponse(result)

def chart_pie(request):
    data_list=[
            {'value': 1048, 'name': 'IT部门'},
            {'value': 735, 'name': '运营部'},
            {'value': 580, 'name': '新媒体'}
        ]
    result = {
        'status': True,
        'data': data_list
    }
    return JsonResponse(result)

def chart_line(request):
    legend=['上海', '杭州']
    xAxis=['1月', '2月', '3月', '4月', '5月', '6月']
    series=[
        {
            'name': legend[0],
            'type': 'line',
            'stack': 'Total',
            'data': [120, 132, 101, 134, 90, 230, 210]
        },
        {
            'name': legend[1],
            'type': 'line',
            'stack': 'Total',
            'data': [220, 182, 191, 234, 290, 330, 310]
        },
    ]
    result = {
        'status': True,
        'data': {
            'legend':legend,
            'xAxis':xAxis,
            'series':series
        }
    }
    return JsonResponse(result)