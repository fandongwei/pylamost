from pylamost import lamost
lm=lamost(dataset=8, version=2.0)#init the lamost class
#查询低分数据
params={'output.fmt':'csv','pos.type':'proximity'}
params['output.combined.snrg']=True
params['output.combined.snri']=True
params['output.combined.snrr']=True
params['output.combined.snru']=True
params['output.combined.snrz']=True
files={'pos.posfile':('sample.txt', open('sample.txt', 'r'))}
low=lm.query2(params, files, ismed=False)
print(low)

#查询中分数据
params['output.med_combined.snr']=True
files={'pos.posfile':('sample.txt', open('sample.txt', 'r'))}
med=lm.query2(params, files, ismed=True)
print(med)
