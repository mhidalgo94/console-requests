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
        self.HOST = self.get_host()
        self.METHOD = self.get_method()
        self.DATA = self.get_data()
        self.params = self.get_params()
        self.headers = self.get_headers()
        self.response = self._requests()


    
    def get_host(self):
        
        return self.args.u

    def get_method(self):
        
        return self.args.m.upper()
    
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


    def _requests(self):
        method = self.METHOD
        params=self.params
        headers = self.headers
        try:
            if method == 'GET':
                r = requests.get(self.HOST, params=params,headers=headers)
                return r
            elif method == "POST":
                headers['Content-type'] = "application/json"
                r = requests.post(self.HOST, data= json.dumps(self.DATA),headers=headers,params=params)   #, headers={"Content-Type":"application/json"})
                return r
            elif method == "PUT":
                headers['Content-type'] = "application/json"
                r = requests.put(self.HOST, data = json.dumps(self.DATA),headers=headers,params=params) 
                return r
            elif method == "DELETE":
                r = requests.delete(self.HOST,params=params)
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
        data = self.args.format
        try:
            if data == "json":
                return f'{colorama.Fore.GREEN}RESPONSE:{self.response.status_code} {colorama.Fore.YELLOW}METHOD:{self.METHOD} {colorama.Fore.RESET}\n INFO:{self.response.json()}'
            elif data == "content":
                return f'{colorama.Fore.GREEN}RESPONSE:{self.response.status_code} {colorama.Fore.YELLOW}METHOD:{self.METHOD} {colorama.Fore.RESET}INFO:{self.response.content}'
            elif data == "text":
                return f'{colorama.Fore.GREEN}RESPONSE:{self.response.status_code} {colorama.Fore.YELLOW}METHOD:{self.METHOD} {colorama.Fore.RESET}INFO:{self.response.text}'
        except json.JSONDecodeError:
            return f'{self.response.text}'



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-format",type=str, default="text",help="Return data format.(json,conent,text)")
    parser.add_argument("-d",type=str,default=None, help="Data to send.Type JSON")
    parser.add_argument("-p",type=str, default=None, help="Shipping parameters.")
    parser.add_argument("-hds",type=str, default=None, help="Add headers to requests.")

    parser.add_argument("-u",type=str,help="Server requests.")
    parser.add_argument("-m",type=str, default="GET",help="Request method, default GET select (POST, DELETE, PUT,).")

    args = parser.parse_args()


    # Fast_Requests(args)
    from pprint import pprint
    pprint(Fast_Requests(args))


if __name__ == '__main__':
    colorama.init()

    main()


