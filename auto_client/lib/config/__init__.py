import os
import importlib
from . import global_settings

class Settings(object):
    """
    global_settings,配置获取
    settings.py，配置获取
    """
    def __init__(self):

        for item in dir(global_settings):
            if item.isupper():
                k = item
                v = getattr(global_settings,item)
                setattr(self,k,v)

        setting_path = os.environ.get('AUTO_CLIENT_SETTINGS')
        md_settings = importlib.import_module(setting_path)
        for item in dir(md_settings):
            if item.isupper():
                k = item
                v = getattr(md_settings,item)
                if k == "PLUGIN_ITEMS":
                    self.PLUGIN_ITEMS.update(v)
                else:
                    setattr(self,k,v)


settings = Settings()