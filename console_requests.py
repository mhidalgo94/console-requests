import requests
import json
import ast
import urllib
import argparse

class Fast_Requests:

    def __init__(self,args):
        # Define all args
        self.args = args
        self.HOST = self.get_host()
        self.METHOD = self.get_method()
        self.DATA = self.get_data()
        self.params = self.get_params()
        self.headers = self.get_headers()
        self.response = self._requests()

    
    def get_host(self):
        url = self.get_url()
        return url

    def get_method(self):
        return f"{self.args.m}".upper()
    
    def get_params(self):
        return self.args.p

    def get_data(self):
        if self.args.d:
            d = ast.literal_eval(self.args.d)
        else:
            d = self.args.d
        return d

    def get_headers(self):
        return self.args.hds or {}

    def get_auth(self):
        auth = self.args.a
        print(auth)
        return auth

    def get_url(self):
        if 'https://' and 'http://' in self.args.u:
            url = self.args.u
        elif self.args.u == 'locahost' or '127.0.0.1':
            url = "http://" + self.args.u

            # if self.PORT is not None:
            #     url += ":" + self.PORT
            #     url += "/"
            # if self.path is not None:
            #     url += self.path
            # if self.params is not None:
            #     url += "?"
            #     url += urllib.urlencode(self.params)
        return url

    def _requests(self):
        method = self.METHOD
        params=self.params
        headers = self.headers
        # try:
        if method == 'GET':
            r = requests.get(self.HOST, params=params,headers=headers)
            return r
        elif method == "POST":
            headers["Content-Type"] = "application/json"
            r = requests.post(self.HOST, data= json.dumps(self.DATA),headers=headers,params=params)   #, headers={"Content-Type":"application/json"})
            return r
        elif method == "PUT":
            headers["Content-Type"] = "application/json"
            r = requests.put(self.HOST, data = json.dumps(self.DATA),headers=headers,params=params) 
            return r
        elif method == "DELETE":
            r = requests.delete(self.HOST,params=params)  
            return r
        # except Exception as e:
        #     print(e)
            
    def __repr__(self) -> str:
        data = self.args.format
        try:
            if data == "json":
                return f'STATUS_CODE:{self.response.status_code}- {self.response.json()}'
            elif data == "content":
                return f'STATUS_CODE:{self.response.status_code}- {self.response.content}'
            elif data == "text":
                return f'STATUS_CODE:{self.response.status_code}- {self.response.text}'
        except json.JSONDecodeError:
            return f'{self.response.text}'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-format",type=str, default="json",help="Formato retorno de datos.")
    parser.add_argument("-d",type=str,default=None, help="Datos para enviar (POST, DELETE, PUT).")
    parser.add_argument("-p",type=str, default=None, help="Parametros para enviar.")
    parser.add_argument("-hds",type=str, default=None, help="Headers para enviar.")
    parser.add_argument("-u",type=str, required=True,help="Servidor destino.")
    parser.add_argument("-m",type=str, default="GET",help="Metodo de peticion.")




    args = parser.parse_args()
    # Fast_Requests(args)

    print(Fast_Requests(args))


if __name__ == '__main__':
    main()


