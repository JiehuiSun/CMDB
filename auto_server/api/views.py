from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import json
from repository import models
from api.plugins import update_func
from django.db.models import Q
from datetime import date
from api.api_auth import api_auth
from django.db import transaction
from .plugins import PluginManger

@csrf_exempt
@api_auth
def server(request):
    if request.method == 'GET':
        # 获取今日为采集的主机列表
        # print(123)
        current_date = date.today()
        host_list = models.Server.objects.filter(Q(latest_date=None)|Q(latest_date__date__lt=current_date)).values('hostname')
        # print(host_list,type(host_list))
        host_list = list(host_list)
        # print(host_list,type(host_list))
        return HttpResponse(json.dumps(host_list))

    else:
        # 客户端采集的最新资产信息
        server_info = json.loads(request.body.decode('utf8'))
        if not server_info.get('basic').get('status'):
            return HttpResponse('获取信息失败！')
        # print(server_info,type(server_info))

        manager = PluginManger()
        response = manager.exec(server_info)

        return HttpResponse(json.dumps(response))
        '''
        new_host = server_info.get('basic').get('data').get('hostname')
        old_host = models.Server.objects.filter(hostname=new_host).first()
        # 获取所有新的资产信息
        server = server_info.get('basic').get('data')  # 取到主机的信息
        nic = server_info.get('nic').get('data')  # 获取所有网卡信息
        disk = server_info.get('disk').get('data')  # 获取所有硬盘信息
        mem = server_info.get('memory').get('data')  # 获取所有内存信息
        board = server_info.get('board').get('data')  # 获取主板信息
        if not old_host:
            try:
                with transaction.atomic():
                    # 如果没有这个主机的信息，则添加新记录
                    # server_obj = models.Server.objects.create(hostname=server.get('hostname'),os_platform=server['os_platform'],os_version=server.get('os_version'))
                    # 将主机资产写入数据库
                    server_obj = models.Server.objects.create(**server,**board)
                    print('%s 主机添加成功！'%server_obj)
                    # 将这个主机的所有网卡添加到资产库
                    if server_info.get('nic').get('status'):
                        for nic_name in nic:
                            models.NIC.objects.create(name=nic_name,server_obj=server_obj,**nic.get(nic_name))
                        print('网卡添加成功！')
                    # 添加硬盘
                    if server_info.get('disk').get('status'):
                        for disk_name,disk_info in disk.items():
                            models.Disk.objects.create(server_obj=server_obj,**disk_info)
                        print('硬盘添加成功！')
                    # 添加内存
                    if server_info.get('memory').get('status'):
                        for mem_name,mem_info in mem.items():
                            models.Memory.objects.create(server_obj=server_obj,**mem_info)
                        print('内存添加成功！')
            except Exception as e:
                print('服务器挂掉了..')

        else:

            # 如果有这个主机的信息，则先判断是否有这个资产信息，如果没有则添加资产，如果有则对比是否有不同

            print('有 %s 这个主机了！'%old_host.hostname)
            # 更新主机信息------------------------------------------
            server_obj = models.Server.objects.filter(hostname=old_host.hostname) # 重新取一下query_set
            update_server_success_dict = update_func.update_info('basic',server,server,old_host,server_obj)
            for update_name, update_data in update_server_success_dict['new'].items():
                update_content = '%s 记录的 %s 信息将 %s 已更改为 %s' % (update_server_success_dict['update_name'], update_name, update_server_success_dict['old'][update_name], update_data)
                print('主机',update_content)
                models.ServerRecord.objects.create(server_obj=old_host, name='主机', content=update_content)

            # 更新网卡信息---------------------------------------------
            old_nics_obj = models.NIC.objects.filter(server_obj=old_host)  # 原来的所有网卡集合
            update_list = update_func.update_set('网卡',old_nics_obj,nic,old_host.id) # 信息列表[需要添加的资产集合0，需要删除的资产集合1，需要更新的资产集合2，需要跟新的新数据3]

            if update_list[0]:
                for i in update_list[0]:
                    models.NIC.objects.create(**update_list[3].get(i))
                    update_content = '%s 网卡添加成功！'%i
                    print(update_content)
                    models.ServerRecord.objects.create(server_obj=old_host, name='网卡', content=update_content)


            if update_list[1]:
                # models.NIC.objects.filter(name=del_nic).delete() 可以直接删除所有的，但是要写入日志
                for i in update_list[1]:
                    models.NIC.objects.get(name=i,server_obj=old_host).delete()
                    update_content = '%s 网卡删除成功！'%i
                    print(update_content)
                    models.ServerRecord.objects.create(server_obj=old_host, name='网卡', content=update_content)



            new_update = {} # 定义需要更新的字段字典
            # 开始更新..
            for i in update_list[2]:
                nic_obj_set = models.NIC.objects.filter(name=i,server_obj=old_host)  # 重新取一下query_set
                nic_obj = nic_obj_set.first()
                update_nic_success_dict = update_func.update_info(i,nic[i],nic,nic_obj,nic_obj_set)
                for update_name,update_data in update_nic_success_dict['new'].items():
                    update_content = '%s 记录的 %s 信息将 %s 已更改为 %s'%(update_nic_success_dict['update_name'],update_name,update_nic_success_dict['old'][update_name],update_data)
                    print('网卡：',update_content)
                    models.ServerRecord.objects.create(server_obj=old_host, name='网卡', content=update_content)

            # 更新硬盘信息-------------------------------------
            old_disk_obj = models.Disk.objects.filter(server_obj=old_host)  # 原来的所有网卡集合
            update_list = update_func.update_set('硬盘',old_disk_obj,disk,old_host.id) # 信息列表[需要添加的资产集合0，需要删除的资产集合1，需要更新的资产集合2，需要更新的新数据3]

            if update_list[0]:
                for i in update_list[0]:
                    models.Disk.objects.create(**update_list[3].get(i))
                    update_content = '%s 硬盘添加成功！'%i
                    print(update_content)
                    models.ServerRecord.objects.create(server_obj=old_host, name='硬盘', content=update_content)



            if update_list[1]:
                # models.NIC.objects.filter(name=del_nic).delete() 可以直接删除所有的，但是要写入日志
                for i in update_list[1]:
                    models.Disk.objects.get(name=i,server_obj=old_host).delete()
                    update_content = '%s 硬盘删除成功！'%i
                    print(update_content)
                    models.ServerRecord.objects.create(server_obj=old_host, name='硬盘', content=update_content)

            # 开始更新..
            for i in update_list[2]:
                disk_obj_set = models.Disk.objects.filter(slot=i,server_obj=old_host)  # 重新取一下query_set
                disk_obj = disk_obj_set.first()
                update_disk_success_dict = update_func.update_info(i,disk[i],disk,disk_obj,disk_obj_set,'disk')
                for update_name,update_data in update_disk_success_dict['new'].items():
                    update_content = '%s 记录的 %s 信息将 %s 已更改为 %s'%(update_disk_success_dict['update_name'],update_name,update_disk_success_dict['old'][update_name],update_data)
                    print('硬盘：',update_content)
                    models.ServerRecord.objects.create(server_obj=old_host,name='硬盘',content=update_content)



            # 更新内存信息-------------------------------------
            old_mem_obj = models.Memory.objects.filter(server_obj=old_host)  # 原来的所有网卡集合
            update_list = update_func.update_set('内存',old_mem_obj, mem,old_host.id)  # 信息列表[需要添加的资产集合0，需要删除的资产集合1，需要更新的资产集合2，需要跟新的新数据3]

            if update_list[0]:
                for i in update_list[0]:
                    print(i)
                    print(update_list[3].get(i))
                    models.Memory.objects.create(**update_list[3].get(i))
                    update_content = '%s 内存添加成功！' % i
                    print(update_content)
                    models.ServerRecord.objects.create(server_obj=old_host, name='内存', content=update_content)


            if update_list[1]:
                # models.NIC.objects.filter(name=del_nic).delete() 可以直接删除所有的，但是要写入日志
                for i in update_list[1]:
                    models.Memory.objects.get(slot=i,server_obj=old_host).delete()
                    update_content = '%s 内存删除成功！' % i
                    print(update_content)
                    models.ServerRecord.objects.create(server_obj=old_host, name='内存', content=update_content)

            # 开始更新..
            for i in update_list[2]:
                mem_obj_set = models.Memory.objects.filter(slot=i,server_obj=old_host)  # 重新取一下query_set
                mem_obj = mem_obj_set.first()

                update_mem_success_dict = update_func.update_info(i, mem[i], mem, mem_obj, mem_obj_set)
                for update_name, update_data in update_mem_success_dict['new'].items():
                    update_content = '%s 记录的 %s 信息将 %s 已更改为 %s' % (
                    update_mem_success_dict['update_name'], update_name, update_mem_success_dict['old'][update_name],
                    update_data)
                    print('内存：',update_content)
                    models.ServerRecord.objects.create(server_obj=old_host,name='内存',content=update_content)


    return HttpResponse('ok')
    '''


