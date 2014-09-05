#!/usr/bin/env python
import CodeaForum
import BotCheck
#import console
import time


DELETE = True



#console.clear()

def loop():
  #ctr = 1
  while True:
    print time.strftime('%H:%M:%S')
    BotCheck.getUsers()
    break
    #time.sleep(300)
    #ctr = ctr + 1
    #if ctr == 5:
        #break

if __name__ == "__main__":
  print '******Welcome to Codea Bot Smasher******'
  forum = CodeaForum.Codea()
  forum.login(loop)
