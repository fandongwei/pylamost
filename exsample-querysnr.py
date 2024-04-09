from pylamost import lamost
lm=lamost(dataset=8, version=2.0)#init the lamost class
#查询低分数据
params={'output.fmt':'csv','fmt':'csv','pos.type':'proximity','pos_type':'pos_proximity'}
tbl='combined'
for f in 'giruz':
    params['{0}_snr{1}'.format(tbl, f)]=True
    params['{0}.snr{1}'.format(tbl, f)]=True
files={'pos.posfile':('sample.txt', open('sample.txt', 'r'))}
files={'pos_posfile':('sample.txt', open('sample.txt', 'r'))}
low=lm.query2(params, files, ismed=False)
print(low)

#查询中分数据
params['med_combined.snr']=True
params['med_combined_snr']=True
files={'pos.posfile':('sample.txt', open('sample.txt', 'r'))}
files={'pos_posfile':('sample.txt', open('sample.txt', 'r'))}
med=lm.query2(params, files, ismed=True)
print(med)
