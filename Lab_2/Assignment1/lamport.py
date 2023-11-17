import socket
import time
import multiprocessing
import json
import threading

from collections import defaultdict, namedtuple

from heapq import heappop, heappush

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
            # Socket is created
            self.socket.bind(("localhost", PORT[id]))

        def run(self):
            while True:
                data = self.socket.recvfrom(Buffer_size)[0]
                message = json.loads(data.decode())

                events = Event(clock=message["clock"], pid=message["pid"])
                if message["type"] == MSG_ACK:
                    self.acks[events] += 1
                    if self.queue:
                        if self.acks[self.queue[0]] >= No_of_Process:
                            self.deliver(heappop(self.queue))
                        elif not self.acknowledged[self.queue[0]]:
                            with self.clock.get_lock():
                                self.clock.value += 1
                            message = dict(type=MSG_ACK, pid=events.pid, clock=events.clock)
                            data = json.dumps(message).encode()
                            for port in PORT:
                                self.socket.sendto(data, ("localhost", port))
                            self.acknowledged[events] = True
                elif message["type"] == EVENTS:
                    with self.clock.get_lock():
                        self.clock.value += 1

                    heappush(self.queue, events)
                    self.acks[events] = 0

                    if not self.acknowledged[events]:
                        with self.clock.get_lock():
                                self.clock.value += 1
                        message = dict(type=MSG_ACK, pid=events.pid, clock=events.clock)
                        data = json.dumps(message).encode()
                        for port in PORT:
                            self.socket.sendto(data, ("localhost", port))
                        self.acknowledged[events] = True

        def deliver(self, events):
                print(f"P{self.id}: Event Processed Successfully P{events.pid}.{events.clock}\n")


    class MemberProcess(multiprocessing.Process):
        def __init__(self, id, **keyword):
            super().__init__(**keyword)
            self.id = id
            self.clock = multiprocessing.Value("i", 0)
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        def run(self):
            comm_thread = Comm_Thread(id=self.id, clock=self.clock)
            comm_thread.start()

            time.sleep(0.01)

            for _ in range(3):

                time.sleep(0.01)

                with self.clock.get_lock():
                    self.clock.value += 1
                message = dict(pid=self.id, clock=self.clock.value, type=EVENTS)
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