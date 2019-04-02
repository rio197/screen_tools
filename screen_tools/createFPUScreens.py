#!/usr/bin/python
# Archived from Andriy P. and Alexandre F. at IMS
import ConfigParser
import operator
import io
import datetime
import re
import math
import sys
def key_func(s):
    return [int(x) if x.isdigit() else x for x in re.findall(r'\D+|\d+', s)]
today = datetime.date.today().strftime("%Y%m%d")
servers = {}
username=raw_input("What's your name? ")
with open("/redacted.com/distribute.cfg") as f:
     sample_config = f.read()
     config = ConfigParser.RawConfigParser()
     config.readfp(io.BytesIO(sample_config))
for key, val in config.items('ServerNumberMap'):
     mod=re.search(".*mod\d.*",key)
     mst=re.search(".*mst\d.*|.*db\d.*",key)
     depot_gw=re.search(".*depot\d.*|.*gw\d.*|.*arch\d.*|.*cache\d.*|.*rig\d.*|.*depot.\d.*|.*rpt\d.*",key)
     if mst:
          weight="-10"
          servers.update({key:weight})
     elif depot_gw:
          weight="-5"
          servers.update({key:weight})
     elif mod:
          weight="0"
          servers.update({key:weight})
     else: servers.update({key:val})
sorted_list=sorted(servers.items(),key= lambda x: (float(x[1]),key_func(x[0]) ))
screen_files_count=int(math.ceil(float(len(sorted_list)/float(39))))
for screens in range(0,screen_files_count):
      print ("screen num:"+str(screens))
      file_name='/tmp/.screenrc.FPU{0}.{1}'.format(screens,today)
      screen_file=open(file_name,'w+')
      print >>screen_file, "termcapinfo xterm* ti@:te@"
      print >>screen_file, "defscrollback 200000"
      print >>screen_file, "vbell off"
      print >>screen_file, "hardstatus alwayslastline"
      print >>screen_file, "hardstatus string \"%{=b kG}%-w%{= BW}%50>%n %t%{-}%+w%< %= | %{= kR}%c%A | %{=b kG} %H\""
#      print >>screen_file, "bindkey -k k8 prev # F8 "
#      print >>screen_file, "bindkey -k k9 next # F9"
      print >>screen_file, "bindkey \"^[[1;2D\" prev"
      print >>screen_file, "bindkey \"^[[1;2C\" next"
      print >>screen_file, "bindkey \"^B\" select"
      print >>screen_file, "altscreen on"
      print >>screen_file, "zombie kr"
      print >>screen_file, "screen -t main"+str(screens)
      if (int((screens+1)*39)>len(sorted_list)):
          out_range=len(sorted_list)-int((screens)*39)
      else: out_range=39
      for screen_rec in range(screens*39,int(screens*39+out_range)):
           print >>screen_file, "screen -t {0} ssh {0} ".format(sorted_list[screen_rec][0].split(".")[0])
      print "screen -S FPU{0} -c {1}".format(screens,file_name)

      print "for i in {1.."+str(out_range)+"}; do screen -S FPU"+str(screens)+" -p $i -X stuff $'sudo su - \\n' ; done"
      print "for i in {1.."+str(out_range)+"}; do screen -S FPU"+str(screens)+" -p $i -X stuff $'cd /tmp \\n' ; done"
      print "for i in {1.."+str(out_range)+"}; do screen -S FPU"+str(screens)+" -p $i -X stuff $'yum install -y wget ; wget --no-check-certificate https://redacted.com/bootstrap-depstart -O /tmp/bootstrap-depstart && sh /tmp/bootstrap-depstart \\n' ; done"
      print "for i in {1.."+str(out_range)+"}; do screen -S FPU"+str(screens)+" -p $i -X stuff $'if [ $(lsb_release -rs | cut -f1 -d.) -lt 7 ]; then /usr/sbin/depstart -va --upgrade ; else echo \"running RHEL7\" && /usr/sbin/depstart --upgrade ; fi \\n' ; done"
