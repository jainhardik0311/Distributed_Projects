import socket
import os
import pickle
import numpy as np
import json
import time


#try:

def recurrence():
    client = socket.socket()

    client.connect(("localhost", 9999))
    print()
    print(client.recv(1024).decode())  # Shows the welcome server message

    print("\nSelect operations to be performed: ")
    print(
        "\n 1. Insert 1 to Calculate Pi's value \n 2. Insert 2 to perform addition on 2 numbers \n 3. Insert 3 to sort array \n 4. Insert 4 for Matrix multiplication \n"
    )
    option = str(input("Insert number of operation to be performed: "))
    client.sendall(f"{option}".encode("utf-8"))

    def calculate_pi():
        time.sleep(3)
        print(client.recv(1024).decode())  # Prints the value of PI
        print("\nOperation has been performed\n")

    def add():
        num1 = input("Enter first number: ")
        client.send(num1.encode())
        num2 = input("Enter second number: ")
        client.send(num2.encode())
        print("Operation is being performed at server end. Please wait")
        time.sleep(3)
        message = client.recv(1024).decode()
        print(f"\n{message}\n")

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
        R1 = int(input("Enter the number of rows for first matrix:"))
        C1 = int(input("Enter the number of columns for second matrix:"))
        
        matrixA = []  # Initialize matrix
        print("Enter the entries rowwise for 1st Matrix:")

            # For user input
        for i in range(0,R1):  # A for loop for row entries
            a = []
            for j in range(0,C1):  # A for loop for column entries
                a.append(int(input()))
            matrixA.append(a)
        data1 = json.dumps([matrixA])
        client.sendall(data1.encode())

        R2 = int(input("Enter the number of rows for second matrix:"))
        C2 = int(input("Enter the number of columns for second matrix:"))

        matrixB = []  # Initialize matrix
        print("Enter the entries rowwise for 2nd Matrix:")

        # For user input
        for l in range(0,R2):  # A for loop for row entries
            b = []
            for m in range(0,C2):  # A for loop for column entries
                b.append(int(input()))
            matrixB.append(b)
        data2 = json.dumps([matrixB])
        client.sendall(data2.encode())

        #matrixC = []  # Initialize matrix
        #data3 = json.dumps([matrixC])
        #client.sendall(data3.encode())

        result = client.recv(4096)
        result = pickle.loads(result)
        print("Matrix multiplication of the above entered matrix is as follows \n")
        print(result)

        print("Operation is being performed at server end. Please wait")

    if option == "1":
        calculate_pi()
    elif option == "2":
        add()
    elif option == "3":
        sort()
    elif option == "4":
        matrix_mul()
    else:
        print(
            "Incorrect Option Selected. \nPlease run the code again with the correct option"
        )

    client.close()

recurrence()

while True:
    num = input("Please enter 1 to continue or 2 to exit: ")
    if num == "1":
        recurrence()
    else:
        quit()

#except:
#   print("An exception occurred")
