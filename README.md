# DIGITAL OCEAN FIREWALL RULE ALLOW BY COUNTRY

This repository has 2 python codes, 
* ***get_new.py*** for retrieving the list of IPs from specific country
* ***refresh_firewall.py***  for updating the DigitalOcean Firewall to allow only this IPs.

## GET_NEW
The first code imports requests and BeautifulSoup to obtain and parse the specific country IPs

It visits https://www.countryipblocks.net/acl.php which has the lists we need

Once it obtains the list, it compares it with the last list we retrieve. If there is any changes,
then you will need to execute the second code *refresh_firewall.py* for updating the rules on DigitalOcean

The old list is replaced by the new one.

The list are saved into a pickle file.
If there is no old list, it will create the first one.)