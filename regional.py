import socket

regional_local_sock = socket.socket()
regional_local_sock.bind(("0.0.0.0", 1555))
regional_local_sock.listen(3)

regional_central_sock = socket.socket()
try:
    regional_central_sock.connect(("127.0.0.1", 1666))
except Exception as e:
    regional_central_sock.close()
    exit(f"server is down try again later {str(e)}")

ip_to_name = {"127.0.0.1": "yourself", "8.8.8.8": "google"}
name_to_ip = {"yourself": "127.0.0.1", "google": "8.8.8.8"}

while True:

    localsock, addr = regional_local_sock.accept()
    print(f"{addr[0]} - connected")

    while True:
        found = False
        result = ""
        data = localsock.recv(1024).decode()
        if data.lower() == "exit" or data == "":
            localsock.close()
            break
        ip_or_name = data.split('/')[0]
        choose = data.split('/')[1]
        if choose.lower() == "ip":
            if ip_or_name in ip_to_name:
                found = True
            if found:
                result = ip_to_name[ip_or_name]
            else:
                print("are you dumb? please enter a valid ip")

        elif choose.lower() == "name":
            if ip_or_name in name_to_ip:
                found = True
            if found:
                result = name_to_ip[ip_or_name]

        if (found == False):
            try:
                regional_central_sock.send(f"{ip_or_name}/{choose}".encode())
                result = regional_central_sock.recv(1024).decode()
            except Exception as e:
                regional_central_sock.close()
                exit(f"error in rcv or send {str(e)}")

        if result != '0':
            if choose.lower() == "ip":
                ip_to_name[ip_or_name] = f"{result}"
                name_to_ip[result] = f"{ip_or_name}"

            elif choose.lower() == "name":
                name_to_ip[ip_or_name] = f"{result}"
                ip_to_name[result] = f"{ip_or_name}"

        localsock.send(f"{result}".encode())
        print(result)