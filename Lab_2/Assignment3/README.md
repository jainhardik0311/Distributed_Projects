Assignment 3:
Steps to run the Centralized coordinated locking and distributed locking 
Steps to Run
1. python3 centralized_locking.py
2. python3 distributed_locking.py

** Please run the program using python3 **

We can use Visual Studio Code, PyCharm or any other ide. We used Visual Studio Code, however it is Linux compatible.

We created a counter file called data with the value "0" at the start of each test.
Then we started five separate member processes, each of which will increase the value in the 'data' file by ten times. As a result, the data file should have the value "50" when all actions have been successfully performed.