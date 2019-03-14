# Echo client program python3 # # # # # # # # # # # # # # # # # #
import socket, time, threading# # # # # # # # # # # # # # # # # #
class tcolor: # # # # # # # # # # # # # # # # # # # # # # # # # #
    red = "\033[0;31m"# # # # # # # # # # # # # # # # # # # # # #
    green = "\033[0;32m"# # # # # # # # # # # # # # # # # # # # #
    yellow = "\033[0;33m" # # # # # # # # # # # # # # # # # # # #
    blue  = "\033[0;34m"# # # # # # # # # # # # # # # # # # # # #
    magenta = "\033[0;35m"# # # # # # # # # # # # # # # # # # # #
    cyan = "\033[0;36m" # # # # # # # # # # # # # # # # # # # # #
    white = "\033[0;37m"# # # # # # # # # # # # # # # # # # # # #
    RED = "\033[1;31m"# # # # # # # # # # # # # # # # # # # # # #
    GREEN = "\033[1;32m"# # # # # # # # # # # # # # # # # # # # #
    YELLOW = "\033[1;33m" # # # # # # # # # # # # # # # # # # # #
    BLUE  = "\033[1;34m"# # # # # # # # # # # # # # # # # # # # #
    MAGENTA = "\033[1;35m"# # # # # # # # # # # # # # # # # # # #
    CYAN = "\033[1;36m" # # # # # # # # # # # # # # # # # # # # #
    WHITE = "\033[1;37m"# # # # # # # # # # # # # # # # # # # # #
    r1 = '\033[91m' # # # # # # # # # # # # # # # # # # # # # # #
    c1 = '\033[96m' # # # # # # # # # # # # # # # # # # # # # # #
    TEST = '\033[95m' # # # # # # # # # # # # # # # # # # # # # #
    OPAL = '\033[95m' # # # # # # # # # # # # # # # # # # # # # #
    YELLOW2 = '\033[93m'# # # # # # # # # # # # # # # # # # # # #
    FAIL = '\033[91m' # # # # # # # # # # # # # # # # # # # # # #
    BOLD = '\033[1m'# # # # # # # # # # # # # # # # # # # # # # #
    RESET = "\033[0;0m" # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
HOST = '127.0.0.1'    # The server/remote host
PORT = 50007          # The port used by the server
brkTHD = False

def processT(pTime):
    print('Processing...')#,end='')
    for i in range(0,pTime,1):
        #print('.',end='')
        time.sleep(0.5)
        #print('.',end='')
    #print('')

def sendMessageTHD(msg): # Message sending thread
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            t = time.time()
            s.sendall(msg)
            print(tcolor.cyan,'Client sent ', msg.decode(),tcolor.RESET)
            data = s.recv(1024)
            t -= time.time()
            s.close()
        print (tcolor.CYAN,'Client received ',data.decode(),' in ',t,' seconds',tcolor.RESET)
    except: print(tcolor.RED,'Error: Could not establish connection to server')

def treatConnectionTHD(conn,addr): # Message treating thread
    with conn:
        print(tcolor.yellow,'Connection established for ',addr,tcolor.RESET)
        data = conn.recv(1024)
        if data == b'Ping':
            print(tcolor.green,'Server received ',data.decode(),' from ',addr,tcolor.RESET)
            data = b'Pong'
            processT(10)
            conn.sendall(data)
            print(tcolor.GREEN,'Server replied to ',addr,' : ',data.decode(),tcolor.RESET)
        elif data == b'stop':
            print(tcolor.RED,'Terminating the server process', tcolor.RESET)
            conn.sendall(b'Server shutting down')
        else: 
            conn.sendall(b'Invalid Request')
            print(tcolor.red,'Server received invalid data [',data.decode(),'] from ',addr,tcolor.RESET)

def serverTHD():
    print(tcolor.white, 'Server thread created', tcolor.RESET)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try: 
            s.bind((HOST, PORT))    
            print(tcolor.white, 'Server started', tcolor.RESET)
            while brkTHD == False:
                print(tcolor.WHITE,'Server listening for new connections...', tcolor.RESET)
                s.listen(1)
                (connection, address) = s.accept()
                print(tcolor.yellow,'Connection initiated at', address, tcolor.RESET)
                try: threading.Thread(target=treatConnectionTHD, args=(connection, address)).start() # _thread.start_new_thread(treatConnectionTHD,(connection, address))
                except: print(tcolor.RED,'Error: server treating thread could not be created', tcolor.RESET)
        except: print(tcolor.RED,'Error: Binding server adress already in use',tcolor.RESET)
        s.close()
def clientTHD(MAX_MESSAGES, messages):
    msgThreads = []
    message = messages
    try: 
        for i in range(0,MAX_MESSAGES,1):
            thd = threading.Thread(target=sendMessageTHD,args=(message,))
            msgThreads.append(thd)
            thd.start()
            time.sleep(0.5)
    except: print(tcolor.RED,'Error: client message thread could not be created', tcolor.RESET)
    for i in range(0,MAX_MESSAGES,1): msgThreads[i].join()

def main():
    global brkTHD
    try: threading.Thread(target=serverTHD).start()
    except: print(tcolor.RED,'Error: Main server thread could not be created', tcolor.RESET)
    time.sleep(0.5)
    
    nrMessages = 0
    messages = b'Ping'
    while brkTHD == False:
        print(tcolor.BLUE,'\nHow many messages to send? ', tcolor.RESET)
        nrMessages = int(input())
        if (nrMessages == 0):
            brkTHD = True
            messages = b'stop'
            nrMessages = 1
        try: 
            cthd = threading.Thread(target=clientTHD,args=(nrMessages, messages))
            cthd.start()
            cthd.join()
        except: print(tcolor.RED,'Error: Main client thread could not be created', tcolor.RESET)

if __name__ == "__main__":
    main()