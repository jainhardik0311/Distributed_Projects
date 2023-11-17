I have neither given nor received unauthorized assistance on this work.
Signed:    
Hardik Jain (ID: 1001954448)					                                          Date: 11/05/2021
Samyak Jain (ID: 1002003127)


***** README *****
 
In this project we have implemented following three algorithms.

Assignment 1:

1 - Total Ordered multi-cast using Lamport’s Algorithm:

We used UDP socket-based communication to communicate between processes. 
Our main function creates N processes, each with a unique process id or PID and a separate port number. 
Each process has two threads: 
1.	One for sending events and 
2.	Another for receiving events and sending acknowledgements to/from other processes. 
The process increments its logical clock and multicasts the event to all processes in the group when an event happens. 

Assignment 2:

2 - Vector Clock:

We used UDP socket-based communication to communicate between processes. 
Our main function creates N processes, each with a unique process id or PID and a separate port number. 
Each process has two threads: 
1.	One for generating events
2.	Another for handling all incoming messages.
Each process has its own independent local vector clock. When an event occurs, each process changes its vector clock and sends it along with the message to all other processes. Each process saves the incoming message in a buffer and then processes it. The process changes its vector clock after the message has been sent.

Assignment 3:

3.1 - Centralized algorithm:

In centralized algorithm coordinator controls the resource allocation. 
At a time only one process will acquire the lock to access the resource. 
Each process asks the coordinator for accessing the resource, if resources is not allocated to any process coordinator grants the permission. 
If resource is allocated to other process, it will not reply immediately. 
Processes keep requesting lock until successfully acquiring the lock.
We implemented all the communications between members and coordinators using the connection-oriented reliable TCP protocol.

3.2 - Distributed Peer-to-Peer Locking:

There is no centralized coordinator in the distributed peer-to-peer locking method. To obtain the lock to a shared resource, a member must send a lock request to every other member and receive an affirmative response from each of them. Each member must also perform the functions of the coordinator in this approach, which means that each member process has two threads: one that accesses and works on the shared resource, and the other that listens for and replies to lock request messages.

Learning’s

•	Learned socket programming in python
•	Multi-casting using sockets
•	Multi-threaded programming in python
•	Learned to synchronize messages between processes
•	By implementing these algorithms gained insight into how distributed system’s work.
•	Also got better understanding of all the above algorithms

Challenges Encountered
•	Initially didn’t know how to implement socket programming in python. 
•	Faced challenges while handling message communication between multiple process.



