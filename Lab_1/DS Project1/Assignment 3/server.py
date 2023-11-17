import socket
import os
import threading
import pickle
import numpy as np
import json
import time

ThreadCount = 0

server = socket.socket()
print("[Starting] Socket is created & Server is Starting")

server.bind(("localhost", 9999))

server.listen(5000)
print("[Listenning] Waiting for connections")

# os.makedirs("Server", exist_ok=True)
# os.chdir("Server")


# def threaded_client():

try:

    def calculate_pi():
        denominator = 1
        sum = 0

        for i in range(1000000):
            # even index elements are positive
            if i % 2 == 0:
                sum += 4 / denominator
            else:
                # odd index elements are negative
                sum -= 4 / denominator
            # denominator is odd
            denominator += 2
        message = f"Value of pi = {sum}"
        client.sendall(message.encode())
        print("\nOperation has been performed and pi's value has been sent to client\n")

    def add():
        num1 = int(client.recv(1024).decode())
        num2 = int(client.recv(1024).decode())
        result = num1 + num2
        print(result)
        message = f"Operation has been performed and addition of {num1} and {num2} is {result}"
        client.sendall(message.encode())
        print(
            f"\nOperation has been performed and addition of {num1} and {num2} is sent to CLient.\n"
        )

    def sort():
        data = client.recv(4096)
        data_received = pickle.loads(data)
        print(f"Entered elelements are {data_received}")
        data_received.sort()
        # print(sortedlist)
        datatosend = pickle.dumps(data_received)
        client.send(datatosend)
        print(
            f"\nOperation has been performed and sorted elements are sent to client.\n"
        )

    def matrix_mul():
        dataMatrixA = client.recv(4096).decode()
        data_MatrixA = json.loads(dataMatrixA)
        print(f"Entered elements in first matrix are {dataMatrixA}")

        dataMatrixB = client.recv(4096).decode()
        data_MatrixB = json.loads(dataMatrixB)
        print(f"Entered elements in second matrix are {dataMatrixB}")

        #dataMatrixC = client.recv(4096).decode()
        #dataMatrixC = json.loads(dataMatrixC)
        matrixC = []
        matrixC = np.matmul(data_MatrixA, data_MatrixB)
        matrixC = pickle.dumps(matrixC)
        client.sendall(matrixC)

        print("\nOperation has been performed and result has been sent to client.\n")
        result()

    while True:
        client, addr = server.accept()
        print("Connected with ", addr)

        client.sendall(bytes("Welcome to Hardik's server".encode("utf-8")))
        option = client.recv(1024).decode("utf-8")
        print(f"The selected options is: {option}")
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
    server.close()

except:
    print("An exception occurred")

#    t = threading.Thread(target=threaded_client)
#    t.start()
#    ThreadCount += 1
#    print("Thread Number: " + str(ThreadCount))
