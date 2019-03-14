# Echo client program python3
import socket, time, threading

HOST = '127.0.0.1'    # The remote host
PORT = 50007              # The same port as used by the server

def sendMessageTHD(msg): # Message sending thread
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            t = time.time()
            s.sendall(msg)
            print('sent ', msg.decode())
            data = s.recv(1024)
            t -= time.time()
        print ('Received', data.decode(), ' in ', t, ' seconds')
    except: print('Error: Could not establish connection to server')

def main():
    MAX_MESSAGES = 5
    threads = []
    message = b'Ping'
    try: 
        for i in range(0,MAX_MESSAGES,1):
            thd = threading.Thread(target=sendMessageTHD,args=(message,))
            threads.append(thd)
            thd.start()
            time.sleep(0.5)
    except: print('Error: thread could not be created')

    for i in range(0,MAX_MESSAGES,1): threads[i].join()

if __name__ == "__main__":
    main()
