#!/usr/bin/env python
#_*_ coding:utf-8 _*_
# __author__ = "huihui"
# Date: 2017/9/28 0028



def update_info(update_name,update_dict,new_dict,old_update_obj,update_set,ass_name=None):
    '''

    :param update_name: 需要更新的资产名
    :param update_dict: 需要更新的数据集合
    :param new_dict: 新数据的字典信息
    :param old_update_obj: 数据库更新对象
    :param update_set: 更新的数据库集合
    :param ass_name: 由于硬盘的capacity信息的数据类型问题，需要做一层判断
    :return:更新资产名，更新设备名，源信息，新信息
    '''
    update_success_dict = {'update_name':update_name,'new':{},'old':{}} # 定义更新完成的信息
    new_update = {}  # 定义需要更新的字段字典
    for k in update_dict:
        # print(new_dict,4444)
        if update_name == 'basic':
            new_info = new_dict.get(k)  # 取到最新获取的信息
        elif ass_name == 'disk' and k == 'capacity':
            # print('这是硬盘')
            new_info = new_dict.get(update_name).get(k)  # 取到最新获取的信息
            new_info = float(new_info)
        else:
            new_info = new_dict.get(update_name).get(k)  # 取到最新获取的信息
        old_info = getattr(old_update_obj, k)  # 利用getattr取到数据库原来的信息 (需要对象)
        if new_info != old_info:
            # print(333333333333,new_info,old_info,type(new_info),type(old_info))
            new_update[k] = new_info  # 有不同以最新数据记录到要更新的字典
            update_success_dict['new'][k]=new_info
            update_success_dict['old'][k]=old_info

    # print(new_update)
    update_set.update(**new_update)  # 更新 (需要集合)
    return update_success_dict


def update_set(assets,old_obj, new_info,server_obj):
    """
    :param assets: 需要处理的资产名
    :param old_obj: 原来资产的集合
    :param new_info: 新资产的更新内容 xxx:{a1:11,a2,22}
    :param server_obj: 资产所属服务器对象
    :return: 信息列表[需要添加的资产集合，需要删除的资产集合，需要更新的资产集合，需要跟新的新数据]
    """
    new_nic_dict = {}  # 所有新网卡及信息
    new_nic_set = set()  # 取差集用
    old_nic_set = set()

    # 取到所有新网卡数据的set及dict
    for new_nic_name, new_nic_info in new_info.items():
        # print(new_nic_name)
        new_nic_dict[new_nic_name] = new_nic_info
        new_nic_set.add(new_nic_name)
        # print('aaaaaaaaa',new_nic_dict)
        new_nic_dict[new_nic_name]['server_obj_id'] = server_obj
        if assets == '网卡':
            new_nic_dict[new_nic_name]['name'] = new_nic_name
    # 取到所有原网卡的set
    for old_nic_obj in old_obj:
        if assets == '网卡':
            old_nic_set.add(old_nic_obj.name)
        else:
            old_nic_set.add(old_nic_obj.slot)

    add_nic = new_nic_set - old_nic_set  # 取出要添加的网卡
    # print('aaaaaaaaaaaaaaa',add_nic,new_nic_set,old_nic_set)
    del_nic = old_nic_set - new_nic_set  # 取出要删除的网卡
    edit_nic = new_nic_set - add_nic - del_nic  # 取出要更新的网卡
    update_list = [add_nic, del_nic, edit_nic, new_nic_dict]
    return update_list

