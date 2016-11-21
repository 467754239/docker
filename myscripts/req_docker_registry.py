# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import os
import json
import requests
from requests.auth import HTTPBasicAuth
import texttable as tt


# Get all repositories
def get_all_repositories(url):
    cert_file = os.path.join( os.path.dirname('__init__'), 'certs/zhengyscn.crt')
    req = requests.get(url, auth=HTTPBasicAuth( os.environ.get('username'), os.environ.get('password') ), verify=cert_file)
    return json.loads(req.content)

# Get repositories's name and tags
def get_registry_info(repositories):
    repo_tag_list = []

    for repo in repositories:
        tag_url = "https://zhengyscn:5000/v2/{}/tags/list".format(repo)
    data = get_all_repositories(tag_url)
        repo_tag_list.append( [data.get('name'), ','.join( data.get('tags'))] )
    return repo_tag_list

# Format message
def format_output(data):
    tab = tt.Texttable()
    tab.add_rows(data)
    tab.set_cols_align(['r','r'])
    tab.header(['name', 'tag'])
    return tab.draw()

def main():
    url = 'https://zhengyscn:5000/v2/_catalog'

    # disable warning message
    requests.packages.urllib3.disable_warnings()

    str_repositories = get_all_repositories(url)
    repositories_dic = str_repositories.get("repositories")

    data = get_registry_info(repositories_dic)
    data.insert(0, [])
    print format_output(data)
   

if __name__ == '__main__':
    main()