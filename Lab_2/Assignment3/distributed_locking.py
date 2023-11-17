import multiprocessing
import select
import socket
import time
from pathlib import Path
from queue import PriorityQueue
from threading import Thread

try:
    TOTAL_MEM = 5
    SIZE = 1024
    PORTS = [9999 + i * 2 for i in range(TOTAL_MEM)]


    class MemberProcess(multiprocessing.Process):
        def __init__(self, ID, **keyword):
            super().__init__(**keyword)
            self.ID = ID
            self.req_time = 0
            self.pending_q = None
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind(("", PORTS[self.ID]))
    
        def server_function(self, halt):
            while not halt():
                ready = select.select([self.sock], [], [], 1)
                if not ready[0]:
                    continue
                data, client_addr = self.sock.recvfrom(SIZE)
                tokens = data.decode().strip().lower().split()
                if tokens[0] == "request":
                    if self.req_time == 0:
                        self.sock.sendto("ok".encode(), client_addr)
                    elif int(tokens[1]) < self.req_time:
                        self.sock.sendto("ok".encode(), client_addr)
                    else:

                        timestamp = int(tokens[1])
                        self.pending_q.put((timestamp, client_addr))

        def acq_lock(self):
            self.req_time = time.time_ns()

            socks = [
                socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                for ID in range(TOTAL_MEM)
            ]

            for ID, sock in enumerate(socks):
                if ID != self.ID:
                    sock.sendto(
                        f"request {self.req_time}".encode(),
                        ("127.0.0.1", PORTS[ID]),
                    )

            def get_ack(sock):
                sock.recvfrom(SIZE)
                sock.close()

            ack_threads = [
                Thread(target=get_ack, args=(sock,))
                for ID, sock in enumerate(socks)
                if ID != self.ID
            ]
            for ack_thread in ack_threads:
                ack_thread.start()
            for ack_thread in ack_threads:
                ack_thread.join()

            print(f"Lock is now successfully acquired by member:  {self.ID}")
            return True

        def release_lock(self):
            while not self.pending_q.empty():
                client_addr = self.pending_q.get()[1]
                self.sock.sendto("OK".encode(), client_addr)
            self.req_time = 0

        def run(self):
            self.pending_q = PriorityQueue(TOTAL_MEM)
            halt = False
            server_thread = Thread(target=self.server_function, args=(lambda: halt,))
            server_thread.start()
            print(f"Member {self.ID} is now starting...")

            time.sleep(1)

            for _ in range(10):
                if self.acq_lock():
                    number = int(Path("shared_data").read_text())
                    number += 1
                    Path("data").write_text(f"{number}\n")
                    self.release_lock()
                else:
                    print(f"*** ERROR *** \n Member {self.ID}: failed to acquire lock")
            print(f"Member {self.ID} done")

            time.sleep(1)
            halt = True
            server_thread.join()


    if __name__ == "__main__":

        Path("shared_data").write_text("0\n")

        members = [MemberProcess(ID=i) for i in range(TOTAL_MEM)]

        for member in members:
            member.start()

        for member in members:
            member.join()


except Exception as x:
    print(f"The following exception occured - \n {x}")