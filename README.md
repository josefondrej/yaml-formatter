Kubernetes .yaml Deployment Formatter
======================================

Small utility that makes the kubernetes deployment yaml files more human readable. 

- Install requirements using:

    `python -m pip install -r requirements.txt`

- Set up an alias in `.bashrc` like

    `alias yform='python /home/josef/dev/yaml_formatter/yaml_format.py`

- and then use

    `cat file.yaml | yform` 