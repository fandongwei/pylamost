import webbrowser
from pylamost import lamost

class access_web(lamost):
        def obsid_web(self, obsids):
              #obsids : list
              for obsid in obsids:
                  url = 'http://dr7.lamost.org/medspectrum/view?obsid={}'.format(obsid)
                  chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
                  webbrowser.get(chrome_path).open(url)                                                                                                                
              print(url)
       
        def conesearch1(self, ra, dec, radius):
              conesearchurl='http://dr7.lamost.org/voservice/conesearch?ra={0}&dec={1}&sr={2}&token={3}'.format(ra, dec, radius, self.token) 
              ### 直接访问网页
              return self.getUrl(conesearchurl)

def obsid_web(obsids):
    #obsids : list
    for obsid in obsids:
        url = 'http://dr7.lamost.org/medspectrum/view?obsid={}'.format(obsid)
        chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
        webbrowser.get(chrome_path).open(url)                                                                                                                
    print(url)


if __name__ == '__main__':
   obsids = ['716201001']
   acweb = access_web()
   acweb.obsid_web(obsids)
   

