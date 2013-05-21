#!/usr/bin/python
# Version 1.0
 
import os,sys,string
sys.path.append('/home/user/python/lib/lib/python')
import socket
import pexpect,getpass,difflib
import xlwt
import re
import credential
 
os.system('rm Devices_Config_Pull.xls') #This will remove previews created spreadsheet
os.system('rm Devices_Config_Pull.zip') #This will remove previews created zip
 
list_devices=open('list.txt').readlines() #This will read the list of devices that file is on the same location as the script
 
 
email, UID, passwd, enable = credential.cred() #This is a module that I created that will store all of credential
connection = sys.argv[1]
connection = int(connection)
 
 ### If the argument is 1 it will telnet into the devices if the argument is 2 it will ssh into the devices
if connection == 1:
        tunnel = 'telnet '
       conmess = 'telnet'
elif connection == 2:
        tunnel = ('ssh -o StrictHostKeyChecking=no -l ' + UID + ' ')
        conmess = 'SSH'
######## This for loop block. is the loop for telnet/ssh into the devices
 
wbk = xlwt.Workbook() #Create an excel workbook
font = xlwt.Font() 
font.bold = True
style = xlwt.XFStyle()
style.font = font
 
for i in list_devices:
         rowHostname = 0
         rowIp = 1
         rowTittle = 2
         rowOutput = 4
         col1 = 0
         IP = ""
         IP2 = ""
         x = i.strip().split()
         if len(x) == 2:
                r = 0
         else:
                r =1
         while r<3:
 
                 if r == 1:
 
                        hostname, IP,IP2 = i.strip().split()
                        print r
                        print IP
                        print IP2
                        print hostname
                        sheet = wbk.add_sheet(hostname)
                        f_write = file (hostname+'_Device_1.txt','wb')
                        sheet.write(rowHostname,0,hostname+"_Device_1", style)
                        sheet.write(rowIp,0,"IP: "+IP, style)
                        sheet.write(rowTittle,0,"Config", style)
 
                 elif r == 2:
 
                        IP = IP2
                        col1 = 1
                        sheet.write(rowHostname,1,hostname+"_Device_2", style)
                        f_write = file (hostname+'_Device_2.txt','wb')
                        sheet.write(rowIp,1,"IP: "+IP, style)
                        sheet.write(rowTittle,1,"Config", style)
 
                 elif r == 0:
 
                        hostname, IP = i.strip().split()
                        print r
                        print IP
                        print IP2
                        print hostname
                        sheet = wbk.add_sheet(hostname)
                        f_write = file (hostname+'_Device_1.txt','wb')
                        sheet.write(rowHostname,0,hostname+"_Device_1", style)
                        sheet.write(rowIp,0,"IP: "+IP, style)
                        sheet.write(rowTittle,0,"Config", style)
                        r=3
                 r+=1
 
                 print "connecting to " + IP +" " +hostname
                 print 'trying to ' + conmess +' ' + IP
                 child = pexpect.spawn(tunnel + IP)
                 m = child.expect (['assword:','[Ll]ogin:','[Uu]sername',pexpect.TIMEOUT,pexpect.EOF])
                 if m==0:
                        child.sendline(passwd)
                 elif m==1:
                        child.sendline(UID)
                                 elif m==2:
                                                child.sendline(UID)
                 elif m==3:
                        print "login error"
                        continue
                 elif m==4:
                        print "no login prompt error"
                        continue
 
 
                 q = child.expect (['>','[Pp]assword',pexpect.TIMEOUT,pexpect.EOF])
                 if q==0:
                        child.sendline ('ena')
                 elif q==1:
                        
                        child.sendline (passwd)
                 elif q==2:
                        print "wrong password or wait too long for prompt"
                        sheet.write(rowOutput,col1,'Wrong Password')
                        rowOutput+=1
                        continue
                 elif q==3:
                        sheet.write(rowOutput,col1,'Prompt Timeouts')
                        rowOutput+=1
                        continue
 
 
                 q = child.expect (['assword:','>',pexpect.TIMEOUT,pexpect.EOF])
                 if q==0:
                        child.sendline (enable)
                 elif q==1:
                        child.sendline ('enable')
                 elif q==2:
                        sheet.write(rowOutput,col1,'Wrong Password')
                        rowOutput+=1
                        continue
                 elif q==3:
                        sheet.write(rowOutput,col1,'Prompt Timeout')
                        rowOutput+=1
                        continue
 
                 q = child.expect (['>','[Pp]assword',pexpect.TIMEOUT,pexpect.EOF, '#'])
                 if q==0:
                        child.sendline ('ena')
                 elif q==1:
                        
                        child.sendline (enable)
                 elif q==2:
                        sheet.write(rowOutput,col1,'Wrong Password')
                        rowOutput+=1
                        continue
                 elif q==3:
                        sheet.write(rowOutput,col1,'Prompt Timeout')
                        rowOutput+=1
                        continue
                 elif q==4:
                        child.sendline(' ')
                 q = child.expect (['>','[Pp]assword',pexpect.TIMEOUT,pexpect.EOF, '#'])
                 if q==0:
                        sheet.write(rowOutput,col1,'Wrong Enable Password')
                        rowOutput+=1
                        continue
                 elif q==1:
                        sheet.write(rowOutput,col1,'Wrong Enable Password')
                        rowOutput+=1
                        continue
                 elif q==2:
                        sheet.write(rowOutput,col1,'Wrong Password')
                        rowOutput+=1
                        continue
                 elif q==3:
                        sheet.write(rowOutput,col1,'Prompt Timeout')
                        rowOutput+=1
                        continue
                 elif q==4:
                        child.sendline(' ')
                                print 'Im OK'
                 child.expect('#')
                 child.sendline ('show run | in hostname') #For grabbing the device histname
                 child.expect('#')
                 host=child.before
                 join =host.split(" ")
                 host = join[5]
                 join1=host.splitlines()
                 host = join1[0]
                 child.sendline ('term len 0')
 
                 print 'pass term'
                 # This is the end of the process to ssh/telnet into the devices


                 #Here start to grab the show run information
                 command = 'sh run'
                 q = child.expect ([host+'#',pexpect.TIMEOUT,pexpect.EOF])
                 if q==0:
                         child.logfile_read = f_write
                         child.sendline (command)
                 elif q==1:
                         print "command not working " + i
                         continue
                 elif q==2:
                         print "command not working" + i
                         continue
 
                 command = 'show clock'
                 q = child.expect ([host+'#',pexpect.TIMEOUT,pexpect.EOF])
                 if q==0:
                        config = child.before
                        config = config.split("\n")
                        rowOutput = 4
                        for i in config:
                                sheet.write(rowOutput,col1,i)
                                rowOutput+=1
                        child.sendline (command)
 
 
                 elif q==1:
                         print "command not working " + i
                         continue
                 elif q==2:
                         print "command not working" + i
                         continue
 
 
                 child.expect('#')
                 f_write.close()
                 child.sendline('exit')
                 sheet.col(0).width = 6000
                 sheet.col(1).width = 6000
 
wbk.save('Devices_Config_Pull.xls') #Saving the spreadsheet
os.system('zip Devices_Config_Pull Devices_Config_Pull.xls') #Send this command to the OS, in my case I use linux
os.system('uuencode Devices_Config_Pull.zip Devices_Config_Pull.zip | mailx -s "Devices Configs - Spreadsheet" ' +email) #Again using the OS Command to send an email with an attachemt
print ('Sending the zip file to ' +email+'.Please check your email in couple of minutes')