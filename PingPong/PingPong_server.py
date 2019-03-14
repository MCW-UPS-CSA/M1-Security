# Echo server program python3
import socket, time, threading # , _thread

HOST = '127.0.0.1' # Server address
PORT = 50007       # Arbitrary non-privileged port

def treatConnectionTHD(conn,addr): # Message treating thread
    with conn:
        print('Connection established for ', addr)
        data = conn.recv(1024)
        if data == b'Ping':
            print('received ', data.decode())
            data = b'Pong'
            time.sleep(5)
            conn.sendall(data)
            print('Replied to ', addr,' : ', data.decode())
        else: 
            conn.sendall(b'Invalid Request')
            print('Invalid data received from ',addr)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        while 1:
            print('Listening for new connections')
            s.listen(1)
            (connection, address) = s.accept()
            print('Connection accepted at', address)
            try: threading.Thread(target=treatConnectionTHD, args=(connection, address)).start() # _thread.start_new_thread(treatConnectionTHD,(connection, address))
            except: print('Error: Thread could not be created')
        
if __name__ == "__main__":
    main()

