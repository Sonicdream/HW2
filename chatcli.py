import socket  
import time  
import threading 
from getpass import getpass

  
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
  
sock.connect(('localhost', 9522))  
sock.send(b'1')  
print(sock.recv(1024).decode())  
nickName = input('input your nickname: ')
password = getpass() #input your password


NamePass = nickName + '$' + password 
sock.send(NamePass.encode())  
mylist = list() #client add's friend
stalist = list() #server's newnest friend list

Hide = 0

DecideClose = 0
#Want = 0
def sendThreadFunc():
    global Hide
  #  print(Hide)
  #  Hide = 1  
    while True:  
        try:
           # if Hide == 1:
           #     myword = getpass()
           #     Hide = 0
            time.sleep(1)
           # print(Hide)
            if Hide ==1:
                 myword = getpass()
                 Hide = 0
                 sock.send(myword.encode())
         
            else :
                myword = input()
           # print(myword[0:2])  
                if myword[0:3] == "add":              
                   mylist.append(myword[4:8])
                
                elif myword[0:4] == "list":                
               # print(mylist[0])
               # print(mylist[1])
                     for i in range(0, len(mylist), +1):
                         comfirm = 0  
                         for j in range(0, len(stalist), +1):
                             if mylist[i] == stalist[j]:
                                 print(mylist[i] , 'online')
                                 comfirm = 1
                                 break
                         if comfirm != 1:
                            print(mylist[i], 'offline' )
                     

                elif myword[0:3] == "del":
                   mylist.remove(myword[4:8])
                   mylist.sort()

                elif myword[0:4] == "sort":
                   mylist.sort()

             # file is code  in server
 
                elif myword[0:4] == "file":
                   sock.send(myword.encode())
                   UseFile = myword[10:]
                   time.sleep(1) 
                   f = open(UseFile, "rb") #open file
                   ff = f.read()
                   sock.send(ff)
               
              # print(f)
              # print(f.readline())
               


           # elif myword[0:5] == "@talk":
           #    YOU want to Leave?

           # elif myword[0:4] == "send":
              # sock.send(myword.encode())   
            
           # elif myword[0:5] == "close":
            #   DecideClose = 1    #################### Decideclose
             #  sock.send(myword.encode())
              # time.sleep(1)
               #sock.close()
              # print("You can reConnect")
              # while True:
              #     reconnect = input('Type @connect to reconnect: ')
              #     if reconnect == "@connect":
              #        
              #         sock.connect(('localhost', 9522))
              #         sock.send(b'1')
              #         print(sock.recv(1024).decode())
              #         nickName = input('input your nickname: ')
              #         password = input('input your password: ') #input your passwor
              #         NamePass = nickName + '$' + password
              #         sock.send(NamePass.encode())
              #         DecideClose = 0
              #         break
               
               
 
                else:      
                    sock.send(myword.encode())
           # sock.send(password.encode())  
            #print(sock.recv(1024).decode())  
        except ConnectionAbortedError:  
            print('Server closed this connection!')  
        except ConnectionResetError:  
            print('Server is closed!')  
      
def recvThreadFunc():
#    i = 0
    Want = 0  
    global Hide
   # Hide = 1
    while True:  
        try:
            k = 0  
            otherword = sock.recv(1024)
            word = otherword.decode()
           # i+=1
             
            if word[0] == '@':  #add online list
                 for i in range(0, len(stalist), +1):
                     if stalist[i] == word[1:5]:
                         k = 1
                         break
                 if k == 0:
                     stalist.append(word[1:5])
                    # print("****" + word[1:5])
               # print(word[1:5])
         
            elif word[0] == '#':
                 stalist.remove(word[1:5]) #remove offline list

            elif word[0] == '&':
                print("Do You get a file from " + word[1:])
                Want = 1
           
            elif Want == 1:
                print(otherword.decode())
                UUU = nickName + ".txt"
                Recev_file = open(UUU, "wb") #open file
                Recev_file.write(otherword)
                Recev_file.close()
                print("This right")
                Want = 0  

               # YesOrNo = input("Do You get a file from " + word[1:] )
               # YesOrNO = input()

               # if YesOrNo == "yes":
               #     Want = 1

               # else:
               #     Want = 2
               # print("I RE FILE")
               # FileWant = word[1:]
                
             #  f = open("trans.txt", "r")
             #  print(f)
             #  print(f.readline())                 
           # elif Want == 1:
          #  elif word == "$Y":   
          #      print(otherword.decode())
          #      Recev_file = open("bbb.txt", "wb") #open file
          #      Recev_file.write(otherword)
          #      Recev_file.close() 
          #      print("This right")

              #  Want = 0 
          #  elif word == "$N":
          #      print("I have rejected")
             #   Want = 0
             
                
            elif word == "You have wrong password":
                print("You have wrong password, please try again")
                Hide = 1 
               # print(Hide)
               # print(Hide)
               # password = getpass()                                 
               # sock.send(password.encode())
               # break


            elif word == "YOU want to Leave?":
                print("YES Leave")
                stalist.remove(nickName)  #remove the offline man              
                sock.close()
                return
               # break

            else:
                print(otherword.decode()) 

         #   elif word[0] != '@' and word != "You have wrong password":                          
         #       print(otherword.decode())  #@@@@@@@@@@@@@@@@ if condition 
                  
            
           # else:  
           #     pass
                   
        except ConnectionAbortedError:  
            print('Server closed this connection!')  
  
        except ConnectionResetError:  
            print('Server is closed!')  
   # print("WHILE")
   # while True:
   #     sock.close()
   #     reconnect = input('Type @connect to reconnect: ')
   #     if reconnect == "@connect":

   #         sock.connect(('localhost', 9522))
   #         sock.send(b'1')
   #         print(sock.recv(1024).decode())
   #         nickName = input('input your nickname: ')
   #         password = input('input your password: ') #input your password

   #         NamePass = nickName + '$' + password
   #         sock.send(NamePass.encode())
   #         break






  
  
th1 = threading.Thread(target=sendThreadFunc)  
th2 = threading.Thread(target=recvThreadFunc)  
threads = [th1, th2]  
  
for t in threads :  
    t.setDaemon(True)  
    t.start()  
t.join()
