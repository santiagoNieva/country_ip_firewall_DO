import argparse
import requests
import os
import pickle
import vars
from bs4 import BeautifulSoup as bs

countries_choices = vars.countries_list.keys()
format_choices = vars.format_list.keys()

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
parser.add_argument("-l", "--list", help="Increase output verbosity", action="store_true")
parser.add_argument("-c", "--country_code", help="Check the vars.py file to get your country code", default="AR", choices=countries_choices, type=str)
parser.add_argument("-f", "--format_code", help="Check the vars.py file to get your format code", default="1", choices=format_choices,type=str)
parser.add_argument("-n", "--name", help="Choose the file that will be compared or created", default="old", type=str)
args = parser.parse_args()

def get_new_list(country='AR', format1='1', filename='old', verbose=False):
    """
        The function will get a Country short name, a format and a filename
        This function will go to https://www.countryipblocks.net/acl.php
        check the country selected and the format and ask for the list of IPs
        Once retrieved the IP BLOCKS it will compare them with your saved ones
        If they are not the same it will tell you and you will need to update it
        If you have no old file then it will create the first one for you.
    """
    if country not in countries_choices:
        print("You choose an incorrect country. Check for vars.py to get the complete list")
        return False

    if format1 not in format_choices:
        print("You choose an incorrect format. Check for vars.py to get the complete list")
        return False

    url = "https://www.countryipblocks.net/acl.php"

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0'}
    payload = {'countries[]': country, 'format1': format1, 'get_acl': 'Create+ACL'}

    print("Loading Page...    (Hope you have internet connection)") if verbose else None
    pagina = requests.post(url,data=payload,headers=headers)

    print("Parsing content...") if verbose else None
    sopa = bs(pagina.content,features="html.parser")

    texto = sopa.find(id="textareaAll").text

    listado = texto.replace(" ","").split("\n")

    if os.path.exists(filename):
        print("Comparing old file with the new ones...") if verbose else None
        with open(filename,'rb') as handle:
            actual = pickle.load(handle)

        if not listado == actual:
            print(f"SOMETHING HAS CHANGED -> NEW IP BLOCKS COUNT: {len(listado)} vs OLD IP BLOCKS COUNT{len(actual)}") if verbose else None
            for x in actual:
                if not x in listado:
                    print(x, "Is not found")

            print("\nReplacing old file with new one...") if verbose else None
            with open('old','wb') as handle:
                pickle.dump(listado,handle)

            print("\n\nThe file has been replaced, you should run the code 'refresh_firewall.py' to update the rules of your DO firewall.")
                
        else:
            print(f"SAME LIST -> {len(listado)} vs {len(actual)} ------> NO NEED FOR UPDATE")
    else:
        print(f'The File "{filename}" does not exists. [Actual directory: {os.getcwd()}]. Once created make sure to run refresh_firewall.py to update the rules of your DO firewall.')
        with open(filename,'wb') as handle:
            pickle.dump(listado,handle)
    
    return True

if __name__ == '__main__':
    if args.list:
        print("Country Codes: [-c]")
        for country_code,country_name in vars.countries_list.items():
            print(f" - {country_code} ----> {country_name}")
        
        print("\n\nCountry Codes: [-f]")
        for format_code,format_name in vars.format_list.items():
            print(f" - {format_code:2} ----> {format_name}")

        print("For Digital Ocean you should choose Format 1 or default")

    else:
        if args.verbose:
            print("Retrieving the IP Blocks. The parameters used are:")
            print(f"Country:  {args.country_code} -> [{vars.countries_list[args.country_code]}]")
            print(f"Format:   {args.format_code:2} -> [{vars.format_list[args.format_code]}]")
            print(f"Filename: {args.name}. (The actual directory is {os.getcwd()})\n")
        get_new_list(country=args.country_code, format1=args.format_code,filename=args.name,verbose=args.verbose)