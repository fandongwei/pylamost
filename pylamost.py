#!/usr/bin/python
# -*- coding: UTF-8 -*-
# packages needed: urllib.request, urllib.parse, requests, pyfits, numpy, scipy.signal
import os
import urllib.request
import urllib.parse
import requests
import astropy.io.fits
import numpy
import scipy.signal
import matplotlib.pyplot as plt
import json
import csv
import re
import io
import urllib.request
import sys
import astropy.io.votable as votable
import pandas as pd
from io import StringIO

pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

class lamost:
    def __init__(self, token=None, dataset=None, version=None):
        self.dataset=str(dataset)
        self.token=token
        self.version=str(version)
        self.__detectToken()
        self.__getDataset()
        self.__getVersion()

    __dr_set = {'1':[], '2':[], '3':[], '4': ['1', '2'], '5': ['0', '1', '2', '3'], '6': ['0', '1', '1.1', '2'], '7': ['0', '1', '1.1', '1.2', '1.3', '2.0'],
              '8': ['0', '1.0', '1.1', '2.0'], '9': ['0', '1.0', '1.1'], '10': ['0', '1.0'], '11': ['0']}

    __catalog_set = {'1':['dr1.fits.gz', 'dr1.csv.gz', 'dr1_stellar.fits.gz', 'dr1_stellar.csv.gz', 'dr1_a_stellar.fits.gz',
                          'dr1_a_stellar.csv.gz', 'dr1_m_stellar.fits.gz', 'dr1_m_stellar.csv.gz', 'dr1_plan.csv.gz'],
                     '2':['dr2.fits.gz', 'dr2.csv.gz', 'dr2_stellar.fits.gz', 'dr2_stellar.csv.gz', 'dr2_a_stellar.fits.gz',
                          'dr2_a_stellar.csv.gz', 'dr2_m_stellar.fits.gz', 'dr2_m_stellar.csv.gz', 'dr2_plan.csv.gz'],
                     '3':['dr3.fits.gz', 'dr3.csv.gz', 'dr3_stellar.fits.gz', 'dr3_stellar.csv.gz', 'dr3_a_stellar.fits.gz',
                          'dr3_a_stellar.csv.gz', 'dr3_m_stellar.fits.gz', 'dr3_m_stellar.csv.gz', 'dr3_plan.csv.gz'],
                     '4':{'v1':['dr3.fits.gz', 'dr3.csv.gz', 'dr3_stellar.fits.gz', 'dr3_stellar.csv.gz', 'dr3_a_stellar.fits.gz',
                          'dr3_a_stellar.csv.gz', 'dr3_m_stellar.fits.gz', 'dr3_m_stellar.csv.gz', 'dr3_plan.csv.gz', 'dr4_inputCatalog.txt.gz'],
                          'v2':['dr4_v2.fits.gz', 'dr4_v2.csv.gz', 'dr4_v2_stellar.fits.gz', 'dr4_v2_stellar.csv.gz', 'dr4_v2_a_stellar.fits.gz',
                                'dr4_v2_a_stellar.csv.gz', 'dr4_v2_m_stellar.fits.gz', 'dr4_v2_m_stellar.csv.gz', 'dr4_v2_plan.csv.gz', 'dr4_v2_inputCatalog.txt.gz']},
                     '5':{'0':['dr5_q1.fits.gz', 'dr5_q1.csv.gz', 'dr5_q2.fits.gz', 'dr5_q2.csv.gz', 'dr5_q3.fits.gz', 'dr5_q3.csv.gz', 'dr5_spec_alpha.fits.gz',
                                'dr5_spec_alpha.csv.gz', 'dr5_q1_stellar.fits.gz', 'dr5_q1_stellar.csv.gz', 'dr5_q2_stellar.fits.gz', 'dr5_q2_stellar.csv.gz',
                                'dr5_q3_stellar.fits.gz', 'dr5_q3_stellar.csv.gz', 'dr5_stellar_alpha.fits.gz', 'dr5_stellar_alpha.csv.gz', 'dr5_q1_plan.csv.gz',
                                'dr5_q2_plan.csv.gz', 'dr5_q3_plan.csv.gz', 'dr5_plan_alpha.csv.gz', 'dr5_q1_inputCatalog.csv.gz', 'dr5_q2_inputCatalog.csv.gz',
                                'dr5_q3_inputCatalog.csv.gz'],
                          '1':['dr5_v1.fits.gz', 'dr5_v1.csv.gz', 'dr5_v1_stellar.fits.gz', 'dr5_v1_stellar.csv.gz', 'dr5_v1_a_stellar.fits.gz', 'dr5_v1_a_stellar.csv.gz',
                                'dr5_v1_m_stellar.fits.gz', 'dr5_v1_m_stellar.csv.gz', 'dr5_v1_plan.csv.gz', 'dr5_v1_inputCatalog.txt.gz'],
                          '2':['dr5_v2.fits.gz', 'dr5_v2.csv.gz', 'dr5_v2_stellar.fits.gz', 'dr5_v2_stellar.csv.gz', 'dr5_v2_a_stellar.fits.gz', 'dr5_v2_a_stellar.csv.gz',
                                'dr5_v2_m_stellar.fits.gz', 'dr5_v2_m_stellar.csv.gz', 'dr5_v2_plan.csv.gz', 'dr5_v2_inputCatalog.txt.gz'],
                          '3':['dr5_v3.fits.gz', 'dr5_v3.csv.gz', 'dr5_v3_stellar.fits.gz', 'dr5_v3_stellar.csv.gz', 'dr5_v3_a_stellar.fits.gz', 'dr5_v3_a_stellar.csv.gz',
                                'dr5_v3_m_stellar.fits.gz', 'dr5_v3_m_stellar.csv.gz', 'dr5_v3_plan.csv.gz', 'dr5_v3_inputCatalog.txt.gz']
                          },
                     '6':{'0':['dr6_v0_q1.fits.gz', 'dr6_v0_q1.csv.gz', 'dr6_v0_q2.fits.gz', 'dr6_v0_q2.csv.gz', 'dr6_v0_q3.fits.gz', 'dr6_v0_q3.csv.gz', 'dr6_v0.fits.gz',
                                'dr6_v0.csv.gz', 'dr6_v0_q1_stellar.fits.gz', 'dr6_v0_q1_stellar.csv.gz', 'dr6_v0_q2_stellar.fits.gz', 'dr6_v0_q2_stellar.csv.gz',
                                'dr6_v0_q3_stellar.fits.gz', 'dr6_v0_q3_stellar.csv.gz', 'dr6_v0_stellar.fits.gz', 'dr6_v0_stellar.csv.gz', 'dr6_v0_q1_plan.csv.gz',
                                'dr6_v0_q2_plan.csv.gz', 'dr6_v0_q3_plan.csv.gz', 'dr6_v0_plan.csv.gz', 'dr6_v0_q1_inputCatalog.txt.gz', 'dr6_v0_q2_inputCatalog.txt.gz',
                                'dr6_v0_q3_inputCatalog.txt.gz', 'dr6_v0_inputCatalog.txt.gz'],
                          '1':['dr6_v1_LSR.fits.gz', 'dr6_v1_LSR.csv.gz', 'dr6_v1_stellar_LSR.fits.gz', 'dr6_v1_stellar_LSR.csv.gz', 'dr6_v1_a_stellar_LSR.fits.gz',
                                'dr6_v1_a_stellar_LSR.csv.gz', 'dr6_v1_m_stellar_LSR.fits.gz', 'dr6_v1_m_stellar_LSR.csv.gz', 'dr6_v1_plan_LSR.csv.gz', 'dr6_inputCatalog_LSR.txt.gz',
                                'dr6_v1_MSR.fits.gz', 'dr6_v1_MSR.csv.gz', 'dr6_v1_stellar_MSR.fits.gz', 'dr6_v1_stellar_MSR.csv.gz', 'dr6_v1_plan_MSR.csv.gz',
                                'dr6_inputCatalog_MSR.txt.gz'],
                          '1.1':['dr6_v1.1_LSR.fits.gz', 'dr6_v1.1_LSR.csv.gz', 'dr6_v1.1_stellar_LSR.fits.gz', 'dr6_v1.1_stellar_LSR.csv.gz', 'dr6_v1.1_a_stellar_LSR.fits.gz',
                                'dr6_v1.1_a_stellar_LSR.csv.gz', 'dr6_v1.1_m_stellar_LSR.fits.gz', 'dr6_v1.1_m_stellar_LSR.csv.gz', 'dr6_v1.1_plan_LSR.csv.gz', 'dr6_inputCatalog_v1.1_LRS.txt.gz',
                                'dr6_med_v1.1_MRS.fits.gz', 'dr6_med_v1.1_MRS.csv.gz', 'dr6_med_v1.1_stellar_MRS.fits.gz', 'dr6_med_v1.1_stellar_MRS.csv.gz', 'dr6_med_v1.1_plan_MRS.csv.gz',
                                'dr6_inputCatalog_v1.1_MRS.txt.gz'],
                          '2':['dr6_v2_LSR.fits.gz', 'dr6_v2_LSR.csv.gz', 'dr6_v2_stellar_LSR.fits.gz', 'dr6_v2_stellar_LSR.csv.gz', 'dr6_v2_a_stellar_LSR.fits.gz',
                                'dr6_v2_a_stellar_LSR.csv.gz', 'dr6_v2_m_stellar_LSR.fits.gz', 'dr6_v2_m_stellar_LSR.csv.gz', 'dr6_v2_plan_LSR.csv.gz', 'dr6_inputCatalog_v2_LRS.txt.gz',
                                'dr6_med_v2_MRS.fits.gz', 'dr6_med_v2_MRS.csv.gz', 'dr6_med_v2_stellar_MRS.fits.gz', 'dr6_med_v2_stellar_MRS.csv.gz', 'dr6_med_v2_plan_MRS.csv.gz',
                                'dr6_inputCatalog_v2_MRS.txt.gz']
                          },
                     '7':{'0':['dr7_v0_q1.fits.gz', 'dr7_v0_q1.csv.gz', 'dr7_v0_q2.fits.gz', 'dr7_v0_q2.csv.gz', 'dr7_v0_q3.fits.gz', 'dr7_v0_q3.csv.gz', 'dr7_v0_q1_stellar.fits.gz',
                                'dr7_v0_q1_stellar.csv.gz', 'dr7_v0_q2_stellar.fits.gz', 'dr7_v0_q2_stellar.csv.gz','dr7_v0_q3_stellar.fits.gz', 'dr7_v0_q3_stellar.csv.gz', 'dr7_v0_q1_plan.csv.gz',
                                'dr7_v0_q2_plan.csv.gz', 'dr7_v0_q3_plan.csv.gz', 'dr7_v0_q1_inputCatalog.txt.gz', 'dr7_v0_q2_inputCatalog.txt.gz','dr7_v0_q3_inputCatalog.txt.gz',
                                'dr7_v0_inputCatalog.txt.gz', 'dr7_med_v0_q1.fits.gz', 'dr7_med_v0_q1.csv.gz', 'dr7_med_v0_q2.fits.gz', 'dr7_med_v0_q2.csv.gz', 'dr7_med_v0_q3.fits.gz', 'dr7_med_v0_q3.csv.gz',
                                'dr7_med_v0_q1_stellar.fits.gz', 'dr7_med_v0_q1_stellar.csv.gz', 'dr7_med_v0_q2_stellar.fits.gz', 'dr7_med_v0_q2_stellar.csv.gz', 'dr7_med_v0_q3_stellar.fits.gz', 'dr7_med_v0_q3_stellar.csv.gz',
                                'dr7_med_v0_q1_plan.csv.gz', 'dr7_med_v0_q2_plan.csv.gz', 'dr7_med_v0_q3_plan.csv.gz', 'dr7_v0_med_q1_inputCatalog.txt.gz', 'dr7_v0_med_q2_inputCatalog.txt.gz', 'dr7_v0_med_q3_inputCatalog.txt.gz'],
                          '1':['dr7_v1.fits.gz', 'dr7_v1.csv.gz', 'dr7_v1_stellar.fits.gz', 'dr7_v1_stellar.csv.gz', 'dr7_v1_astellar.fits.gz', 'dr7_v1_astellar.csv.gz', 'dr7_v1_mstellar.fits.gz', 'dr7_v1_mstellar.csv.gz',
                                'dr7_v1_plan.csv.gz', 'dr7_inputCatalog_LRS_v1.txt.gz', 'dr7_med_v1.fits.gz', 'dr7_med_v1.csv.gz', 'dr7_med_v1_stellar.fits.gz', 'dr7_med_v1_stellar.csv.gz', 'dr7_med_v1_plan.csv.gz', 'dr7_inputCatalog_MRS_v1.txt.gz'],
                          '1.1':['dr7_v1.1.fits.gz', 'dr7_v1.1.csv.gz', 'dr7_v1.1_stellar.fits.gz', 'dr7_v1.1_stellar.csv.gz', 'dr7_v1.1_astellar.fits.gz', 'dr7_v1.1_astellar.csv.gz', 'dr7_v1.1_mstellar.fits.gz', 'dr7_v1.1_mstellar.csv.gz',
                                'dr7_v1.1_plan.csv.gz', 'dr7_inputCatalog_LRS_v1.1.txt.gz', 'dr7_med_v1.1.fits.gz', 'dr7_med_v1.1.csv.gz', 'dr7_med_v1.1_stellar.fits.gz', 'dr7_med_v1.1_stellar.csv.gz', 'dr7_med_v1.1_plan.csv.gz', 'dr7_inputCatalog_MRS_v1.1.txt.gz'],
                          '1.2':['dr7_v1.2.fits.gz', 'dr7_v1.2.csv.gz', 'dr7_v1.2_stellar.fits.gz', 'dr7_v1.2_stellar.csv.gz', 'dr7_v1.2_astellar.fits.gz', 'dr7_v1.2_astellar.csv.gz', 'dr7_v1.2_mstellar.fits.gz', 'dr7_v1.2_mstellar.csv.gz',
                                  'dr7_v1.2_plan.csv.gz', 'dr7_inputCatalog_v1.2_LRS.txt.gz', 'dr7_v1.2_mec.csv.gz', 'dr7_med_v1.2.fits.gz', 'dr7_med_v1.2.csv.gz', 'dr7_med_v1.2_stellar.fits.gz', 'dr7_med_v1.2_stellar.csv.gz',
                                  'dr7_med_v1.2_plan.csv.gz', 'dr7_inputCatalog_v1.2_MRS.txt.gz'],
                          '1.3':['dr7_v1.3_catalogue_LRS.fits.gz', 'dr7_v1.3_catalogue_LRS.csv.gz', 'dr7_v1.3_stellar_LRS.fits.gz', 'dr7_v1.3_stellar_LRS.csv.gz', 'dr7_v1.3_astellar_LRS.fits.gz', 'dr7_v1.3_astellar_LRS.csv.gz',
                                  'dr7_v1.3_mstellar_LRS.fits.gz', 'dr7_v1.3_mstellar_LRS.csv.gz', 'dr7_v1.3_plan_LRS.fits.gz', 'dr7_v1.3_plan_LRS.csv.gz', 'dr7_v1.3_inputcatalog_LRS.fits.gz', 'dr7_v1.3_inputcatalog_LRS.csv.gz',
                                  'dr7_v1.3_mec_LRS.fits.gz', 'dr7_v1.3_mec_LRS.csv.gz', 'dr7_med_v1.3_catalogue_MRS.fits.gz', 'dr7_med_v1.3_catalogue_MRS.csv.gz', 'dr7_med_v1.3_stellar_MRS.fits.gz', 'dr7_med_v1.3_stellar_MRS.csv.gz',
                                  'dr7_med_v1.3_plan_MRS.fits.gz', 'dr7_med_v1.3_plan_MRS.csv.gz', 'dr7_med_v1.3_inputcatalog_MRS.fits.gz', 'dr7_med_v1.3_inputcatalog_MRS.csv.gz'],
                          '2':['dr7_v2.0_LRS_catalogue.fits.gz', 'dr7_v2.0_LRS_catalogue.csv.gz', 'dr7_v2.0_LRS_stellar.fits.gz', 'dr7_v2.0_LRS_stellar.csv.gz', 'dr7_v2.0_LRS_astellar.fits.gz', 'dr7_v2.0_LRS_astellar.csv.gz', 'dr7_v2.0_LRS_mstellar.fits.gz',
                                'dr7_v2.0_LRS_mstellar.csv.gz', 'dr7_v2.0_LRS_plan.fits.gz', 'dr7_v2.0_LRS_plan.csv.gz', 'dr7_v2.0_LRS_inputcatalog.fits.gz', 'dr7_v2.0_LRS_inputcatalog.csv.gz', 'dr7_v2.0_LRS_mec.fits.gz', 'dr7_v2.0_LRS_mec.csv.gz', 'dr7_v2.0_LRS_cv.fits.gz',
                                'dr7_v2.0_LRS_cv.csv.gz', 'dr7_v2.0_LRS_wd.fits.gz', 'dr7_v2.0_LRS_wd.csv.gz', 'dr7_v2.0_MRS_catalogue.fits.gz', 'dr7_v2.0_MRS_catalogue.csv.gz', 'dr7_v2.0_MRS_stellar.fits.gz', 'dr7_v2.0_MRS_stellar.csv.gz', 'dr7_v2.0_MRS_stellar.fits.gz',
                                'dr7_v2.0_MRS_stellar.csv.gz', 'dr7_v2.0_MRS_inputcatalog.fits.gz', 'dr7_v2.0_MRS_inputcatalog.csv.gz'],
                          },
                     '8':{'0':['dr8_v0_q1.fits.gz', 'dr8_v0_q1.csv.gz', 'dr8_v0_q2.fits.gz', 'dr8_v0_q2.csv.gz', 'dr8_v0_q3.fits.gz', 'dr8_v0_q3.csv.gz', 'dr8_v0_q1_stellar.fits.gz', 'dr8_v0_q1_stellar.csv.gz', 'dr8_v0_q2_stellar.fits.gz', 'dr8_v0_q2_stellar.csv.gz', 'dr8_v0_q3_stellar.fits.gz',
                                'dr8_v0_q3_stellar.csv.gz', 'dr8_v0_q1_plan.csv.gz', 'dr8_v0_q2_plan.csv.gz', 'dr8_v0_q3_plan.csv.gz', 'dr8_v0_q1_inputCatalog.txt.gz', 'dr8_v0_q2_inputCatalog.txt.gz', 'dr8_v0_q3_inputCatalog.txt.gz', 'dr8_med_v0_q1.fits.gz', 'dr8_med_v0_q1.csv.gz', 'dr8_med_v0_q2.fits.gz',
                                'dr8_med_v0_q2.csv.gz', 'dr8_med_v0_q3.fits.gz', 'dr8_med_v0_q3.csv.gz', 'dr8_med_v0_q1_stellar.fits.gz', 'dr8_med_v0_q1_stellar.csv.gz', 'dr8_med_v0_q2_stellar.fits.gz', 'dr8_med_v0_q2_stellar.csv.gz', 'dr8_med_v0_q3_stellar.fits.gz', 'dr8_med_v0_q3_stellar.csv.gz',
                                'dr8_med_v0_q1_plan.csv.gz', 'dr8_med_v0_q2_plan.csv.gz', 'dr8_med_v0_q3_plan.csv.gz', 'dr8_v0_med_q1_inputCatalog.txt.gz', 'dr8_v0_med_q2_inputCatalog.txt.gz', 'dr8_v0_med_q3_inputCatalog.txt.gz'],
                          '1.0':['dr8_v1.0_catalogue_LRS.fits.gz', 'dr8_v1.0_catalogue_LRS.csv.gz', 'dr8_v1.0_stellar_LRS.fits.gz', 'dr8_v1.0_stellar_LRS.csv.gz', 'dr8_v1.0_astellar_LRS.fits.gz', 'dr8_v1.0_astellar_LRS.csv.gz','dr8_v1.0_mstellar_LRS.fits.gz', 'dr8_v1.0_mstellar_LRS.csv.gz',
                                  'dr8_v1.0_plan_LRS.fits.gz', 'dr8_v1.0_plan_LRS.csv.gz', 'dr8_v1.0_inputcatalog_LRS.fits.gz', 'dr8_v1.0_inputcatalog_LRS.csv.gz', 'dr8_v1.0_LRS_mec.fits.gz', 'dr8_v1.0_LRS_mec.csv.gz', 'dr8_med_v1.0_catalogue_MRS.fits.gz', 'dr8_med_v1.0_catalogue_MRS.csv.gz',
                                  'dr8_med_v1.0_stellar_MRS.fits.gz', 'dr8_med_v1.0_stellar_MRS.csv.gz', 'dr8_med_v1.0_plan_MRS.fits.gz', 'dr8_med_v1.0_plan_MRS.csv.gz', 'dr8_med_v1.0_inputcatalog_MRS.fits.gz', 'dr8_med_v1.0_inputcatalog_MRS.csv.gz'],
                          '1.1':['dr8_v1.1_LRS_catalogue.fits.gz', 'dr8_v1.1_LRS_catalogue.csv.gz', 'dr8_v1.1_LRS_stellar.fits.gz', 'dr8_v1.1_LRS_stellar.csv.gz', 'dr8_v1.1_LRS_astellar.fits.gz', 'dr8_v1.1_LRS_astellar.csv.gz', 'dr8_v1.1_LRS_mstellar.fits.gz', 'dr8_v1.1_LRS_mstellar.csv.gz',
                                  'dr8_v1.1_LRS_mec.fits.gz', 'dr8_v1.1_LRS_mec.csv.gz', 'dr8_v1.1_LRS_plan.fits.gz', 'dr8_v1.1_LRS_plan.csv.gz', 'dr8_v1.1_LRS_inputcatalog.fits.gz', 'dr8_v1.1_LRS_inputcatalog.csv.gz', 'dr8_v1.1_LRS_cv.fits.gz', 'dr8_v1.1_LRS_cv.csv.gz', 'dr8_v1.1_LRS_wd.fits.gz',
                                  'dr8_v1.1_LRS_wd.csv.gz', 'dr8_v1.1_LRS_qso.fits.gz', 'dr8_v1.1_LRS_qso.csv.gz', 'dr8_v1.1_LRS_galaxy.fits.gz', 'dr8_v1.1_LRS_galaxy.csv.gz', 'dr8_v1.1_MRS_catalogue.fits.gz', 'dr8_v1.1_MRS_catalogue.csv.gz', 'dr8_v1.1_MRS_stellar.fits.gz', 'dr8_v1.1_MRS_stellar.csv.gz',
                                  'dr8_v1.1_MRS_mec.fits.gz', 'dr8_v1.1_MRS_mec.csv.gz', 'dr8_v1.1_MRS_plan.fits.gz', 'dr8_v1.1_MRS_plan.csv.gz', 'dr8_v1.1_MRS_inputcatalog.fits.gz', 'dr8_v1.1_MRS_inputcatalog.csv.gz'],
                          '2.0':['dr8_v2.0_LRS_catalogue.fits.gz', 'dr8_v2.0_LRS_catalogue.csv.gz', 'dr8_v2.0_LRS_stellar.fits.gz', 'dr8_v2.0_LRS_stellar.csv.gz', 'dr8_v2.0_LRS_astellar.fits.gz', 'dr8_v2.0_LRS_astellar.csv.gz', 'dr8_v2.0_LRS_mstellar.fits.gz', 'dr8_v2.0_LRS_mstellar.csv.gz',
                                  'dr8_v2.0_LRS_mec.fits.gz', 'dr8_v2.0_LRS_mec.csv.gz', 'dr8_v2.0_LRS_plan.fits.gz', 'dr8_v2.0_LRS_plan.csv.gz', 'dr8_v2.0_LRS_inputcatalog.fits.gz', 'dr8_v2.0_LRS_inputcatalog.csv.gz', 'dr8_v2.0_LRS_cv.fits.gz', 'dr8_v2.0_LRS_cv.csv.gz', 'dr8_v2.0_LRS_wd.fits.gz',
                                  'dr8_v2.0_LRS_wd.csv.gz', 'dr8_v2.0_LRS_qso.fits.gz', 'dr8_v2.0_LRS_qso.csv.gz', 'dr8_v2.0_LRS_galaxy.fits.gz', 'dr8_v2.0_LRS_galaxy.csv.gz', 'dr8_v2.0_MRS_catalogue.fits.gz', 'dr8_v2.0_MRS_catalogue.csv.gz', 'dr8_v2.0_MRS_stellar.fits.gz', 'dr8_v2.0_MRS_stellar.csv.gz',
                                  'dr8_v2.0_MRS_mec.fits.gz', 'dr8_v2.0_MRS_mec.csv.gz', 'dr8_v2.0_MRS_plan.fits.gz', 'dr8_v2.0_MRS_plan.csv.gz', 'dr8_v2.0_MRS_inputcatalog.fits.gz', 'dr8_v2.0_MRS_inputcatalog.csv.gz']
                          },
                     '9':{'0':['dr9_v0_q1_LRS_catalogue.fits.gz', 'dr9_v0_q1_LRS_catalogue.csv.gz', 'dr9_v0_q2_LRS_catalogue.fits.gz', 'dr9_v0_q2_LRS_catalogue.csv.gz', 'dr9_v0_q3_LRS_catalogue.fits.gz', 'dr9_v0_q3_LRS_catalogue.csv.gz', 'dr9_v0_q1q2_LRS_catalogue.fits.gz', 'dr9_v0_q1q2_LRS_catalogue.csv.gz', 'dr9_v0_q1q2q3_LRS_catalogue.fits.gz', 'dr9_v0_q1q2q3_LRS_catalogue.csv.gz',
                                'dr9_v0_q1_LRS_stellar.fits.gz', 'dr9_v0_q1_LRS_stellar.csv.gz', 'dr9_v0_q2_LRS_stellar.fits.gz', 'dr9_v0_q2_LRS_stellar.csv.gz', 'dr9_v0_q3_LRS_stellar.fits.gz', 'dr9_v0_q3_LRS_stellar.csv.gz', 'dr9_v0_q1q2_LRS_stellar.fits.gz', 'dr9_v0_q1q2_LRS_stellar.csv.gz', 'dr9_v0_q1q2q3_LRS_stellar.fits.gz', 'dr9_v0_q1q2q3_LRS_stellar.csv.gz',
                                'dr9_v0_q1_LRS_plan.fits.gz', 'dr9_v0_q1_LRS_plan.csv.gz', 'dr9_v0_q2_LRS_plan.fits.gz', 'dr9_v0_q2_LRS_plan.csv.gz', 'dr9_v0_q3_LRS_plan.fits.gz', 'dr9_v0_q3_LRS_plan.csv.gz', 'dr9_v0_q1q2_LRS_plan.fits.gz', 'dr9_v0_q1q2_LRS_plan.csv.gz', 'dr9_v0_q1q2q3_LRS_plan.fits.gz', 'dr9_v0_q1q2q3_LRS_plan.csv.gz',
                                'dr9_v0_q1_LRS_inputcatalog.fits.gz', 'dr9_v0_q1_LRS_inputcatalog.csv.gz', 'dr9_v0_q2_LRS_inputcatalog.fits.gz', 'dr9_v0_q2_LRS_inputcatalog.csv.gz', 'dr9_v0_q3_LRS_inputcatalog.fits.gz', 'dr9_v0_q3_LRS_inputcatalog.csv.gz', 'dr9_v0_q1q2_LRS_inputcatalog.fits.gz', 'dr9_v0_q1q2_LRS_inputcatalog.csv.gz', 'dr9_v0_q1q2q3_LRS_inputcatalog.fits.gz', 'dr9_v0_q1q2q3_LRS_inputcatalog.csv.gz'],
                          '1.0':['dr9_v1.0_LRS_catalogue.fits.gz', 'dr9_v1.0_LRS_catalogue.csv.gz', 'dr9_v1.0_LRS_stellar.fits.gz', 'dr9_v1.0_LRS_stellar.csv.gz', 'dr9_v1.0_LRS_astellar.fits.gz', 'dr9_v1.0_LRS_astellar.csv.gz', 'dr9_v1.0_LRS_mstellar.fits.gz', 'dr9_v1.0_LRS_mstellar.csv.gz',
                                  'dr9_v1.0_LRS_mec.fits.gz', 'dr9_v1.0_LRS_mec.csv.gz', 'dr9_v1.0_LRS_plan.fits.gz', 'dr9_v1.0_LRS_plan.csv.gz', 'dr9_v1.0_LRS_inputcatalog.fits.gz', 'dr9_v1.0_LRS_inputcatalog.csv.gz', 'dr9_v1.0_LRS_cv.fits.gz', 'dr9_v1.0_LRS_cv.csv.gz', 'dr9_v1.0_LRS_wd.fits.gz',
                                  'dr9_v1.0_LRS_wd.csv.gz', 'dr9_v1.0_LRS_qso.fits.gz', 'dr9_v1.0_LRS_qso.csv.gz', 'dr9_v1.0_LRS_galaxy.fits.gz', 'dr9_v1.0_LRS_galaxy.csv.gz', 'dr9_v1.0_MRS_catalogue.fits.gz', 'dr9_v1.0_MRS_catalogue.csv.gz', 'dr9_v1.0_MRS_stellar.fits.gz', 'dr9_v1.0_MRS_stellar.csv.gz',
                                  'dr9_v1.0_MRS_mec.fits.gz', 'dr9_v1.0_MRS_mec.csv.gz', 'dr9_v1.0_MRS_plan.fits.gz', 'dr9_v1.0_MRS_plan.csv.gz', 'dr9_v1.0_MRS_inputcatalog.fits.gz', 'dr9_v1.0_MRS_inputcatalog.csv.gz'],
                          '1.1':['dr9_v1.1_LRS_catalogue.fits.gz', 'dr9_v1.1_LRS_catalogue.csv.gz', 'dr9_v1.1_LRS_stellar.fits.gz', 'dr9_v1.1_LRS_stellar.csv.gz', 'dr9_v1.1_LRS_astellar.fits.gz', 'dr9_v1.1_LRS_astellar.csv.gz', 'dr9_v1.1_LRS_mstellar.fits.gz', 'dr9_v1.1_LRS_mstellar.csv.gz',
                                  'dr9_v1.1_LRS_mec.fits.gz', 'dr9_v1.1_LRS_mec.csv.gz', 'dr9_v1.1_LRS_plan.fits.gz', 'dr9_v1.1_LRS_plan.csv.gz', 'dr9_v1.1_LRS_inputcatalog.fits.gz', 'dr9_v1.1_LRS_inputcatalog.csv.gz', 'dr9_v1.1_LRS_cv.fits.gz', 'dr9_v1.1_LRS_cv.csv.gz', 'dr9_v1.1_LRS_wd.fits.gz',
                                  'dr9_v1.1_LRS_wd.csv.gz', 'dr9_v1.1_LRS_qso.fits.gz', 'dr9_v1.1_LRS_qso.csv.gz', 'dr9_v1.1_LRS_galaxy.fits.gz', 'dr9_v1.1_LRS_galaxy.csv.gz', 'dr9_v1.1_MRS_catalogue.fits.gz', 'dr9_v1.1_MRS_catalogue.csv.gz', 'dr9_v1.1_MRS_stellar.fits.gz', 'dr9_v1.1_MRS_stellar.csv.gz',
                                  'dr9_v1.1_MRS_mec.fits.gz', 'dr9_v1.1_MRS_mec.csv.gz', 'dr9_v1.1_MRS_plan.fits.gz', 'dr9_v1.1_MRS_plan.csv.gz', 'dr9_v1.1_MRS_inputcatalog.fits.gz', 'dr9_v1.1_MRS_inputcatalog.csv.gz']
                          },
                     '10':{'0':['dr10_v0_LRS_catalogue_q1.fits.gz', 'dr10_v0_LRS_catalogue_q1.csv.gz', 'dr10_v0_LRS_catalogue_q2.fits.gz', 'dr10_v0_LRS_catalogue_q1.csv.gz', 'dr10_v0_LRS_catalogue_q3.fits.gz', 'dr10_v0_LRS_catalogue_q3.csv.gz', 'dr10_v0_LRS_catalogue_q1q2.fits.gz', 'dr10_v0_LRS_catalogue_q1q2.csv.gz', 'dr10_v0_LRS_catalogue_q1q2q3.fits.gz', 'dr10_v0_LRS_catalogue_q1q2q3.csv.gz',
                                 'dr10_v0_LRS_stellar_q1.fits.gz', 'dr10_v0_LRS_stellar_q1.csv.gz', 'dr10_v0_LRS_stellar_q2.fits.gz', 'dr10_v0_LRS_stellar_q2.csv.gz', 'dr10_v0_LRS_stellar_q3.fits.gz', 'dr10_v0_LRS_stellar_q3.csv.gz', 'dr10_v0_LRS_stellar_q1q2.fits.gz', 'dr10_v0_LRS_stellar_q1q2.csv.gz', 'dr10_v0_LRS_stellar_q1q2q3.fits.gz', 'dr10_v0_LRS_stellar_q1q2q3.csv.gz',
                                 'dr10_v0_LRS_plan_q1.fits.gz', 'dr10_v0_LRS_plan_q1.csv.gz', 'dr10_v0_LRS_plan_q2.fits.gz', 'dr10_v0_LRS_plan_q2.csv.gz', 'dr10_v0_LRS_plan_q3.fits.gz', 'dr10_v0_LRS_plan_q3.csv.gz', 'dr10_v0_LRS_plan_q1q2.fits.gz', 'dr10_v0_LRS_plan_q1q2.csv.gz', 'dr10_v0_LRS_plan_q1q2q3.fits.gz', 'dr10_v0_LRS_plan_q1q2q3.csv.gz',
                                 'dr10_v0_LRS_q1_inputcatalog.fits.gz', 'dr10_v0_LRS_q1_inputcatalog.csv.gz', 'dr10_v0_LRS_q2_inputcatalog.fits.gz', 'dr10_v0_LRS_q2_inputcatalog.csv.gz', 'dr10_v0_LRS_q3_inputcatalog.fits.gz', 'dr10_v0_LRS_q3_inputcatalog.csv.gz', 'dr10_v0_LRS_inputcatalog_q1q2.fits.gz', 'dr10_v0_LRS_inputcatalog_q1q2.csv.gz', 'dr10_v0_LRS_inputcatalog_q1q2q3.fits.gz', 'dr10_v0_LRS_inputcatalog_q1q2q3.csv.gz'],
                           '1.0':['dr10_v1.0_LRS_catalogue.fits.gz', 'dr10_v1.0_LRS_catalogue.csv.gz', 'dr10_v1.0_LRS_stellar.fits.gz', 'dr10_v1.0_LRS_stellar.csv.gz', 'dr10_v1.0_LRS_astellar.fits.gz', 'dr10_v1.0_LRS_astellar.csv.gz', 'dr10_v1.0_LRS_mstellar.fits.gz', 'dr10_v1.0_LRS_mstellar.csv.gz',
                                  'dr10_v1.0_LRS_mec.fits.gz', 'dr10_v1.0_LRS_mec.csv.gz', 'dr10_v1.0_LRS_plan.fits.gz', 'dr10_v1.0_LRS_plan.csv.gz', 'dr10_v1.0_LRS_inputcatalog.fits.gz', 'dr10_v1.0_LRS_inputcatalog.csv.gz', 'dr10_v1.0_LRS_cv.fits.gz', 'dr10_v1.0_LRS_cv.csv.gz', 'dr10_v1.0_LRS_wd.fits.gz',
                                  'dr10_v1.0_LRS_wd.csv.gz', 'dr10_v1.0_LRS_qso.fits.gz', 'dr10_v1.0_LRS_qso.csv.gz', 'dr10_v1.0_LRS_galaxy.fits.gz', 'dr10_v1.0_LRS_galaxy.csv.gz', 'dr10_v1.0_MRS_catalogue.fits.gz', 'dr10_v1.0_MRS_catalogue.csv.gz', 'dr10_v1.0_MRS_stellar.fits.gz', 'dr10_v1.0_MRS_stellar.csv.gz',
                                  'dr10_v1.0_MRS_mec.fits.gz', 'dr10_v1.0_MRS_mec.csv.gz', 'dr10_v1.0_MRS_plan.fits.gz', 'dr10_v1.0_MRS_plan.csv.gz', 'dr10_v1.0_MRS_inputcatalog.fits.gz', 'dr10_v1.0_MRS_inputcatalog.csv.gz']
                           },
                     '11':{'0':['dr11_v0_LRS_catalogue_q1.fits.gz', 'dr11_v0_LRS_catalogue_q1.csv.gz', 'dr11_v0_LRS_stellar_q1.fits.gz', 'dr11_v0_LRS_stellar_q1.csv.gz', 'dr11_v0_LRS_plan_q1.fits.gz', 'dr11_v0_LRS_plan_q1.csv.gz', 'dr11_v0_LRS_q1_inputcatalog.fits.gz', 'dr11_v0_LRS_q1_inputcatalog.csv.gz']}
                     }

    def __getDataset(self):
        if self.dataset not in self.__dr_set:
            raise Exception("The dataset you provided does not exist!")
        else:
            return f'{self.dataset}'

    def __getVersion(self):
        if self.dataset in ['1', '2', '3']:
            if self.version == 'None':
                return ''
            else:
                raise Exception("There is no version of this dataset!")
        else:
            if self.version == 'None':
                raise Exception("The data version is not filled in correctly!")
            else:
                if self.dataset in self.__dr_set and self.version in self.__dr_set[self.dataset]:
                    return f'{self.version}'
                else:
                    raise Exception("The version of the data you provided does not exist in the dataset!")

    __config = None
    __config_file_path = os.path.expanduser('~') + '\pylamost.ini'

    def __getConfig(self, reload=False):
        if not os.path.exists(self.__config_file_path):   # 检查执行程序路径中是否存在初始化文件:.ini中会配置token信息
            return None

        if not reload and None != self.__config:
            return self.__config

        with open(self.__config_file_path) as fh:
            self.__config = {}
            for line in fh:
                if line.startswith('#'):  # 注释行判断
                    continue
                k, v = line.split("=")    # token=...
                self.__config[k.strip()] = v.strip()
        return self.__config

    def __detectToken(self):
        if self.token is not None:
            return True
        cf = self.__getConfig()
        if cf is None or 'token' not in cf.keys():
            raise Exception("please set your token!")
        self.token=cf['token']
        return True

    def download(self, url, savedir):
        response = urllib.request.urlopen(url=url)
        data = response.read()
        # If the obtained data is empty, exit the program
        if not data:
            print("No data received. Exiting...")
            sys.exit()
        if savedir[-1] == '/':
            savefile=savedir + response.getheader("Content-disposition").split('=')[1]
        else:
            savefile = savedir + '/' + response.getheader("Content-disposition").split('=')[1]
        with open(savefile, 'wb') as fh:
            fh.write(data)
        print('Done!')
        return savefile

    def getUrl(self, url, params=None):
        if params is None:
            response = urllib.request.urlopen(url)
        else:
            response = urllib.request.urlopen(url, urllib.parse.urlencode(params).encode('utf-8'))
        chrset = response.headers.get_content_charset()
        if chrset is None:
            chrset='utf-8'
        data = response.read().decode(chrset)
        return data

    def Structured(self, data, savedir=None, filename=None):
        data_file = StringIO(data)
        sep_pattern = r'[|,]'  # 匹配'|'或者','作为分隔符
        df = pd.read_csv(data_file, sep=sep_pattern, na_values=[''], keep_default_na=False, dtype=str, engine='python')
        # 将DataFrame保存到CSV文件
        if savedir is not None and filename is not None:
            if savedir[-1] == '/':
                df.to_csv(f'{savedir}{filename}.csv', index=False)
            else:
                df.to_csv(f'{savedir}/{filename}.csv', index=False)
        return df

    def downloadCatalog(self, catname, savedir='./'):
        dr = self.__getDataset()
        version = self.__getVersion()
        if dr in ['1', '2', '3']:
            if version == '':
                if catname in self.__catalog_set[dr]:
                    print("Downloading...")
                    caturl = 'http://dr{0}.lamost.org/catdl?name={1}&token={2}'.format(dr, catname, self.token)
                    return self.download(caturl, savedir)
                else:
                    raise Exception("A catalog of this name does not exist!")
            else:
                raise Exception("This version of this dataset is not available!")
        else:
            if version in self.__catalog_set[dr] and catname in self.__catalog_set[dr][version]:
                print("Downloading...")
                if dr in ['8', '9', '10', '11'] or (dr == '7' and version == '2.0'):
                    caturl = 'http://www.lamost.org/dr{0}/v{1}/catdl?name={2}&token={3}'.format(dr, version, catname,
                                                                                                self.token)
                    return self.download(caturl, savedir)
                else:
                    caturl = 'http://dr{0}.lamost.org/v{1}/catdl?name={2}&token={3}'.format(dr, version, catname,
                                                                                            self.token)
                    return self.download(caturl, savedir)
            else:
                raise Exception("The wrong version or catalog name caused the catalog to not be downloaded!")

    def downloadFits_obs(self, res, obsid, savedir='./'):
        dr = self.__getDataset()
        version = self.__getVersion()
        if res == 'low':
            if dr in ['1', '2', '3']:
                fitsurl = 'http://dr{0}.lamost.org/spectrum/fits/{1}'.format(dr, obsid, self.token)
                print("Downloading...")
                return self.download(fitsurl, savedir)
            elif dr in ['4', '5']:
                fitsurl = 'http://dr{0}.lamost.org/v{1}/spectrum/fits/{2}?token={3}'.format(dr, version, obsid,
                                                                                            self.token)
                print("Downloading...")
                return self.download(fitsurl, savedir)
            else:
                fitsurl = 'http://www.lamost.org/dr{0}/v{1}/spectrum/fits/{2}?token={3}'.format(dr, version, obsid,
                                                                                                self.token)
                print("Downloading...")
                return self.download(fitsurl, savedir)
        elif res == 'med':
            if dr in ['1', '2', '3', '4', '5'] or (dr == '6' and version == '0'):
                raise Exception('No medium resolution spectra are available for download!')
            else:
                fitsurl = 'http://www.lamost.org/dr{0}/v{1}/medspectrum/fits/{2}?token={3}'.format(dr, version, obsid, self.token)
                print("Downloading...")
                return self.download(fitsurl, savedir)

    def downloadPng_obs(self, obsid, savedir='./'):
        dr = self.__getDataset()
        version = self.__getVersion()
        if dr in ['1', '2', '3']:
            pngurl = 'http://dr{0}.lamost.org/spectrum/png/{1}?token={2}'.format(dr, obsid, self.token)
            print("Downloading...")
            return self.download(pngurl, savedir)
        elif dr in ['4', '5']:
            pngurl = 'http://dr{0}.lamost.org/v{1}/spectrum/png/{2}?token={3}'.format(dr, version, obsid, self.token)
            print("Downloading...")
            return self.download(pngurl, savedir)
        else:
            pngurl = 'http://www.lamost.org/dr{0}/v{1}/spectrum/png/{2}?token={3}'.format(dr, version, obsid, self.token)
            print("Downloading...")
            return self.download(pngurl, savedir)

    def getFitsCsv_obs(self, res, obsid, savedir=None, filename=None):
        dr = self.__getDataset()
        version = self.__getVersion()
        if res == 'low':
            if dr in ['1', '2', '3']:
                fitscsvurl = 'http://dr{0}.lamost.org/spectrum/fits2csv/{1}?token={2}'.format(dr, obsid, self.token)
            elif dr in ['4', '5']:
                fitscsvurl = 'http://dr{0}.lamost.org/v{1}/spectrum/fits2csv/{2}?token={3}'.format(dr, version, obsid, self.token)
            else:
                fitscsvurl='http://www.lamost.org/dr{0}/v{1}/spectrum/fits2csv/{2}?token={3}'.format(dr, version, obsid, self.token)
            resp = self.getUrl(fitscsvurl)
            resp1 = self.Structured(resp, savedir=savedir, filename=filename)
            return resp1
        elif res == 'med':
            if dr in ['1', '2', '3', '4', '5'] or (dr == '6' and version == '0'):
                raise Exception('No medium resolution spectra are available!')
            else:
                fitscsvurl='http://www.lamost.org/dr{0}/v{1}/medspectrum/fits2csv/{2}?token={3}'.format(dr, version, obsid, self.token)
            resp = self.getUrl(fitscsvurl)
            return resp

    def getInfo_obs(self, obsid):
        dr = self.__getDataset()
        version = self.__getVersion()
        if dr in ['1', '2', '3']:
            url = 'http://dr{0}.lamost.org/spectrum/info/{1}'.format(dr, obsid)
        elif dr in ['4', '5', '6']:
            url = 'http://dr{0}.lamost.org/v{1}/spectrum/info/{2}'.format(dr, version, obsid)
        else:
            url = 'http://www.lamost.org/dr{0}/v{1}/spectrum/info/{2}'.format(dr, version, obsid)
        info=self.getUrl(url, {'token':self.token})
        info=json.loads(info)
        res={}
        for prop in info["response"]:
            res[prop["what"]]=prop["data"]
        return res

    # Cone Search Protocol
    def conesearch(self, res, ra, dec, radius):
        if res == 'low':
            url = f'http://www.lamost.org/dr{self.__getDataset()}/v{self.__getVersion()}/voservice/conesearch?ra={ra}&dec={dec}&sr={radius}&token={self.token}'
        elif res == 'med':
            url = f'http://www.lamost.org/dr{self.__getDataset()}/v{self.__getVersion()}/medvoservice/conesearch?ra={ra}&dec={dec}&sr={radius}&token={self.token}'
        res = urllib.request.urlopen(url=url)
        file_data = res.read()  # 读文件
        # 从文件中读取VOTable
        votable_data = io.BytesIO(file_data)
        # 读取VOTable文件
        votable_table = votable.parse_single_table(votable_data)
        column_names = [field.name for field in votable_table.fields]
        column_names = [f[10:] for f in column_names]
        # 获取表格数据
        table_data = votable_table.array
        if len(table_data) == 0:
            print('return 0 row')
            sys.exit()
        # 将列名和数据组合在一起
        n = 0
        print(f'return {len(table_data)} row')
        resp = {}
        for line in table_data:
            lis = list(line)
            new_list = zip(column_names, lis)
            resp[n+1] = list(new_list)
            n += 1
        return resp

    def desisearch(self, res, designation):
        ra_hours = int(designation[1:3])
        ra_minutes = int(designation[3:5])
        ra_seconds = float(designation[5:10])

        dec_sign = -1 if designation[10] == '-' else 1
        dec_degrees = int(designation[11:13]) * dec_sign
        dec_arcminutes = int(designation[13:15]) * dec_sign
        dec_arcseconds = float(designation[15:]) * dec_sign

        ra = (ra_hours + ra_minutes / 60 + ra_seconds / 3600) * 15
        dec = dec_degrees + dec_arcminutes / 60 + dec_arcseconds / 3600
        resp = self.conesearch(res, ra, dec, 0.001)
        return resp

    def downloadVOTable(self, ra, dec, radius, savedir):
        dr = self.__getDataset()
        version = self.__getVersion()
        if dr in ['1', '2', '3']:
            votableurl = 'http://dr{0}.lamost.org/voservice/ssap?pos={1},{2}&size={3}&token={4}'.format(dr, ra, dec, radius, self.token)
        elif dr in ['4', '5', '6']:
            votableurl = 'http://dr{0}.lamost.org/v{1}/voservice/ssap?pos={2},{3}&size={4}&token={5}'.format(dr, version, ra, dec, radius, self.token)
        else:
            votableurl = 'http://www.lamost.org/dr{0}/v{1}/voservice/ssap?pos={2},{3}&size={4}&token={5}'.format(dr, version, ra, dec, radius, self.token)
        self.download(votableurl, savedir)
        return self.getUrl(votableurl)

    def sql(self, sql, filename=None, savedir=None):
        dr = self.__getDataset()
        version = self.__getVersion()
        if dr in ['1', '2', '3']:
            sqlurl = 'http://dr{0}.lamost.org/sql/q?&token={1}'.format(dr, self.token)
        elif dr in ['4', '5', '6']:
            sqlurl = 'http://dr{0}.lamost.org/v{1}/sql/q?&token={2}'.format(dr, version, self.token)
        else:
            sqlurl = 'http://www.lamost.org/dr{0}/v{1}/sql/q?&token={2}'.format(dr, version, self.token)
        resp = self.getUrl(sqlurl, {'output.fmt': 'csv', 'sql': sql})
        resp1 = self.Structured(data=resp, savedir=savedir, filename=filename)  #  Save in CSV format
        return resp1

    def query(self, res, params, filename=None, savedir=None):
        dr = self.__getDataset()
        version = self.__getVersion()
        if res == 'low':
            if dr in ['1', '2', '3']:
                qurl = 'http://dr{0}.lamost.org/q?&token={1}'.format(dr, self.token)
            elif dr in ['4', '5', '6']:
                qurl = 'http://dr{0}.lamost.org/v{1}/q?&token={2}'.format(dr, version, self.token)
            else:
                qurl = 'http://www.lamost.org/dr{0}/v{1}/q?&token={2}'.format(dr, version, self.token)
        elif res == 'med':
            if dr in ['1', '2', '3', '4', '5'] or (dr == '6' and version == '0'):
                raise Exception('No medium resolution spectra are available!')
            else:
                qurl='http://www.lamost.org/dr{0}/v{1}/medcas/q?token={2}'.format(dr, version, self.token)
        resp = self.getUrl(qurl, params)
        resp1 = self.Structured(resp, filename=filename, savedir=savedir)
        return resp1

    #  Upload files for bulk operations
    def query2(self, res, params, files, filename=None, savedir=None):
        dr = self.__getDataset()
        version = self.__getVersion()
        if res == 'low':
            if dr in ['1', '2', '3']:
                qurl = 'http://dr{0}.lamost.org/q?&token={1}'.format(dr, self.token)
            elif dr in ['4', '5', '6']:
                qurl = 'http://dr{0}.lamost.org/v{1}/q?&token={2}'.format(dr, version, self.token)
            else:
                qurl = 'http://www.lamost.org/dr{0}/v{1}/q?&token={2}'.format(dr, version, self.token)
        elif res == 'med':
            if dr in ['1', '2', '3', '4', '5'] or (dr == '6' and version == '0'):
                raise Exception('No medium resolution spectra are available!')
            else:
                qurl='http://www.lamost.org/dr{0}/v{1}/medcas/q?token={2}'.format(dr, version, self.token)
        resp=requests.post(qurl, data=params, files=files)
        resp1 = self.Structured(resp.text, filename=filename, savedir=savedir)
        return resp1

    def getQueryResultCount(self, res, sqlid):
        dr = self.__getDataset()
        version = self.__getVersion()
        if res == 'low':
            if dr in ['1', '2', '3']:
                qurl = 'http://dr{0}.lamost.org/sqlid/{1}?token={2}&output.fmt=dbgrid&rows=1&page=1'.format(dr, sqlid, self.token)
            elif dr in ['4', '5', '6']:
                qurl = 'http://dr{0}.lamost.org/v{1}/sqlid/{2}?token={3}&output.fmt=dbgrid&rows=1&page=1'.format(dr, version, sqlid, self.token)
            else:
                qurl = 'http://www.lamost.org/dr{0}/v{1}/sqlid/{2}?token={3}&output.fmt=dbgrid&rows=1&page=1'.format(dr, version, sqlid, self.token)
        elif res == 'med':
            if dr in ['1', '2', '3', '4', '5'] or (dr == '6' and version == '0'):
                raise Exception('No medium resolution spectra are available!')
            else:
                qurl = 'http://www.lamost.org/dr{0}/v{1}/medcas/sqlid/{2}?token={3}&output.fmt=dbgrid&rows=1&page=1'.format(dr, version, sqlid, self.token)
        r = requests.post(qurl)
        info = json.loads(r.text)
        return int(info["total"])

    def readLRSFits(self, filename):
        hdulist = astropy.io.fits.open(filename)
        len_list = len(hdulist)
        if 1 == len_list:
            head = hdulist[0].header
            scidata = hdulist[0].data
            coeff0 = head['COEFF0']
            coeff1 = head['COEFF1']
            pixel_num = head['NAXIS1']
            specflux = scidata[0,]
            spec_noconti = scidata[2,]
            wavelength = numpy.linspace(0, pixel_num - 1, pixel_num)
            wavelength = numpy.power(10, (coeff0 + wavelength * coeff1))
            hdulist.close()
        elif 2 == len_list:
            scidata = hdulist[1].data
            wavelength = scidata[0][2]
            specflux = scidata[0][0]
        spec_smooth_7 = scipy.signal.medfilt(specflux, 7)
        spec_smooth_15 = scipy.signal.medfilt(specflux, 15)
        return (wavelength, specflux, spec_smooth_7, spec_smooth_15)

    def plotLRSFits(self, filename):
        wavelength, specflux, spec_smooth_7, spec_smooth_15 = self.readLRSFits(filename)
        plt.figure().set_size_inches(18.5, 6.5, forward=True)
        plt.plot(wavelength, specflux)
        plt.xlabel('Wavelength [Ångströms]')
        plt.ylabel('Flux')
        plt.show()

    def downloadAndPlotLRSSpectrum(self, obsid, savedir):
        self.plotLRSFits(self.downloadFits_obs(res="low", obsid=obsid, savedir=savedir))

    def readMRSFits(self, filename):
        hdulist = astropy.io.fits.open(filename)
        len_list=len(hdulist)
        data={}
        for i in range(1, len_list):
            header = hdulist[i].header
            scidata = hdulist[i].data
            specflux = scidata[0][0]
            wavelength = scidata[0][2]
            data[header['EXTNAME']]={'wavelength':wavelength, 'specflux':specflux}
        hdulist.close()
        return data

    def plotMRSFits(self, filename):
        data = self.readMRSFits(filename)
        plt.figure().set_size_inches(18.5, 6.5, forward=True)
        for k,v in data.items():
            plt.plot(v['wavelength'], v['specflux'])
        plt.xlabel('Wavelength [Ångströms]')
        plt.ylabel('Flux')
        plt.show()

    def downloadAndPlotMRSSpectrum(self, obsid, savedir):
        self.plotMRSFits(self.downloadFits_obs(res='med', obsid=obsid, savedir=savedir))