Kubernetes .yaml Deployment Formatter
======================================

Small utility that makes the kubernetes deployment yaml files more human readable. 

Use like:

`file.yaml | python yaml_format.py`

Personally I have an alias in `.bashrc`

`alias yform='python /home/josef/dev/yaml_formatter/yaml_format.py`

and then I can do 

`file.yaml | yform` 