import os
import subprocess
import sys

def install():
    subprocess.check_call([sys.executable, "-m", "pip", "install","-r", "requirements.txt"])

install()
os.system('python manage.py runserver')