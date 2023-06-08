import os.path
import subprocess
import os
# Path to a Python interpreter that runs any Python script
# under the virtualenv /path/to/virtualenv/
python_bin = "../djangoProject/venv/Scripts/python.exe"
asd = os.path.isfile(python_bin)

# Path to the script that must run under the virtualenv
script_file = "../djangoProject/runserver.py"
cxvsc = os.path.isfile(script_file)
subprocess.Popen([python_bin, script_file])