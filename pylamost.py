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

class lamost:
    def __init__(self, isdev=False, dataset=5):
        self.__isdev=isdev
        self.dataset=dataset
        self.email=None
        self.token=None
        self.version=None
        self.__isdev=False

    def __getDataset(self):
        prefix='dr5'
        if self.dataset is not None:
            prefix = 'dr%d'%self.dataset
        if self.__isdev: return 'l'+prefix
        else: return prefix

    def __getVersion(self):
        if self.version is not None:
            return '/v%d'%self.version
        return ''

    __config=None
    __config_file_path=os.path.expanduser('~')+'/pylamost.ini'
    
    def __getConfig(self, reload=False):
        if not os.path.exists(self.__config_file_path): return None
        
        if not reload and None!=self.__config: return self.__config
        
        with open(self.__config_file_path) as fh:
            self.__config={}
            for line in fh:
                if line.startswith('#'):continue
                k,v=line.split("=")
                self.__config[k.strip()]=v.strip()
        return self.__config

    def __detectToken(self):
        if self.token is not None: return True
        cf = self.__getConfig()
        if cf is None or 'token' not in cf.keys(): 
            print('please set your token')
            return False
        self.token=cf['token']
        return True

    def download(self, url, savedir='./'):
        response = urllib.request.urlopen(url)
        data = response.read()
        savefile=savedir+'/'+response.getheader("Content-disposition").split('=')[1]
        with open(savefile, 'wb') as fh:
            fh.write(data)
        return savefile

    def getUrl(self, url, params=None):
        if params is None:
            response = urllib.request.urlopen(url)
        else:
            response = urllib.request.urlopen(url, urllib.parse.urlencode(params).encode('utf-8'))
        chrset = response.headers.get_content_charset()
        if chrset is None: chrset='utf-8'
        data = response.read().decode(chrset)
        return data

    def downloadCatalog(self, catname, savedir='./'):
        caturl='http://{0}.lamost.org{1}/catdl?name={2}&token={3}'.format(self.__getDataset(), self.__getVersion(), catname, self.token)
        return self.download(url, savedir)

    def downloadFits(self, obsid, savedir='./'):
        if not self.__detectToken(): return
        fitsurl='http://{0}.lamost.org{1}/spectrum/fits/{2}?token={3}'.format(self.__getDataset(), self.__getVersion(), obsid, self.token)
        return self.download(fitsurl, savedir)

    def downloadPng(self, obsid, savedir='./'):
        if not self.__detectToken(): return
        pngurl='http://{0}.lamost.org{1}/spectrum/png/{2}?token={3}'.format(self.__getDataset(), self.__getVersion(), obsid, self.token)
        return self.download(pngurl, savedir)

    def getFitsCsv(self, obsid):
        if not self.__detectToken(): return None
        url='http://{0}.lamost.org{1}/spectrum/fits2csv/{2}?token={3}'.format(self.__getDataset(), self.__getVersion(), obsid, self.token)
        return self.getUrl(url)

    def getInfo(self, obsid):
        if not self.__detectToken(): return None
        #url='http://{0}.lamost.org{1}/spectrum/info/{2}?token={3}'.format(self.__getDataset(), self.__getVersion(), obsid, self.token)
        #return self.getUrl(url, params)
        url='http://{0}.lamost.org{1}/spectrum/info/{2}'.format(self.__getDataset(), self.__getVersion(), obsid)
        info=self.getUrl(url, {'token':self.token})
        info=json.loads(info)
        res={}
        for prop in info["response"]:
            res[prop["what"]]=prop["data"]
        return res

    #Cone Search Protocol
    def conesearch(self, ra, dec, radius):
        if not self.__detectToken(): return
        conesearchurl='http://{0}.lamost.org{1}/voservice/conesearch?ra={2}&dec={3}&sr={4}&token={5}'.format(self.__getDataset(), self.__getVersion(), ra, dec, radius, self.token)
        return self.getUrl(conesearchurl)

    #Simple Spectral Access Protocol
    def ssap(self, ra, dec, radius):
        if not self.__detectToken(): return
        ssapurl='http://{0}.lamost.org{1}/voservice/ssap?pos={2},{3}&size={4}&token={5}'.format(self.__getDataset(), self.__getVersion(), ra, dec, radius, self.token)
        return self.getUrl(ssapurl)

    def sql(self, sql):
        if not self.__detectToken(): return
        sqlurl='http://{0}.lamost.org{1}/sql/q?&token={2}'.format(self.__getDataset(), self.__getVersion(), self.token)
        return self.getUrl(sqlurl, {'output.fmt':'csv', 'sql':sql})

    def query(self, params):
        if not self.__detectToken(): return
        qurl='http://{0}.lamost.org{1}/q?token={2}'.format(self.__getDataset(), self.__getVersion(), self.token)
        return self.getUrl(qurl, params)
    
    def query2(self, params, files):
        if not self.__detectToken(): return
        qurl='http://{0}.lamost.org{1}/q?token={2}'.format(self.__getDataset(), self.__getVersion(),self.token)
        r=requests.post(qurl, data=params, files=files)
        return str(r.text)
    
    def readFits(self, filename):
        hdulist = astropy.io.fits.open(filename)
        head = hdulist[0].header
        scidata = hdulist[0].data
        coeff0 = head['COEFF0']
        coeff1 = head['COEFF1']
        pixel_num = head['NAXIS1'] 
        specflux = scidata[0,]
        spec_noconti = scidata[2,]
        wavelength=numpy.linspace(0,pixel_num,pixel_num)
        wavelength=numpy.power(10,(coeff0+wavelength*coeff1))
        hdulist.close()
        #
        spec_smooth_7=scipy.signal.medfilt(specflux,7)
        spec_smooth_15=scipy.signal.medfilt(specflux,15)
        return (wavelength, specflux, spec_smooth_7, spec_smooth_15)
    
    def plotFits(self, filename):
        wavelength, specflux, spec_smooth_7, spec_smooth_15 = self.readFits(filename)        
        plt.figure().set_size_inches(18.5, 6.5, forward=True)
        plt.plot(wavelength, specflux)
        plt.xlabel('Wavelength [Ångströms]')
        plt.ylabel('Flux')
        plt.show()
        
    def downloadAndPlotSpectrum(self, obsid):
        self.plotFits(self.downloadFits(obsid))