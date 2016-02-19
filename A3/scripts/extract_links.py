# -*- coding: utf-8 -*-
import json 

fileN = open("link_info.json",'r')
data_set = json.loads(fileN.read())

fileN.close()

link_list = [] 

for key in data_set.keys():
	link_list.append(data_set[key]['link_info']['redirected_url'])

out = open("links.txt",'w')

for link in link_list:
	out.write(link)
	out.write('\n')

out.close()