
In this repo there are different kinds of python scripts for their respective uses. These all are open sourced and you can use them in any form for free.

Script created with the aim of making requests through the console through command lines or configuration files.    
## Instalation

```bash
git clone https://github.com/mhidalgo94/console-requests.git
```

create virtual environment to install requirements.
```bash
pip install virtualenv
```

After install virtual enviroment, create eviroment and activate
### Linux
```bash
virutalenv env
source env/bin/activate
```
###  Windows
```bash
virutalenv env
./env/Script/activate
``` 
### Then you install the requirements
```bash
pip install -r requirements.txt 
```

## How to use
Puedes iniciar la ayuda parametros -h
```python
python console_requests.py -h 
usage: console_requests.py [-h] [-format FORMAT] [-d D] [-p P] [-hds HDS] [-m M] [-dfile DFILE] [-cfile CFILE [CFILE ...]]

options:
  -h, --help            show this help message and exit
  -format FORMAT        Return data format.(json,conent,text)
  -d D                  Data to send.Type JSON
  -p P                  Shipping parameters.
  -hds HDS              Add headers to requests.
  -m M                  Request method, default GET select (POST, DELETE, PUT).
  -dfile DFILE          Send data with a file.
  -cfile CFILE [CFILE]  Config file with all data.
```

The script has several ways to make requests to the Rest API server

1. Request through console
### Method GET (default)
```python
python console_requests.py -u http://localhost:8000/api/list-album/
STATUS_CODE:200 METHOD:GET INFO:[{"id":8,"name":"Carlos","release_date":"2022-06-01","num_stars":3,"artist":1},{"id":9,"name":"Carlos","release_date":"2022-06-01","num_stars":3,"artist":1},{"id":12,"name":"Pedro","release_date":"2022-06-01","num_stars":3,"artist":1},{"id":13,"name":"Pedro","release_date":"2022-06-01","num_stars":3,"artist":1},{"id":14,"name":"Maikel","release_date":"2022-07-01","num_stars":5,"artist":1},{"id":16,"name":"Maikel","release_date":"2022-07-01","num_stars":5,"artist":1},{"id":21,"name":"Maikel","release_date":"2022-07-01","num_stars":5,"artist":1}]
```
### Method POST
```python
python console_requests.py -u http://localhost:8000/api/list-album/ -m POST -d '{"name":"Carlos","release_date":"2022-06-01","num_stars":3,"artist":1}'
```

You can see the response status when you make the request unless the server does not return a response

```
STATUS_CODE:405 METHOD:POST INFO:{"detail":"Method \"POST\" not allowed."}
```

or 

```python
python console_requests.py -u http://localhost:8000/api/create-album/ -m POST -d {'name':'Carlos','release_date':'2022-06-01','num_stars':3,'artist':1}
STATUS_CODE:201 METHOD:POST INFO:{"id":33,"name":"Carlos","release_date":"2022-06-01","num_stars":3,"artist":1}
```

2. Request through console with data by json file
Example file `data.json`
```json
{
    "server":"http://localhost:8000/api/create-album/",
    "method": "PUT",
    "format": "text",
    "data": {
        "name": "Jhonson",
        "release_date": "2022-07-01",
        "num_stars": 5,
        "artist": 1
    }
}
```

Response
```python
python console_requests.py -dfile data.json
STATUS_CODE:201 METHOD:POST INFO:{'id': 35, 'name': 'Jhonson', 'release_date': '2022-07-01', 'num_stars': 5, 'artist': 1}
```

3. Request through console with data by configuration of init or txt file.
- You need the -cfile option, then file path and configuration profile name.
Example file `configfile.ini`
```init
[ALBUM]
url = http://localhost:8000/api/list-album/
method = GET
format = json
file_data = data.json

[AUTOR]
url = http://localhost:8000/api/list-autor/
method = POST
format = json
data = {'name': 'Jhonson', 'release_date': '2022-07-01', 'num_stars': 5, 'artist': 1}
params = {"Content-Type":"application/json"}
```
```
- Execute command.
```python
python console_requests.py -cfile configfile.ini ALBUM
```
or
```python
python console_requests.py -cfile configfile.ini autor
STATUS_CODE:201 METHOD:POST INFO:{'id': 38, 'name': 'Jhonson', 'release_date': '2022-07-01', 'num_stars': 5, 'artist': 1}
```