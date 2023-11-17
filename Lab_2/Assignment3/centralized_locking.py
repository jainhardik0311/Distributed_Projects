from multiprocessing import Process
import threading
import os
import socket
import time
import sys

try:
    FORMAT = 'utf-8'
    SIZE = 1024

    class update_file(Process):

        def __init__(self,IP,PORT,proc_count,proc_run_count,fname):
            Process.__init__(self)
            self.IP = IP
            self.PORT = PORT
            self.processes = proc_count
            self.run_count = proc_run_count
            self.fname = fname

        def run(self):
            cor_ser = socket.socket()
            cor_ser.connect((self.IP,self.PORT))
            cor_ser.settimeout(None)
            flag = 0
            count_inc = 0
            while flag < self.run_count:
                while True:
                    time.sleep(self.pid%self.processes)
                    print('Process ID:%s Trying to Acquire Lock' %(self.pid))
                    cor_ser.send(('[SERVER] Acquire Lock' + '\n').encode(FORMAT))
                    coord1 = cor_ser.recv(SIZE).decode(FORMAT)
                    if(coord1 == '[COORDINATOR] Lock is now acquired.'):
                        print('Process ID:%s acquired the lock' %(self.pid))
                        break
                    else:
                        time.sleep(2)
                if os.path.exists(self.fname):
                    doc = open(self.fname,"r+")
                    count_inc = doc.readline().strip()
                    if (count_inc!=''):
                        count_inc = int(count_inc)
                elif(count_inc > self.processes):
                    print('[ERROR] File contains corrupted value.')
                else:
                    doc = open(self.fname,"w")
                    count_inc = 0
                doc.seek(0)
                count_inc += 1
                print("Process ID:%s Updating the count_inc from %s to %s"%(self.pid,count_inc-1,count_inc))
                doc.write(str(count_inc))
                doc.close()
                cor_ser.send(('[SERVER] Release Lock' + '\n').encode(FORMAT))
                coord2 = cor_ser.recv(SIZE).decode(FORMAT)
                if(coord2 != '[COORDINATOR] Lock is now released'):
                    print('[ERROR] Coordinator behaved in an unexpected way. Please try again.')
                print('Process ID:%s Releasing the Lock' %(self.pid))
                time.sleep(1)
                flag += 1
            cor_ser.send(('[SERVER] All tasks are now completed.' + '\n').encode(FORMAT))
            cor_ser.close()
            return True

    class coordinator(threading.Thread):

        def __init__(self,IP,PORT,proc_count):
            threading.Thread.__init__(self)
            self.IP = IP
            self.PORT = PORT
            self.processes = proc_count

        def run(self):
            client = {}
            cor_ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cor_ser.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            cor_ser.bind((self.IP,self.PORT))
            cor_ser.listen(4)
            for i in range(self.processes):
                csocket, address = cor_ser.accept()
                client[address] = csocket
            lock_flag = 0
            while len(client) > 0:
                for address in client:
                    csocket = client[address]
                    csocket.settimeout(1)
                    msg = ""
                    try:
                        msg_queue = csocket.recv(SIZE).decode(FORMAT).split('\n')
                        close_conn = 0
                        for msg in msg_queue:
                            if (msg == '[SERVER] Acquire Lock'):
                                if lock_flag == 0:
                                    lock_flag = 1
                                    msg = '[COORDINATOR] Lock is now acquired.'
                                else:
                                    msg = '[COORDINATOR] Coordinator is busy. Please try again...'
                                csocket.send(msg.encode(FORMAT))
                            if msg == '[SERVER] Release Lock':
                                lock_flag = 0
                                csocket.send('[COORDINATOR] Lock is now released'.encode(FORMAT))
                            if msg == '[SERVER] All tasks are now completed.':
                                print(msg)
                                csocket.close()
                                close_conn = 1
                        if close_conn == 1:
                            client.pop(address,None)
                            break
                    except socket.timeout as e:
                        err = e.args[0]
                        if err == 'timed out':
                            time.sleep(1)
            cor_ser.close()
            return True

    def main():

        IP = 'localhost'
        PORT = 9876
        proc_count = 4
        proc_run_count = 3
        fname = "Test_Shared_File.txt"
        if len(sys.argv) == 3:
            proc_count = int(sys.argv[1])
            proc_run_count = int(sys.argv[2])
        if proc_count < 2:
            print("[SERVER] Number of process cannot be less than two. Changing the number of prcoesses to two.")
            proc_count = 2
        server = coordinator(IP,PORT,proc_count)
        server.start()
        time.sleep(2)
        proc_list = []
        for i in range(proc_count):
            proc_list.append(update_file(IP,PORT,proc_count,proc_run_count,fname))
            proc_list[i].start()
        for i in range(proc_count):
            proc_list[i].join()
        server.join()

    if __name__ == '__main__':
        main()
except Exception as x:
    print(f"The following exception occured - \n {x}")