from pylamost import lamost
import json
lm=lamost(dataset=11, version=1.0)#init the lamost class
sql='select * from combined limit 10'
ret=lm.sql(sql, fmt='json')
j = json.loads(ret)
print(j)
