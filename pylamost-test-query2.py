#!/usr/bin/env python
# coding: utf-8


from pylamost import lamost
#lm=lamost(dataset=9, version=2.0, is_dev=False)
lm=lamost(dataset=10, version=2.0, is_dev=False)
# query low resolution catalog by ra,dec file
tbl='combined.'
params={
    'pos_group':'ra,dec',
    'output.fmt':'csv','pos.type':'proximity',
    'showcol':[tbl+'obsid', tbl+'ra', tbl+'dec']
    }
files={'pos.posfile':('sample.txt', open('sample.txt', 'r'))}
low=lm.query2(params, files)
print(low)

