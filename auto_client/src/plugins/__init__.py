import importlib
import requests
from lib.config import settings
import traceback
# def func():
#     server_info = {}
#     for k,v in settings.PLUGIN_ITEMS.items():
#         # 找到v字符串：src.plugins.nic.Nic，src.plugins.disk.Disk
#         module_path,cls_name = v.rsplit('.',maxsplit=1)
#         module = importlib.import_module(module_path)
#         cls = getattr(module,cls_name)
#         obj = cls()
#         ret = obj.process()
#         server_info[k] = ret
#
#     requests.post(
#         url=settings.API,
#         data=server_info
#     )

class PluginManager(object):
    def __init__(self,hostname=None):
        self.hostname = hostname
        self.plugin_items = settings.PLUGIN_ITEMS
        self.mode = settings.MODE
        self.test = settings.TEST
        if self.mode == "SSH":
            self.ssh_user = settings.SSH_USER
            self.ssh_port = settings.SSH_PORT
            self.ssh_pwd = settings.SSH_PWD


    def exec_plugin(self):
        server_info = {}
        for k,v in self.plugin_items.items():
            # 找到v字符串：src.plugins.nic.Nic，
            # src.plugins.disk.Disk
            info = {'status':True,'data': None,'msg':None}
            try:
                module_path,cls_name = v.rsplit('.',maxsplit=1)
                module = importlib.import_module(module_path)
                cls = getattr(module,cls_name)

                if hasattr(cls,'initial'):
                    obj = cls.initial()
                else:
                    obj = cls()
                ret = obj.process(self.exec_cmd,self.test)
                info['data'] = ret
            except Exception as e:
                info['status'] = False
                info['msg'] = traceback.format_exc()

            server_info[k] = info
        return server_info

    def exec_cmd(self,cmd):
        if self.mode == "AGENT":
            import subprocess
            result = subprocess.getoutput(cmd)
        elif self.mode == "SSH":
            import paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.hostname, port=self.ssh_port, username=self.ssh_user, password=self.ssh_pwd)
            stdin, stdout, stderr = ssh.exec_command(cmd)
            result = stdout.read()
            ssh.close()
        elif self.mode == "SALT":
            import subprocess
            result = subprocess.getoutput('salt "%s" cmd.run "%s"' %(self.hostname,cmd))
        else:
            raise Exception("模式选择错误：AGENT,SSH,SALT")
        return result