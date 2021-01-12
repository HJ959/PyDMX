import socket
import re
#b   'Some\x00\x00\x00\x00,s\x00\x00words\x00\x00\x00'
re_udp_audiofile = re.compile(r"b'<(.+?)>")
re_udp_clockin = re.compile(r"b'{(.+?)}")

UDP_IP = ""
UDP_PORT = 5005


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    udp_string = re.search(re_udp_audiofile, str(data))
    if udp_string:
        print(udp_string.group(1))

    udp_clock = re.search(re_udp_clockin, str(data))
    if udp_clock:
        print(udp_clock.group(1))

