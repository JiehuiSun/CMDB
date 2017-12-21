from django.shortcuts import render,HttpResponse
import json,time
from repository import models
from django.http import JsonResponse # 用法  return JsonResponse(data) 同 return HttpResponse(json.dumps(data))
from utils.page import Pagination

# Create your views here.


def server(request):

    return render(request,'server.html')

def server_json(request):
    if request.method == 'GET':
        time.sleep(0.5)
        search_config = [
            {'name': 'server_status_id', 'title': '服务器状态', 'type': 'select', 'choice_name': 'status_choices'},
            {'name': 'hostname__contains','title':'主机名','type':'input'},
            {'name': 'cabinet_num', 'title': "机柜号", 'type': 'input'},

        ]
        table_config = [
            {
                'q': None,
                'title': '选择',
                'display':True,
                'text': {'tpl': '<input type="checkbox" value="{nid}" />', 'kwargs': {'nid': '@id'}},
                'attr': {'class': 'c1', 'nid': '@id'},
            },
            {
                'q': 'id',
                'display': False,
                'title': 'ID',
                'text': {'tpl': '{a1}', 'kwargs': {'a1': '@id'}},
                'attr':{},
            },
            {
                'q':'hostname',
                'display': True,
                'title':'主机名',
                'text': {'tpl': '{a1}-{a2}', 'kwargs': {'a1': '@hostname', 'a2': '666'}},
                'attr': {'class': 'c1', 'edit': 'true', 'origin': '@hostname', 'name': 'hostname'},
            },
            {
                'q': 'sn',
                'display': True,
                'title': '序列号',
                'text': {'tpl': '{a1}', 'kwargs': {'a1': '@sn'}},
                'attr': {'class': 'c1', 'edit': 'true', 'origin': "@sn", 'name': 'sn'},
            },
            {
                'q': 'os_platform',
                'display': True,
                'title': '系统',
                'text': {'tpl': '{a1}', 'kwargs': {'a1': '@os_platform'}},
                'attr': {'class': 'c1','edit':'true','origin':'@os_platform','name':'os_platform'},
            },
            {
                'q': 'os_version',
                "display": True,
                'title': '系统版本',
                'text': {'tpl': '{a1}', 'kwargs': {'a1': '@os_version'}},
                'attr': {'class': 'c1'},
            },
            {
                'q': 'business_unit__name',
                'display': True,
                'title': '业务线',
                'text': {'tpl': '{a1}', 'kwargs': {'a1': '@business_unit__name'}},
                'attr': {'class': 'c1'},
            },
            {
                'q': 'server_status_id',
                'display': True,
                'title': '服务器状态',
                'text': {'tpl': '{a1}', 'kwargs': {'a1': '@@status_choices'}},
                'attrs': {'class':'server_status'},
                'attr': {'class': 'c1', 'edit': 'true', 'edit-type': 'select', 'choice-key': 'status_choices',
                         'origin': '@server_status_id', 'name': 'server_status_id'},
            },
            # {
            #     'q': None,
            #     'display': True,
            #     'title': '操作',
            #     'text': {'tpl': '<a href="/edit/{nid}/">编辑</a> | <a href="/del/{uid}/">删除</a> ',
            #              'kwargs': {'nid': '@id', 'uid': '@id'}},
            # },
        ]

        values = []
        for item in table_config:
            if item['q']:
                values.append(item['q'])

        # 获取搜索条件
        condition_dict = json.loads(request.GET.get('search_condition'))
        """
        {
            server_status_id: [1,2],
            hostname: ['c1.com','c2.com']
        }
        """
        from django.db.models import Q
        con = Q()
        for k, v in condition_dict.items():
            temp = Q()
            temp.connector = 'OR'
            for item in v:
                temp.children.append((k, item,))
            con.add(temp, 'AND')

        current_page = request.GET.get('pageNum')
        total_item_count = models.Server.objects.filter(con).count()
        page_obj = Pagination(current_page, total_item_count,per_page_count=2)
        server_list = models.Server.objects.filter(con).values(*values)[page_obj.start:page_obj.end]


        response = {
            'search_config':search_config,
            'data_list':list(server_list),
            'table_config':table_config,
            'global_choices_dict':{
                'status_choices':models.Server.server_status_choices
            },
            'page_html': page_obj.page_html_js()
        }
        return JsonResponse(response)
    elif request.method == "DELETE":

        id_list = json.loads(request.body.decode('utf-8'))
        # str(request.body,encoding='utf-8')
        # bytes(v,encoding='utf-8')

        # models.Server.objects.filter(id__in=id_list).delete()
        # for nid in id_list:
        #     try:
        #         models.Server.objects.filter(id=nid).delete()
        #     except Exception as e:
        #         pass
        response = {'status': True, 'msg': None}
        try:
            # models.Server.objects.filter(id__in=id_list).delete()
            pass
        except Exception as e:
            response['status'] = False
            response['msg'] = str(e)

        return HttpResponse(json.dumps(response))
    elif request.method == 'PUT':
        update_info = json.loads(request.read().decode('utf-8'))[0]  # 获取需要更新的id及数据{'id': '5', 'hostname': 'c1.comsaa'}
        server_obj = models.Server.objects.filter(id=update_info.pop('nid')).update(**update_info)  # 过滤并更新返回值为(成功1，失败0)
        if server_obj:
            return HttpResponse(json.dumps('ok'))
        else:
            return HttpResponse(json.dumps('err'))

def del_(request,host_id):
    del_info = {}
    print('host_id',host_id)
    server_obj = models.Server.objects.filter(id=host_id).first()
    if host_id:
        if server_obj:
            del_info['status'] = 'ok'
            models.Server.objects.get(id=host_id).delete()
            update_content = 'id为 %s 的服务器已删除。'%host_id
            print(update_content)
            # models.ServerRecord.objects.create(server_obj=server_obj, name='主机', content=update_content)

    else:
        del_info['status'] = 'err'
    # return del_info
    return render(request,'server.html')

def xxxx(server_list):
    for row in server_list:
        for item in models.Server.server_status_choices:
            if item[0] == row['server_status_id']:
                row['server_status_id_name'] = item[1]
                break
        yield row

def test(request):
    data_list = models.Server.objects.all().values('hostname','server_status_id')
    return render(request,'test.html',{'server_list':xxxx(data_list)})

def ceshi(request):
    return render(request,'ceshi.html')
