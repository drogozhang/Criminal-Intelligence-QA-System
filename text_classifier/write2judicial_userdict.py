# -*- coding:utf-8 -*-
#
# Created by Drogo Zhang
#
# On 2018-11-11

import re

write_file = open("judicial_userdict_11_11_backup.txt", "w", encoding="utf-8")
read_all = open("judicial_userdict_11_11.txt", "r", encoding="utf-8").readlines()

for index in range(len(read_all)):
    read_all[index] = re.sub("\(201[4-8]\)", '', read_all[index])
    read_all[index] = re.sub("（201[4-8]）", '', read_all[index])
    read_all[index] = re.sub("〔201[4-8]〕", '', read_all[index])

for item in read_all:
    write_file.write(item)
