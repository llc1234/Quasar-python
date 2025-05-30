import socket
import threading



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)

lo = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
lo.connect(("8.8.8.8", 80))

IP = lo.getsockname()[0]
PORT = 5050

print("Start CLient...")
print("IP  : ", IP)
print("PORT: ", PORT)




def main():
    while True:
        s.send(bytes("<START:CMD>0000000000000000000000000<END:ALL>", "utf-8"))
        s.send(bytes("<START:CMD>1111111111111111111111111<END:ALL>", "utf-8"))


def SendUserDATA():
    s.send(bytes("<USERDATASTART>Laptop\nKevin@LAPTOP\n1.3.8\nConnected\nActive\nGermany\nWindows 11\nUser<USERDATAEND>", "utf-8"))
    main()

try:
    s.connect((IP, PORT))
    print("Connecting")
    SendUserDATA()
except:
    print("ERROR: Connecting")