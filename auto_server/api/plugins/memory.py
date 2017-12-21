#!/usr/bin/env python
#_*_ coding:utf-8 _*_
# __author__ = "huihui"
# Date: 2017/10/11 0011
from repository import models
from api.plugins import update_func
class Memory(object):
    def __init__(self,server_obj,info):
        self.server_obj = server_obj
        self.mem_dict = info.get('data')

    def process(self):
        # 更新内存信息-------------------------------------
        old_mem_obj = models.Memory.objects.filter(server_obj=self.server_obj)  # 原来的所有网卡集合
        update_list = update_func.update_set('内存', old_mem_obj, self.mem_dict,
                                             self.server_obj.id)  # 信息列表[需要添加的资产集合0，需要删除的资产集合1，需要更新的资产集合2，需要跟新的新数据3]
        
        if update_list[0]:
            for i in update_list[0]:
                print(i)
                print(update_list[3].get(i))
                models.Memory.objects.create(**update_list[3].get(i))
                update_content = '%s 内存添加成功！' % i
                print(update_content)
                models.ServerRecord.objects.create(server_obj=self.server_obj, name='内存', content=update_content)
        
        if update_list[1]:
            # models.NIC.objects.filter(name=del_nic).delete() 可以直接删除所有的，但是要写入日志
            for i in update_list[1]:
                models.Memory.objects.get(slot=i, server_obj=self.server_obj).delete()
                update_content = '%s 内存删除成功！' % i
                print(update_content)
                models.ServerRecord.objects.create(server_obj=self.server_obj, name='内存', content=update_content)
        
        # 开始更新..
        for i in update_list[2]:
            mem_obj_set = models.Memory.objects.filter(slot=i, server_obj=self.server_obj)  # 重新取一下query_set
            mem_obj = mem_obj_set.first()
        
            update_mem_success_dict = update_func.update_info(i, self.mem_dict[i], self.mem_dict, mem_obj, mem_obj_set)
            for update_name, update_data in update_mem_success_dict['new'].items():
                update_content = '%s 记录的 %s 信息将 %s 已更改为 %s' % (
                    update_mem_success_dict['update_name'], update_name, update_mem_success_dict['old'][update_name],
                    update_data)
                print('内存：', update_content)
                models.ServerRecord.objects.create(server_obj=self.server_obj, name='内存', content=update_content)
        
