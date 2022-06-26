import configparser
import requests
import json
import ast
import colorama
import argparse
import sys

class Console_Requests:

    def __init__(self,args):
        # Define all args
        self.args = args
        self.dfile = self.args.dfile
        self.cfile = self.args.cfile
        self.HOST = self.get_host()
        self.METHOD = self.get_method()
        self.DATA = self.get_data()
        self.format = self.get_format()
        self.params = self.get_params()
        self.headers = self.get_headers()
        self.response = self._requests()

    def get_config_file(self,args):
        """
            Return configuration file.
        """
        config = configparser.ConfigParser()
        
        if config.read(args[0]):
            name_section = args[1].upper()
            config_to_dict = config._sections
            if name_section in config_to_dict:
                all_data_config = config_to_dict[name_section]
                try:
                    if 'data' in all_data_config:
                        all_data_config['data'] = ast.literal_eval(all_data_config['data'])
                        return all_data_config
                    elif 'file_data' in all_data_config:
                        all_data_config['data'] = self.read_file_json(all_data_config['file_data'])
                        return all_data_config
                except KeyError:
                    print(colorama.Fore.RED  + "Insert in the configuration file about data to send")
                    sys.exit()
            else:
                print(colorama.Fore.RED + 'Exception raised when a specified section is not found.')
                sys.exit()
        else:
            print(colorama.Fore.RED + f'Could not read file {args[0]}')
            sys.exit()
        

    def read_file_json(self, file):
        """
            Return read file json.
        """
        with open(file, 'r') as f:
            data_tojson = json.load(f)
            return data_tojson

    def get_data_file(self):
        """
            Return data in file json or file configuration.
        """
        if self.dfile:
            return self.read_file_json(self.dfile)
        elif self.cfile:
            data_tojson = self.get_config_file(self.cfile)
            return data_tojson
        else:
            return None

    def get_host(self):
        """
            Returns the host either json file, configuration file or inserted argument..
        """
        if self.dfile:
            host = self.get_data_file().get('url',None) or self.get_data_file().get('host',None) or self.get_data_file().get('server',None)
            return host
        elif self.cfile:
            host = self.get_data_file().get('url',None) or self.get_data_file().get('host',None) or self.get_data_file().get('server',None)
            return host
        
        return self.args.u

    def get_method(self):
        """
            Returns method json file, configuration file or inserted argument..
        """
        if self.dfile:
            method = self.get_data_file()['method'].upper()
            return method
        elif self.cfile:
            method = self.get_data_file()['method'].upper()
            return method
        return self.args.m.upper()

    def get_format(self):
        """
            Returns format data response json file, configuration file or inserted argument..
        """
        if self.get_data_file():
            return self.get_data_file().get('format')
        else:
            return self.args.format
    
    def get_params(self):
        """
            Returns params json file, configuration file or inserted argument..
        """
        params = self.get_data_file()
        if 'params' in params:
            return params['params']
        else:
            return self.args.p


    def get_data(self):
        """
            Returns params json file, configuration file or inserted argument..
        """
        if self.args.d:
            try:
                d = ast.literal_eval(self.args.d)
            except ValueError:
                print(colorama.Fore.RED  + "The data format is not correct. Fix data content.")
        elif self.dfile:
            d = self.get_data_file().get('data',dict())
        elif self.cfile:
            d = self.get_data_file().get('data',)
        else:
            d = self.args.d
        return d

    def get_headers(self):
        return self.args.hds or None


    def _requests(self):
        """
            Start requests to the server. return a response object
        """
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
                return f'{colorama.Fore.GREEN}STATUS_CODE:{self.response.status_code} {colorama.Fore.YELLOW}METHOD:{self.METHOD} {colorama.Fore.RESET}INFO:{self.response.json()}'
            elif f == "content":
                return f'{colorama.Fore.GREEN}STATUS_CODE:{self.response.status_code} {colorama.Fore.YELLOW}METHOD:{self.METHOD} {colorama.Fore.RESET}INFO:{self.response.content}'
            elif f == "text":
                return f'{colorama.Fore.GREEN}STATUS_CODE:{self.response.status_code} {colorama.Fore.YELLOW}METHOD:{self.METHOD} {colorama.Fore.RESET}INFO:{self.response.text}'
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
    parser.add_argument("-cfile",type=str, nargs="+", default=None, help="Config file with all data.")

    namespace,arr = parser.parse_known_args()
    if namespace.dfile==None and namespace.cfile == None:
        parser.add_argument("-u",type=str,required=True,help="Server requests.")
    else:
        parser.add_argument("-u",type=str,required=False,help="Server requests.")

    args = parser.parse_args()

    print(Console_Requests(args))


if __name__ == '__main__':
    colorama.init()

    main()


