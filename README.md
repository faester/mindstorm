# Install

This is standard flask, use
```
pip install flask
```

Tell Flask where to start 

### Powershell
```
$env:FLASK_APP ="server/flaskr"
```

### bash 
```
$ export FLASK_ENV=development
$ flask run --host=0.0.0.0
```

### Running flask 
```flask run```

# venv
http://flask.pocoo.org/docs/1.0/installation/#virtual-environments

## Activate venv (windows)
.\venv\Scripts\activate


# 'sys' folder
This folder contains a copy of a subset of the /sys/class folder from a
brick running with two motors and the IR sensor connected. It is meant 
for tests and development, where the brick is not actually running. 
(ie: a very simple simulator.)

