import socket
from socket import SHUT_RDWR
import fcntl
import struct
import time
import serial
import cv2
from PIL import Image
import threading
from http.server import BaseHTTPRequestHandler,HTTPServer
from socketserver import ThreadingMixIn
from io import StringIO,BytesIO
capture=None

class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path.endswith('.mjpg'):
			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()
			while True:
				try:
					rc,img = capture.read()
					if not rc:
						continue
					imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
					jpg = Image.fromarray(imgRGB)
					tmpFile = BytesIO()
					jpg.save(tmpFile,'JPEG')
					self.wfile.write("--jpgboundary".encode())
					self.send_header('Content-type','image/jpeg')
					self.send_header('Content-length',str(tmpFile.getbuffer().nbytes))
					self.end_headers()
					jpg.save(self.wfile,'JPEG')
					time.sleep(0.05)
				except KeyboardInterrupt:
					break
			return
		if self.path.endswith('.html'):
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>'.encode())
			self.wfile.write('<img src="http://169.254.214.107:8080/cam.mjpg"/>'.encode())
			self.wfile.write('</body></html>'.encode())
			return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""Handle requests in a separate thread."""
	
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15], 'utf-8'))
    )[20:24])

def baglan():
	global c_socket, c_address, sock, sock2, connected
	sock = socket.socket()
	sock2 = socket.socket()
	sock.bind((rpi_ip_address, 3333))
	print("Socket olusturuldu!")

	sock.listen(4) 
	c_socket, c_address = sock.accept()
	print(c_address, "Dinleme baglantisi kuruldu!")

	sock2.connect((ip_address, 4444))
	print("Gonderme baglantisi kuruldu!")
	connected = True
	print("a")

def yenidenBaglan():
	global c_socket, c_address, sock, sock2, connected
	
	#sock2.shutdown(SHUT_RDWR)
	#sock2.close()
	#sock.shutdown(SHUT_RDWR)
	#sock.close()
	time.sleep(1)
	print("bitti")
	#sock = socket.socket()
	#sock.bind((rpi_ip_address, 3333))
	sock.listen(4) 
	c_socket, c_address = sock.accept()
	print(c_address, "Dinleme baglantisi kuruldu!")
	connected = True

rpi_ip_address = get_ip_address('eth0')
ip_address = ""

templines = []



with open('config.txt') as f:
	templines = f.readlines()
	
for line in templines:
	if "ip_address:" in line:
		ips = line.split(':')
		
		ip_address = ips[1]
		
		
def kamera():
	global capture
	capture = cv2.VideoCapture(0)
	capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320); 
	capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240);
	capture.set(cv2.CAP_PROP_SATURATION,0.2);
	global img
	try:
		server = ThreadedHTTPServer(('169.254.214.107', 8080), CamHandler)
		print( "server started")
		server.serve_forever()
	except KeyboardInterrupt:
		capture.release()
		server.socket.close()

def hareket():
	global stringdeger_encode
	while True:
		try:
			ser.write(stringdeger_encode)	
		except:
			print("DATA YOK")
	
kameraThread = threading.Thread(target=kamera)

kameraThread.start()

#hareketThread = threading.Thread(target=hareket)

#hareketThread.start()


baglan()


ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)
ser.flush()

while True:
	global c_socket, c_address, sock, sock2, connected, stringdeger_encode
	
	
	
	try:
		if(connected == True):
			message = "hey"
			data = c_socket.recv(1024).decode()
			#print("mesaj: ", data)
	
			sock2.send(message.encode())
			
			stringdeger = data + "S"
			stringdeger_encode = stringdeger.encode()
			ser.write(stringdeger_encode)	
			#time.sleep(0.025)
			print(stringdeger);
		
	except ConnectionResetError:
		print("HATA!")
		connected = False
		yenidenBaglan()
	except BrokenPipeError:
		print("HATA!")
		connected = False
		yenidenBaglan()
