#!/usr/bin/env python
# coding: utf-8


from pylamost import lamost
lm=lamost(dr_version='dr10', sub_version='v2.0', is_dev=False)
lm.download_fits(obsid='101001',savedir='./',overwrite=True)
lm.download_png(obsid='101001',savedir='./',overwrite=True)
