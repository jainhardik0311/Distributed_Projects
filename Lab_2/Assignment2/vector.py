import socket
import time
import multiprocessing
import json
import threading

from collections import defaultdict, namedtuple

try:
    class Comm_Thread(threading.Thread):
        def __init__(self, id, clock, **keyword):
            super().__init__(**keyword)
            self.clock = clock
            self.id = id
            self.acks = defaultdict(int)
            self.acknowledged = defaultdict(bool)
            self.queue = []

                       
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            self.socket.bind(("localhost", PORT[id]))
            
        def deliver(self, event):
            pid = event["pid"]
            print("P{}: Processed event P{}.{}".format(self.id, pid, event["clock"][pid]))

        def run(self):
            while True:
                
                data = self.socket.recvfrom(Buffer_size)[0]
                message = json.loads(data.decode())
                self.queue.append(message)

                ready_indices = []
                for i, m in enumerate(self.queue):
                    pid = m["pid"]
                    if pid != self.id and m["clock"][pid] != self.clock[pid] + 1:
                        continue
                    for k in range(No_of_Process):
                        if k != pid and m["clock"][pid] > self.clock[pid]:
                            continue
                    ready_indices.append(i)
                    self.deliver(m)

                for i in ready_indices[::-1]:
                    self.queue.pop(i)

                for id in range(No_of_Process):
                    self.clock[id] = max(self.clock[id], message["clock"][id])


    class MemberProcess(multiprocessing.Process):
        def __init__(self, id, **keyword):
            super().__init__(**keyword)
            self.id = id
            self.clock = [0] * No_of_Process
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        def run(self):
            comm_thread = Comm_Thread(id=self.id, clock=self.clock)
            comm_thread.start()

            time.sleep(0.01)

            self.clock[self.id] += 1
            message = dict(pid=self.id, clock=self.clock)
            print(f"P{self.id}: Creating event P{self.id}.{message['clock'][self.id]}")
            data = json.dumps(message).encode()
            for port in PORT:
                self.socket.sendto(data, ("localhost", port))

            print(f"\nP{self.id}: Event Sent successfully: P{self.id}.{message['clock']}\n")


    No_of_Process = 3
    PORT = [9999 + i for i in range(No_of_Process)]
    Buffer_size = 2048

    EVENTS = 0
    MSG_ACK = 1

    Event = namedtuple("Event", ["clock", "pid"])


    if __name__ == "__main__":

        members = [MemberProcess(id=i) for i in range(No_of_Process)]

        for member in members:
            member.start()
            time.sleep(0.01)
            
        for member in members:
            member.join()
except Exception as x:
    print(f"The following exception occured - \n {x}")