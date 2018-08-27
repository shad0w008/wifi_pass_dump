#coding=utf-8

#Make sure OS must be Windows 7，Windows Vista, Windows Server 2008 R2 or Windows Server 2008 or window 10.

from subprocess import Popen,PIPE
import re,time,sys,os
import platform

os_ver=platform.platform().lower()


def main():
  #folder_name='tmp-'+str(int(time.time()))
  #os.mkdir(folder_name)
  #folder_name=os.path.realpath(sys.path[0])+'\\'+folder_name
  #print('create folder: %s' % (folder_name))
  
  print('Starting wlansvc......')

  try:
    cmd0='net start wlansvc'
    a=Popen(cmd0,stdout=PIPE,shell=True)
    cmd1='netsh wlan show profiles'
    b=Popen(cmd1,stdout=PIPE,shell=True)
    c=b.stdout.read()
    d=re.findall(': (.*?)\r\n',c)
    e=[i for i in d if len(i)>0]
    mm=0
    while len(e)==0:
      cmd0='net start wlansvc'
      a=Popen(cmd0,stdout=PIPE,shell=True)
      cmd1='netsh wlan show profiles'
      b=Popen(cmd1,stdout=PIPE,shell=True)
      c=b.stdout.read()
      d=re.findall(': (.*?)\r\n',c)
      e=[i for i in d if len(i)>0]
      mm+=1
      if mm>=3:
        break
      
    print('Found %s WIFI accounts!'%str(len(e)))
    f0=[]
    for i in e[:]:
      if 'windows-10' not in os_ver:
        g0=Popen('netsh wlan show profile name="'+i+'" key=clear',stdout=PIPE,shell=True).stdout.read()
        g1=re.findall(': (.*?)\r\n\r\n',g0)[-1]
      else:
        g0=Popen('netsh wlan export profile name="'+i+'" folder=.'+' key=clear',stdout=PIPE,shell=True)
        time.sleep(1)
        files='WLAN-'+i+'.xml'
        g11=open(files).read()
        g1='' if g11.find('keyMaterial')==-1 else re.findall('keyMaterial>(.*?)</keyMaterial',g11)[0]
        os.system('del {0}'.format(files))
      print('wifi name:'+i+'\n'+'wifi password:'+g1+'\n')
      hashes=i+':'+g1
      f0.append(hashes)
    filename=time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())+'.txt'
    with open(filename,'a+') as f:
      for i in f0:
        f.write(i+'\n\n\n')

    print('Wifi passwords saved in file: %s'%filename)
    print('Please Stop wlansvc Manually!')
    #cmd3='net stop wlansvc'
    #g=Popen(cmd3,stdout=PIPE,shell=True)
  except Exception,e:
    print(e)
    exit(0)

if __name__=='__main__':
  main()
