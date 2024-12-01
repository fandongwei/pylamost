#!/usr/bin/env python
# coding: utf-8

# ## test the pylamost

# In order to access protected LAMOST data, you should provide your token.
# Your token can be obtained at http://www.lamost.org/lmusers/user/, find the "Your pylamost Token".
# When you get your token you can also create a file `~/pylamost.ini` or `%userprofile%/pylamost.ini` on Windows, with content:
# ```
# token=12345678
# ```
# Then you don't have to write the token next time.

# In[1]:


from pylamost import lamost
lm=lamost(dataset=8, version=2.0)#init the lamost class
#lm.token='12345678'#specify your token. You can pass this step, if you created the ~/pylamost.ini file.
#Using international released data, token can be skip, except sql() function.

#lm.dataset=8 #specify the Data Release number
#lm.version=2.0 #specify the data version, or leave it None to always use the leatest version.


# ### Query interface

# In[2]:


# query low resolution catalog by obsid
params={'output.fmt':'csv','combined.obsid.textarea':'353301001'}
low=lm.query(params)
print(low)


# In[3]:


# query medium resolution catalog by obsid
params={'output.fmt':'csv','combined.obsid.textarea':'588902003'}
med=lm.query(params, ismed=True)
print(med)


# In[4]:


# query low resolution catalog by ra,dec file
params={'pos_group':'ra,dec','output.fmt':'csv','pos.type':'proximity'}
files={'pos.posfile':('sample.txt', open('sample.txt', 'r'))}
low=lm.query2(params, files)
print(low)


# In[5]:


# query medium resolution catalog by ra,dec file
params={'output.fmt':'csv','pos.type':'proximity'}
files={'pos.posfile':('sample.txt', open('sample.txt', 'r'))}
low=lm.query2(params, files, ismed=True)
print(low)


# ### SQL query interface

# In[6]:


s=lm.sql("select c.obsid,c.obsdate, c.ra, c.dec, c.z, c.lmjd from catalogue c where spos(c.ra,c.dec) @ scircle '<(331.7d, -1.4d),0.2d>' limit 5", fmt='csv')
print(s)


# In[7]:


s=lm.sql("select c.obsid from catalogue c where spos(c.ra,c.dec) @ scircle '<(331.7d, -1.4d),0.3d>' limit 5", fmt='csv')
print(s)


# In[8]:


csv = lm.getFitsCsv(obsid='101068')
print(csv)


# ### simple information

# In[9]:


# get low resolution fiber info
info=lm.getInfo('353301001')
for k,v in info.items():
    print(k,':',v)


# In[10]:


# get medium resolution fiber info
info=lm.getInfo('588902003', ismed=True)
print(info)


# ### download FITS file

# In[11]:


#download low resolution fits file by obsid
lm.downloadFits(obsid='353301001',savedir='./')


# In[12]:


#download medium resolution fits file by obsid
lm.downloadFits(obsid='588902003',savedir='./',ismed=True)


# ### download spectrumthumbnail png

# In[13]:


#download low resolution spectrum thumbnail png file by obsid
#medium resolution fits file has no png thumbnail
lm.downloadPng(obsid='353301007',savedir='./')


# ### download csv format spectrum

# In[14]:


#download low resolution csv format spectrum by obsid
csv = lm.getFitsCsv(obsid='353301007')
print(csv)


# In[15]:


#download medium resolution csv format spectrum by obsid
csv = lm.getFitsCsv(obsid='588902003',ismed=True)
print(csv)


# ### Cone Search Protocol

# In[16]:


#fetch low resolution catalog conesearch result 
votable_string = lm.conesearch(ra=10.0004738,dec=40.9952444,radius=0.2)
# print(votable_string)
from astropy.io.votable import parse_single_table
import io
# 将字符串编码为字节
byte_data = votable_string.encode('utf-8')
# 创建一个io.BytesIO对象
byte_io = io.BytesIO(byte_data)
table = parse_single_table(byte_io)

# 现在你可以像处理任何其他Astropy Table对象一样处理table
print(table)


# In[17]:


#fetch medium resolution catalog conesearch result 
cs = lm.conesearch(ra=15.3672776,dec=4.0094024,radius=0.002, ismed=True)
print(cs)


# ### Simple Spectral Access Protocol

# In[18]:


#fetch low resolution ssap search result 
ssap = lm.ssap(ra=10.0004738,dec=40.9952444,radius=0.2)
print(ssap)


# In[19]:


#fetch medium resolution ssap search result 
ssap = lm.ssap(ra=15.3672776,dec=4.0094024,radius=0.002)
print(ssap)


# ### read local spectrum fits to data array

# In[20]:


#read low resolution spectrum fits file
wavelength, specflux, spec_smooth_7, spec_smooth_15=lm.readLRSFits('spec-57278-EG224429N215706B01_sp01-001.fits.gz')
print('wavelength', wavelength)
#print('specflux', specflux)
#print('spec_smooth_7', spec_smooth_7)
print('spec_smooth_15', spec_smooth_15)


# In[21]:


#read medium resolution spectrum fits file
data=lm.readMRSFits('med-58025-HIP507401_sp02-003.fits.gz')
print(data)


# ### plot local spectrum

# In[22]:


#plot local low resolution spectrum
lm.plotLRSFits('spec-57278-EG224429N215706B01_sp01-001.fits.gz')


# In[23]:


#plot local medium resolution spectrum
lm.plotMRSFits('med-58025-HIP507401_sp02-003.fits.gz')


# ### download spectrum data and plot

# In[24]:


#download and plot low resolution spectrum
lm.downloadAndPlotLRSSpectrum('353301007')


# In[25]:


#download and plot medium resolution spectrum
lm.downloadAndPlotMRSSpectrum('588902003')

