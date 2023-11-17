import socket
import os

try:

    def recurrence():
        client = socket.socket()

        client.connect(("localhost", 9999))

        print(client.recv(1024).decode())  # Shows the welcome server message

        print("\nSelect operations to be performed: ")
        print(
            "\n 1. Insert 1 for Download \n 2. Insert 2 for Upload \n 3. Insert 3 for Rename \n 4. Insert 4 for Delete \n"
        )
        option = str(input("Insert number of operation to be performed: "))
        client.sendall(f"{option}".encode("utf-8"))

        os.makedirs("Client1", exist_ok=True)
        os.chdir("Client1")

        def upload():
            print("\nOperation has been performed\n")
            print(client.recv(1024).decode())  # Prints the filename and filesize
            with open("received.txt", "a+") as f:
                # read 1024 bytes from the socket (receive)
                bytes_read = client.recv(1024)
                str_read = str(bytes_read)
                f.write(str_read)

        def download():
            with open("mytext2.txt", "w") as f:
                f.write("Debugging at its best")

            with open("mytext2.txt") as f:
                message = f.read()

            filename = "mytext2.txt"
            # get the file size
            filesize = os.path.getsize(filename)
            dataToSend = (
                "Recieved filename is: "
                + filename
                + " & its filesize is: "
                + str(filesize)
                + "\n"
            )
            client.sendall(dataToSend.encode())
            print("\n")
            with open(filename, "rb") as f:
                while True:
                    # read the bytes from the file
                    bytes_read = f.read()
                    if not bytes_read:
                        # file transmitting is done
                        break
                    client.sendall(bytes_read)
            print("\nThe Operation has been performed\n")

        def rename():
            Currentserverlist = client.recv(1024).decode()
            print("\nThe files present in the current directory are displayed below\n")
            print(Currentserverlist)
            oldname = str(input("\nEnter the file name which needs to be renamed: \n"))
            client.send(oldname.encode())
            newname = str(input("\nEnter new file name: \n"))
            client.send(newname.encode())

        def delete():
            Currentserverlist = client.recv(1024).decode()
            print("\nThe files present in the current directory are displayed below\n")
            print(Currentserverlist)
            filename = str(input("\nEnter the file name which needs to be renamed: \n"))
            client.sendall(filename.encode())
            print("\nThe operation has been performed.\n")

        if option == "1":
            upload()
        elif option == "2":
            download()
        elif option == "3":
            rename()
        elif option == "4":
            delete()
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

except:
    print("An exception occurred")
