import argparse
from base64 import b16encode
import http.client
import os
import ssl
from ssl import SSLContext, VerifyMode
from xml.etree import ElementTree

def create_ssl_context():
    ssl_context = SSLContext()
    ssl_context.verify_mode = VerifyMode.CERT_REQUIRED
    ssl_context.load_verify_locations(cafile="ww-np-dl-playstation-net-root.pem") # Load the CA certificate for Playsation servers
    return ssl_context

def split_url_to_parts(url):
    slash = url.index("/")
    
    host = url[0:slash]
    path = url[slash:]

    slash = url.rindex("/")
    filename = url[slash+1:]

    return host, path, filename

def request(url, path, verify = False):
    conn = http.client.HTTPSConnection(url, context = ( create_ssl_context() if verify else ssl._create_unverified_context() ))
    conn.request("GET", path)

    return conn.getresponse()

def download_package(outputFolder, package):
    host, path, filename = split_url_to_parts(package.get("url")[7:]) # Remove https://
    
    response = request(host, path, False) # Do not verify here, the certificate is invalid
    data = response.read()

    file = open(f"{outputFolder}/{filename}", "wb")
    file.write(data)
    file.close()

def get_file_size(size):
    if size < 1024:
        return f"{size} bytes"
    elif size < (1024*1024):
        return f"{int(size/1024)} KiBi"
    elif size < (1024*1024*1024):
        return f"{int(size/(1024*1024))} MiBi"
    else:
        return f"{int(size/(1024*1024*1024))} GiBi"
    
parser = argparse.ArgumentParser(prog='ps3updatedownloader', description='Download game updates from Playstation servers.')
parser.add_argument('titleid', nargs='+', help='PS3 titleid to download updates from')
parser.add_argument('-e', '--env', required=False, dest='env', default='np', help='Envionnement to download updates from')
parser.add_argument('-q', '--quiet', required=False, dest='quiet', action='store_true', help='Supress output')
parser.add_argument('-o', '--output', required=False, dest='outputFolder', action='store', default='updates', help='Specify output folder')

args = parser.parse_args()

for titleid in args.titleid:
    response = request(f"a0.ww.{args.env}.dl.playstation.net", f"/tpl/{args.env}/{titleid}/{titleid}-ver.xml", True)
    tree = ElementTree.fromstring(response.read())

    outputFolder = f"{args.outputFolder}/{titleid}"

    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    for package in tree.iter("package"):
        if not args.quiet:
            print(f"Downloading update {package.get('version')} for {titleid} ({get_file_size(int(package.get('size')))})")
        
        download_package(outputFolder, package)
