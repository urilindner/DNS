import socket

localsock = socket.socket()

ip_to_name = {}
name_to_ip = {}

try:
    localsock.connect(("127.0.0.1", 1555))
except Exception as e:
    localsock.close()
    exit(f"server is down try again later {str(e)}")

while True:
    found = False
    result = ""

    choose = input("choose IP or DOMAIN name(for Domain name enter name): ")

    if choose.lower() == "exit":
        try:
            localsock.send("exit".encode())
        except Exception as e:
            localsock.close()
            exit(f"error in send {str(e)}")
        break

    ip_or_name = input("enter IP or DOMAIN name: ")

    if ip_or_name in name_to_ip or ip_or_name in ip_to_name:
        found = True
    if found:
        if choose.lower() == "ip":
            result = ip_to_name[ip_or_name]
        elif choose.lower() == "name":
            result = name_to_ip[ip_or_name]

        else:
            print("are you dumb? please enter ip or DOMAIN name!!!")
            continue

    if (found == False):
        try:
            localsock.send(f"{ip_or_name}/{choose}".encode())
            result = localsock.recv(1024).decode()
        except Exception as e:
            localsock.close()
            exit(f"error in rcv or send {str(e)}")

    if result != '0':
        if choose.lower() == "ip":
            ip_to_name[ip_or_name] = f"{result}"
            name_to_ip[result] = f"{ip_or_name}"

        elif choose.lower() == "name":
            name_to_ip[ip_or_name] = f"{result}"
            ip_to_name[result] = f"{ip_or_name}"
    else:
        print("try anther ip/Domain name")
        continue

    print(result)