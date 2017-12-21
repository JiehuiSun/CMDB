import os
from lib.config import settings

class Board(object):
    def process(self, cmd_func, test):
        if test:
            output = open(os.path.join(settings.BASEDIR, 'files/board.out'), 'r', encoding='utf-8').read()
        else:
            output = cmd_func("sudo dmidecode -t1")
        return self.parse(output)

    def parse(self, content):

        result = {}
        key_map = {
            'Manufacturer': 'manufacturer',
            'Product Name': 'model',
            'Serial Number': 'sn',
        }

        for item in content.split('\n'):
            row_data = item.strip().split(':')
            if len(row_data) == 2:
                if row_data[0] in key_map:
                    result[key_map[row_data[0]]] = row_data[1].strip() if row_data[1] else row_data[1]

        return result

