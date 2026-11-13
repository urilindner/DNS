import socket

central_sock = socket.socket()
central_sock.bind(("0.0.0.0", 1666))
central_sock.listen(3)

ip_to_name = {"127.0.0.1": "yourself", "8.8.8.8": "google", "1.1.1.1": "cloudflare", "4.2.2.1": "microsoft"}
name_to_ip = {"yourself": "127.0.0.1", "google": "8.8.8.8", "cloudflare": "1.1.1.1", "microsoft": "4.2.2.1"}

while True:

    regional_central_sock, addr = central_sock.accept()
    print(f"{addr[0]} - connected")

    while True:
        found = False
        result = ""
        data = regional_central_sock.recv(1024).decode()
        if data.lower() == "exit" or data == "":
            regional_sock.close()
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

        if found == False:
            result = '0'

        regional_central_sock.send(f"{result}".encode())
        print(result)