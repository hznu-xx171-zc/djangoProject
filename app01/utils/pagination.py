from django.utils.safestring import mark_safe
'''
使用时:在view,py中
1.筛选想要的数据
def pretty_list(request):
    queryset = PrettyNum.objects.filter()
    
2.实例化分页对象
    page_object=Pagination(request,queryset)
    context={
        "queryset":page_object.page_queryset,  #分完页的数据
        'page_string':page_object.html()        #生成页码
    }
    return render(request,'pretty_list.html',context)

在html中:
1.生成数据
{% for item in queryset %}
    <tr>
        <td>{{ item.id }}</td>
        <td>{{ item.mobile }}</td>
        <td>{{ item.price }}</td>
        <td>{{ item.get_level_display }}</td>
        <td>{{ item.get_status_display }}</td>
        <td>
            <a class="btn btn-primary btn-xs" href="/pretty/{{ item.id }}/edit/">编辑</a>
            <a class="btn btn-danger btn-xs" href="/pretty/{{ item.id }}/delete/">删除</a>
        </td>
    </tr>
{% endfor %}
2.生成页码
<ul class="pagination">
    {{ page_string }}
</ul>
'''
class Pagination(object):
    def __init__(self,request,queryset,page_size=10,page_param='page',plus=5):
        '''
        :param request: 请求的对象
        :param queryset: 符合条件的数据
        :param page_size: 每页显示多少条数据
        :param page_param: 在URL中获取页码的参数，例如/pretty/list/?page=12
        :param plus: 显示当前页的前和后几页(页码)
        '''

        from django.http.request import QueryDict
        import copy
        query_dict=copy.deepcopy(request.GET)
        query_dict._mutable=True
        self.query_dict=query_dict
        page = request.GET.get(page_param, '1')
        if page.isdecimal():
            page=int(page)
        else:
            page=1
        self.page=page
        self.page_size=page_size
        start = (page - 1) * page_size
        end = page * page_size
        self.page_queryset=queryset[start:end]
        total_count = queryset.count()
        totol_page_count, div = divmod(total_count, page_size)
        if div:
            totol_page_count += 1
        self.totol_page_count=totol_page_count
        self.plus=plus
        self.page_param=page_param

    def html(self):
        if self.totol_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.totol_page_count + 1
        else:
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1 + 1
            else:
                if (self.page + self.plus) > self.totol_page_count:
                    start_page = self.totol_page_count - 2 * self.plus
                    end_page = self.totol_page_count + 1
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus + 1
        page_str_list = []
        self.query_dict.setlist(self.page_param,[1])
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)
        for i in range(start_page, end_page):
            if i == self.page:
                self.query_dict.setlist(self.page_param, [i])
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                self.query_dict.setlist(self.page_param, [i])
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)
        if self.page < self.totol_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            next = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.totol_page_count])
            next = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(next)
        self.query_dict.setlist(self.page_param, [self.totol_page_count])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))

        search_string = '''
            <li>
                        <form style="width: 200px;float: left" method="get" >
                            <div class="input-group">
                                <input type="text" name="page" class="form-control" placeholder="页码">
                                <span class="input-group-btn">
                <button class="btn btn-default" type="submit">跳 转</button>
              </span>
                            </div>
                        </form>
                    </li>
            '''
        page_str_list.append(search_string)
        page_string = mark_safe(''.join(page_str_list))
        return page_string
