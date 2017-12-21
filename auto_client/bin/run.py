import sys
import os
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
os.environ['AUTO_CLIENT_SETTINGS'] = "conf.settings"
from src import script


if __name__ == '__main__':
    script.start()