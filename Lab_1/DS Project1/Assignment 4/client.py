import socket
import os
import pickle
import numpy as np
import json
import time
import threading
import logging

threadcount = 0

logging.basicConfig(
    level=logging.DEBUG,
    format="(%(threadName)-10s) %(message)s",
)

client = socket.socket()

client.connect(("localhost", 9999))

print(client.recv(1024).decode())  # Shows the welcome server message

print("Hello. Welcome to my Async server...")
# print("\nSelect operations to be performed: ")
# print(
#    "\n 1. Insert 1 to Calculate Pi's value \n 2. Insert 2 to perform addition on 2 numbers \n 3. Insert 3 to sort array \n 4. Insert 4 for Matrix multiplication \n"
# )
# option = str(input("Insert number of operation to be performed: "))
# client.sendall(f"{option}".encode("utf-8"))

try:

    def calculate_pi():
        logging.debug("Starting Calculate PI")
        time.sleep(0.5)
        print(client.recv(1024).decode())  # Prints the value of PI
        print("\nOperation has been performed\n")
        logging.debug("Exiting Calculate PI")

    def add():
        logging.debug("Starting Add")
        time.sleep(3)
        num = input("Enter two numbers: ")
        client.send(num.encode())
        # num2 = input("Enter second number: ")
        # client.send(num2.encode())
        print("Operation is being performed at server end. Please wait")
        time.sleep(3)
        message = client.recv(1024).decode()
        print(f"\n{message}\n")
        logging.debug("Exiting Add")

    def sort():
        demolist = []
        list_length = int(input("Please enter the length of items to be sorted: "))
        for i in range(list_length):
            element = input("Enter element: ")
            demolist.append(element)

        print("\nEntered array elements are :", demolist)
        data = pickle.dumps(demolist)
        client.send(data)
        print("Operation is being performed at server end. Please wait")
        time.sleep(3)
        datarecieved = client.recv(4096)
        sorted_data = pickle.loads(datarecieved)
        print(f"\nElements after sorting: {sorted_data}\n")

    def matrix_mul():
        def matrixA():
            R1 = int(input("Enter the number of rows for first matrix:"))
            C1 = int(input("Enter the number of columns for second matrix:"))

            matrixA = []  # Initialize matrix
            print("Enter the entries rowwise for 1st Matrix:")

            # For user input
            for i in range(R1):  # A for loop for row entries
                a = []
                for j in range(C1):  # A for loop for column entries
                    a.append(int(input()))
                matrixA.append(a)
            data1 = json.dumps([matrixA])
            client.sendall(data1.encode())

        def matrixB():
            R2 = int(input("Enter the number of rows for second matrix:"))
            C2 = int(input("Enter the number of columns for second matrix:"))

            matrixB = []  # Initialize matrix
            print("Enter the entries rowwise for 2nd Matrix:")

            # For user input
            for i in range(R2):  # A for loop for row entries
                a = []
                for j in range(C2):  # A for loop for column entries
                    a.append(int(input()))
                matrixB.append(a)

            data2 = json.dumps([matrixB])
            client.sendall(data2.encode())

        def matrixC():
            matrixC = []  # Initialize matrix
            data3 = json.dumps([matrixC])
            client.sendall(data3.encode())

        logging.debug("Starting Matrix")
        matrixA()
        matrixB()
        matrixC()

        def result():
            result = client.recv(4096)
            result = pickle.loads(result)
            print("Matrix multiplication of the above entered matrix is as follows \n")
            print(result)

        print("Operation is being performed at server end. Please wait")
        result()
        logging.debug("Exiting Matrix")

        # if option == "1":
        # calculate_pi()
        # elif option == "2":
        # add()
        # elif option == "3":
        # sort()
        # elif option == "4":
        #    matrix_mul()
        # else:
        #    print(
        #        "Incorrect Option Selected. \nPlease run the code again with the correct option"
        #   )

    t1 = threading.Thread(name="calculate_pi", target=calculate_pi)
    threadcount += 1
    print("Thread Number: " + str(threadcount))
    t1.start()

    t2 = threading.Thread(name="add", target=add)
    threadcount += 1
    print("Thread Number: " + str(threadcount))
    t2.start()

    t3 = threading.Thread(name="sort", target=sort)
    threadcount += 1
    print("Thread Number: " + str(threadcount))
    t3.start()

    t4 = threading.Thread(name="matrix_mul", target=matrix_mul)
    threadcount += 1
    print("Thread Number: " + str(threadcount))
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()

    client.close()

except Exception as x:
    print(x)
