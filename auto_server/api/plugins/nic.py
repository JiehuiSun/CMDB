#!/usr/bin/env python
#_*_ coding:utf-8 _*_
# __author__ = "huihui"
# Date: 2017/10/10 0011

from repository import models
from api.plugins import update_func

class Nic(object):
    def __init__(self,server_obj,info):
        self.server_obj = server_obj
        self.nic_dict = info.get('data')

    def process(self):
        # print(123)
        # 更新网卡信息---------------------------------------------
        old_nics_obj = models.NIC.objects.filter(server_obj=self.server_obj)  # 原来的所有网卡集合
        update_list = update_func.update_set('网卡', old_nics_obj, self.nic_dict,
                                             self.server_obj.id)  # 信息列表[需要添加的资产集合0，需要删除的资产集合1，需要更新的资产集合2，需要跟新的新数据3]

        if update_list[0]:
            for i in update_list[0]:
                models.NIC.objects.create(**update_list[3].get(i))
                update_content = '%s 网卡添加成功！' % i
                print(update_content)
                models.ServerRecord.objects.create(server_obj=self.server_obj, name='网卡', content=update_content)

        if update_list[1]:
            # models.NIC.objects.filter(name=del_nic).delete() 可以直接删除所有的，但是要写入日志
            for i in update_list[1]:
                models.NIC.objects.get(name=i, server_obj=self.server_obj).delete()
                update_content = '%s 网卡删除成功！' % i
                print(update_content)
                models.ServerRecord.objects.create(server_obj=self.server_obj, name='网卡', content=update_content)

        new_update = {}  # 定义需要更新的字段字典
        # 开始更新..
        for i in update_list[2]:
            nic_obj_set = models.NIC.objects.filter(name=i, server_obj=self.server_obj)  # 重新取一下query_set
            nic_obj = nic_obj_set.first()
            update_nic_success_dict = update_func.update_info(i, self.nic_dict[i], self.nic_dict, nic_obj, nic_obj_set)
            for update_name, update_data in update_nic_success_dict['new'].items():
                update_content = '%s 记录的 %s 信息将 %s 已更改为 %s' % (
                update_nic_success_dict['update_name'], update_name, update_nic_success_dict['old'][update_name],
                update_data)
                print('网卡：', update_content)
                models.ServerRecord.objects.create(server_obj=self.server_obj, name='网卡', content=update_content)
