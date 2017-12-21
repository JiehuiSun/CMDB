from repository import models

class Disk(object):
    def __init__(self,server_obj,info):
        self.server_obj = server_obj
        self.disk_dict = info

    def process(self):
        # 硬盘、网卡和内存
        new_disk_info_dict = self.disk_dict['data']
        """
        {
            '0': {'slot': '0', 'pd_type': 'SAS', 'capacity': '279.396', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'},
            '1': {'slot': '1', 'pd_type': 'SAS', 'capacity': '279.396', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5AH'},
            '2': {'slot': '2', 'pd_type': 'SATA', 'capacity': '476.939', 'model': 'S1SZNSAFA01085L     Samsung SSD 850 PRO 512GB               EXM01B6Q'},
            '3': {'slot': '3', 'pd_type': 'SATA', 'capacity': '476.939', 'model': 'S1AXNSAF912433K     Samsung SSD 840 PRO Series              DXM06B0Q'},
            '4': {'slot': '4', 'pd_type': 'SATA', 'capacity': '476.939', 'model': 'S1AXNSAF303909M     Samsung SSD 840 PRO Series              DXM05B0Q'},
            '5': {'slot': '5', 'pd_type': 'SATA', 'capacity': '476.939', 'model': 'S1AXNSAFB00549A     Samsung SSD 840 PRO Series
        }"""
        new_disk_info_list = self.server_obj.disk.all()
        """
        [
            obj,
            obj,
            obj,
        ]
        """
        new_disk_slot_set = set(new_disk_info_dict.keys())
        old_disk_slot_set = {obj.slot for obj in new_disk_info_list}

        # add_slot_list = new_disk_slot_set - old_disk_slot_set
        add_slot_list = new_disk_slot_set.difference(old_disk_slot_set)
        del_slot_list = old_disk_slot_set.difference(new_disk_slot_set)
        update_slot_list = old_disk_slot_set.intersection(new_disk_slot_set)

        add_record_list = []
        # 增加 [2,5]
        for slot in add_slot_list:
            value = new_disk_info_dict[slot]
            tmp = "添加硬盘..."
            add_record_list.append(tmp)
            value['server_obj'] = self.server_obj
            models.Disk.objects.create(**value)
        # 删除 [4,6]
        models.Disk.objects.filter(server_obj=self.server_obj, slot__in=del_slot_list).delete()

        # 更新 [7,8]
        for slot in update_slot_list:
            value = new_disk_info_dict[
                slot]  # {'slot': '0', 'pd_type': 'SAS', 'capacity': '279.396', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'}
            obj = models.Disk.objects.filter(server_obj=self.server_obj, slot=slot).first()
            for k, new_val in value.items():
                old_val = getattr(obj, k)
                if old_val != new_val:
                    setattr(obj, k, new_val)
            obj.save()

    def add_disk(self):
        pass

    def del_disk(self):
        pass

    def update_disk(self):
        pass