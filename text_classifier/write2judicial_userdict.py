# -*- coding:utf-8 -*-
#
# Created by Drogo Zhang
#
# On 2018-11-11


write_file = open("judicial_userdict_11_11.txt", "a")

for year in range(1950, 2050):
    write_file.write(str(year)+"\n")

write_file.close()