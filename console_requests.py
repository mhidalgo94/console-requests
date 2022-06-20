from urllib.request import Request
import requests
import json
import ast
import colorama
import argparse
import sys

class Fast_Requests:

    def __init__(self,args):
        # Define all args
        self.args = args
        self.dfile = self.args.dfile
        self.HOST = self.get_host()
        self.METHOD = self.get_method()
        self.DATA = self.get_data()
        self.format = self.get_format()
        self.params = self.get_params()
        self.headers = self.get_headers()
        self.response = self._requests()

    def get_data_file(self):
        if self.dfile:
            with open(self.dfile, 'r') as f:
                data_tojson = json.load(f)
                return data_tojson
        else:
            return None

    
    def get_host(self):
        if self.dfile:
            host = self.get_data_file().get('url',None) or self.get_data_file().get('host',None) or self.get_data_file().get('server',None)
            if host is None:
                print(colorama.Fore.RED + "ERROR:" + "Wrong data file configuration. Try url, host or server")
                sys.exit()
            return host
        return self.args.u

    def get_method(self):
        if self.dfile:
            method = self.get_data_file()['method'].upper()
            return method
        return self.args.m.upper()

    def get_format(self):
        if self.get_data_file().get('format'):
            return self.get_data_file().get('format') 
        else:
            return self.args.format
    
    def get_params(self):
        return self.args.p


    def get_data(self):
        if self.args.d:
            d = ast.literal_eval(self.args.d)
        elif self.dfile:
            d = self.get_data_file()['data']
        else:
            d = self.args.d
        return d

    def get_headers(self):
        return self.args.hds or None


    def _requests(self):
        method = self.METHOD
        params=self.params
        try:
            if method == 'GET':
                r = requests.get(self.HOST, params=params,headers=self.headers)
                self.header = r.headers
                return r
            elif method == "POST":
                r = requests.post(self.HOST, json= self.DATA, headers=self.headers,params=params)
                self.headers = r.headers   #, headers={"Content-Type":"application/json"})
                return r
            elif method == "PUT":
                r = requests.put(self.HOST, json = self.DATA, headers=self.headers,params=params)
                self.headers = r.headers 
                return r
            elif method == "DELETE":
                r = requests.delete(self.HOST,params=params)
                self.headers = r.headers
                return r
        except requests.RequestException:
            print(colorama.Fore.RED + 'ERROR: There was an ambiguous exception that occurred while handling your request.')
        except requests.HTTPError:
            print(colorama.Fore.RED + 'ERROR: An HTTP error occurred.')
        except requests.URLRequired:
            print(colorama.Fore.RED + 'ERROR: A valid URL is required to make a request.')
        except requests.TooManyRedirects:
            print(colorama.Fore.RED + 'ERROR: Too many redirects.')
        except requests.ConnectTimeout:
            print(colorama.Fore.RED + 'ERROR: The request timed out while trying to connect to the remote server.')
        except requests.ReadTimeout:
            print(colorama.Fore.RED + 'ERROR: The server did not send any data in the allotted amount of time.')
        except requests.Timeout:
            print(colorama.Fore.RED + 'ERROR: The request timed out.')
        except Exception as e:
            print(colorama.Fore.RED + str(e))
        sys.exit()


    def __repr__(self) -> str:
        f = self.format
        try:
            if f == "json":
                return f'{colorama.Fore.GREEN}RESPONSE:{self.response.status_code} {colorama.Fore.YELLOW}METHOD:{self.METHOD} {colorama.Fore.RESET}INFO:{self.response.json()}'
            elif f == "content":
                return f'{colorama.Fore.GREEN}RESPONSE:{self.response.status_code} {colorama.Fore.YELLOW}METHOD:{self.METHOD} {colorama.Fore.RESET}INFO:{self.response.content}'
            elif f == "text":
                return f'{colorama.Fore.GREEN}RESPONSE:{self.response.status_code} {colorama.Fore.YELLOW}METHOD:{self.METHOD} {colorama.Fore.RESET}INFO:{self.response.text}'
        except json.JSONDecodeError:
            return f'{self.response.text}'



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-format",type=str, default="text",help="Return data format.(json,conent,text)")
    parser.add_argument("-d",type=str,default=None, help="Data to send.Type JSON")
    parser.add_argument("-p",type=str, default=None, help="Shipping parameters.")
    parser.add_argument("-hds",type=str, default=None, help="Add headers to requests.")
    parser.add_argument("-m",type=str, default="GET",help="Request method, default GET select (POST, DELETE, PUT,).")
    parser.add_argument("-dfile",type=str, default=None, help="Send data with a file.")

    namespace,arr = parser.parse_known_args()

    if namespace.dfile is None:
        parser.add_argument("-u",type=str,required=True,help="Server requests.")
    else:
        parser.add_argument("-u",type=str,required=False,help="Server requests.")

    args = parser.parse_args()

    # Fast_Requests(args)
    print(Fast_Requests(args))


if __name__ == '__main__':
    colorama.init()

    main()


