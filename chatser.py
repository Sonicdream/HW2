import socket  
import threading 
import time 
  
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
  
sock.bind(('localhost', 9522))  
  
sock.listen(5)  
print('Server', socket.gethostbyname('localhost'), 'listening ...')  
  
mydict = dict()  #name
mylist = list()
  
stalist = list() #pure name

 
nameToaddress = dict()
defaultMan = ['def1','def2']
defaultpass = '0000'
NewPass = dict()
NewPass['def1'] = '0000'
NewPass['def2'] = '0000'

Note = "You have wrong password"
WhenLeave = list()


 

def tell(addr, whatToSay):
    addr.send(whatToSay)
    time.sleep(1)



def tellOne(addr, whatToSay):
    addr.send(whatToSay.encode())
    time.sleep(1)
           

#把whatToSay传给除了exceptNum的所有人  
def tellOthers(exceptNum, whatToSay):  
    for c in mylist:  
       # if c.fileno() != exceptNum :  
            try:  
               # print(whatToSay)
                c.send(whatToSay.encode())
                time.sleep(1)
               # for i in range(0, len(stalist), +1):
                #    tem = '@'+ stalist[i]
                #    c.send(tem.encode())
            except:  
                pass  
  
def subThreadIn(myconnection, connNumber):


    NewMan = 1  
    nickname = myconnection.recv(1024).decode() #receive nickname add
    name = nickname[0:4]
    secret = nickname[5:]
    print(name)


    
    for i in range(0, len(defaultMan), +1):
       # if name == [defaultMan[i]][1:] and [defaultMan[i]][0] == '@':
       #     print("################")
       #     NewMan = 0
       #     while secret != NewPass[name] :      
       #         myconnection.send(Note.encode())
       #         secret = myconnection.recv(1024).decode()
       #         print("11")
 
        if name == defaultMan[i]:
            NewMan = 0
            while secret != NewPass[name]:
           # while secret != defaultpass:      
                myconnection.send(Note.encode())
                secret = myconnection.recv(1024).decode()
                print("11")

    if NewMan == 1:
       # OneUse = '@'+name
        defaultMan.append(name)
       # print(defaultMan[2])
       # print([defaultMan[2]][0])
        NewPass[name] = secret
        print(secret)
                
    print("below is registered man")
    print("========================")
    for i in range(0, len(defaultMan), +1):
         print(defaultMan[i])

    print("========================")         
      
   # print(myconnection) ###    

  
    mydict[myconnection.fileno()] = name  #mydict = name
    stalist.append(mydict[myconnection.fileno()]) # assign name to stalist
    mylist.append(myconnection)
    
   # nameToaddress.append(nickname,myconnection)    
    nameToaddress[name] = myconnection
   
    print(555) 

    #broadcast who  go online
    tellOthers(connNumber, name + " is going up")    

 #   nameToaddress[nickname] = myconnection  ##### name To address dict
   


    for i in range(0, len(stalist), +1):
       # print(stalist[i])
        tem = '@' + stalist[i]
       # print(tem+"xxx")
        tellOthers(connNumber, tem)####################

   # tem = '@' + name
   # tellOthers(connNumber, tem)
    
       

    #send Leave Msg to that man
    for i in range(0, len(WhenLeave), +1):
        if(name == (WhenLeave[i])[0:4]):
            tellOne(nameToaddress[name], (WhenLeave[i])[5:])
            print("****")
            WhenLeave[i] = '0'
           # WhenLeave.pop(i)

    #delete the Msg which had been sent
    
        
            
    
           
           
            

   # print(mydict[myconnection.fileno()])
   # mylist.append(myconnection)  
    print('connection', connNumber, ' has nickname :', name)
   # for i in range(0, len(mydict), +1):
    
        
  
   # tellOthers(connNumber, '【系统提示：'+mydict[connNumber]+' 进入聊天室】')#############
    
    checkLeave = 0  # using offline msg 
    WantFile = 0
    WhoWant = "0"
    while True:  
        try:  
           # print(mydict[4])
           # member = mydict[4]
           # sock.send(member.encode()) 
           # print(0)
            
            recv = myconnection.recv(1024)      
            recvedMsg = recv.decode()
           # recvedMsg = myconnection.recv(1024).decode() #receive speak
           # recvedFile = 

                         
            if recvedMsg:
                if recvedMsg[0:4] == "send":
                    for i in range(0, len(stalist), +1):
                        if recvedMsg[5:9] == stalist[i]:
                            tellOne(nameToaddress[recvedMsg[5:9]], mydict[myconnection.fileno()] + ": " + recvedMsg[10:])
                            checkLeave = 1
                    if checkLeave == 0:    
                         WhenLeave.append(recvedMsg[5:9] +'@'+ mydict[connNumber]+ ": " +recvedMsg[10:]) 

                    checkLeave = 0
                            #put msg into leaveBuffer          

                elif recvedMsg[0:5] == "@talk":
                     TalkMsg = myconnection.recv(1024).decode()
                     while TalkMsg != "@exit":
                         tellOne(nameToaddress[recvedMsg[6:10]], mydict[connNumber] + ": " + TalkMsg)
                        # print("FFFFF")
                         TalkMsg = myconnection.recv(1024).decode()

                elif recvedMsg[0:5] == "close":
                     tellOne(nameToaddress[name], "YOU want to Leave?" )

                     stalist.remove(name)  #remove the online man
                    # for i in range(0, len(stalist), +1):
                        # pem = '#' + name
                     tellOthers(connNumber, '#' + name )####################
                    # print("****" + name)
                     mydict.pop(myconnection.fileno()) #remove the online man
                     mylist.remove(myconnection) ##
                     nameToaddress.pop(name) ##

                    # myconnection.close()
                    # mylist.remove(myconnection)
                    # print("LEAVE")
                    # myconnection.close()


                elif recvedMsg[0:4] == "file":
             #   elif WantFile == 1:
             #       print("Want")
             #       print(recv)
             #       WantFile = 0
                    for i in range(0, len(stalist), +1):
                        if recvedMsg[5:9] == stalist[i]:
                            WhoWant = recvedMsg[5:9]
                            WantFile = 1
                            print("*****" + WhoWant)
                            tellOne(nameToaddress[WhoWant], '&' + name )
                            time.sleep(1)

                            
                           # nameToaddress[recvedMsg[5:9]] 
                           # tell(myconnection, AAA)
                elif WantFile == 1:
                    tell(nameToaddress[WhoWant], recv )
                   # print(TheFile)
                    WantFile = 0

                     

           # print("HELLO") 
                 
               # elif WantFile == 1:
               # elif recvedMsg[0:3] == "yes":
                   # tellOne(nameToaddress[WhoWant], '&' + name )
                   # print(WhoWant)
               #     print(recvedMsg[4:])
                   # time.sleep(2)
                   # tell(nameToaddress[recvedMsg[4:]], "$Y")
                   # time.sleep(1)
                   # tell(nameToaddress[recvedMsg[4:]], TheFile)
                #    print(TheFile)
                   # WantFile = 0

               # elif recvedMsg[0:2] == "no":
               #     time.sleep(2)
               #     tell(nameToaddress[recvedMsg[3:]], "$N")
      
                    
                           
                         
                    
     
               # print(mydict[connNumber], ':', recvedMsg)  # print who speak what
                else: 
                    tellOthers(connNumber, mydict[connNumber]+' :'+recvedMsg)##### #mydict[cooNumber]:nickname
                      
  
        except (OSError, ConnectionResetError):  
         #   try:  
         #       mylist.remove(myconnection)  
         #   except:  
         #       pass  
         #   print(mydict[connNumber], 'exit, ', len(mylist), ' person left')  
         #   tellOthers(connNumber, '【系统提示：'+mydict[connNumber]+' 离开聊天室】')  
         #   myconnection.close()  
            return  
  
while True:  
    connection, addr = sock.accept()  
    print('Accept a new connection', connection.getsockname(), connection.fileno()) #who sock ; what port 
    try:  
        #connection.settimeout(5)  
        buf = connection.recv(1024).decode()  
        if buf == '1':  
            connection.send(b'welcome to server!')  
  
            #为当前连接开辟一个新的线程
            print('***' + buf)
           # for i in range(0, len(defaultMan), +1):
            #    if buf[0:4] == defaultMan[i]:
             #       if buf[5:] != defaultpass:
              #          print('wrong password')
               #         connection.send(b'wrong password!') 
              # print("existMan")
  
            mythread = threading.Thread(target=subThreadIn, args=(connection, connection.fileno()))  
            mythread.setDaemon(True)  
            mythread.start()  
              
        else:  
            connection.send(b'please go out!')  
            connection.close()  
    except :    
        pass
