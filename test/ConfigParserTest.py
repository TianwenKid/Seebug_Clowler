import configparser
import re

cf = configparser.ConfigParser()
cf.read('../seebug.cfg')

keywords_list = cf.get('seebug', 'keywords_list').split(',')
#cf.set('seebug', 'keywords_list', '1,2,3,4')
#cf.write(open('../seebug.cfg', 'w'))
print(keywords_list)
print(len(keywords_list))

dict = {'key1': 'value1', 'key2': 'value2'}
print(type(dict))
for value in dict:
    print(value)

keywords_last_ssvid = ""
for key, value in dict.items():
    print(key)
    print(value)
    keywords_last_ssvid += key + ':' + value + ", "
print(keywords_last_ssvid)

results = re.findall('(\w*?):(\w*)', keywords_last_ssvid)
dict = {}
print(type(dict))
for k, v in results:
    dict[k] = v


print(dict)