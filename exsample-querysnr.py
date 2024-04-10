from pylamost import lamost
lm=lamost(dataset=11, version=1.0, is_dev=True)#init the lamost class
#查询低分数据
params={'output.fmt':'json','pos.type':'proximity'}
tbl='combined'
showcol=[]
for f in 'giruz':
    colname='{0}.snr{1}'.format(tbl, f)
    params[colname]=True #old way
    showcol.append(colname)#new way
params['showcol']=showcol
files={'pos.posfile':('sample.txt', open('sample.txt', 'r'))}
low=lm.query2(params, files, ismed=False)
print(low)

#查询中分数据
params['med_combined.snr']=True # old way
params['showcol']=['med_combined.snr'] # new way
files={'pos.posfile':('sample.txt', open('sample.txt', 'r'))}
med=lm.query2(params, files, ismed=True)
print(med)
