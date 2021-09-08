import socket
from socket import SHUT_RDWR
import struct
import time
import serial
import cv2
from PIL import Image
import threading
from http.server import BaseHTTPRequestHandler,HTTPServer
from socketserver import ThreadingMixIn
from io import StringIO,BytesIO
import fcntl

# 169.254.214.107
# 169.254.132.242

class Client():

    def __init__(self):
        self.rpi_ip_address = Client.get_ip_address('eth0')
        #self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)
        #self.ser.flush()

    def get_ip_address(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s', bytes(ifname[:15], 'utf-8')))[20:24])

    def Connect(self):
        global c_socket, c_address, sock, sock2, connected
        sock = socket.socket()
        sock2 = socket.socket()
        sock.bind((self.rpi_ip_address, 3000))

        sock.listen(4) 
        c_socket, c_address = sock.accept()

        # Client IP
        self.ip_address = '169.254.132.242'
        sock2.connect((self.ip_address, 4000))
        connected = True

    def Reconnect():
        global c_socket, c_address, sock, sock2, connected
        time.sleep(1)
        sock.listen(4) 
        c_socket, c_address = sock.accept()
        connected = True

    def Capture():
        global capture
        capture = cv2.VideoCapture(0)

        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        capture.set(cv2.CAP_PROP_SATURATION,80)

        global img
        try:
            server = ThreadedHTTPServer(('169.254.214.107', 8080), CamHandler)
            server.serve_forever()
        except KeyboardInterrupt:
            capture.release()
            server.socket.close()
        return capture

    def Capture2():
        global capture2
        capture2 = cv2.VideoCapture(2)

        capture2.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        capture2.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        capture.set(cv2.CAP_PROP_SATURATION,80)
        
        global img2
        try:
            server2 = ThreadedHTTPServer(('169.254.214.107', 8081), CamHandler2)
            server2.serve_forever()
        except KeyboardInterrupt:
            capture2.release()
            server2.socket.close()
        return capture2

    '''
    def old_drive(self):
        global stringdeger_encode
        
        while True:
            try: self.ser.write(stringdeger_encode)	
            except: print("No data.")
    '''

    def driveRuntime():
        global c_socket, c_address, sock, sock2, connected, stringdeger
        try:
            if(connected == True):
                message = "hey"
                data = c_socket.recv(1024).decode()
                sock2.send(message.encode())
                
                stringdeger = data + "S"
                return data
                #print(data)
            
        except ConnectionResetError:
            print("Connection Reset.")
            connected = False
            Client.Reconnect()
        except BrokenPipeError:
            print("Broken Pipe.")
            connected = False
            Client.Reconnect()

    def returnData(data):
        return data


capture=None
capture2=None

class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path.endswith('.mjpg'):
			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()

			while True:
				try:
					rc,img = capture.read()
					if not rc: continue
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
				except KeyboardInterrupt: break
			return

		if self.path.endswith('.html'):
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>'.encode())
			self.wfile.write('<img src="http://169.254.214.107:8080/cam1.mjpg"/>'.encode())
			self.wfile.write('</body></html>'.encode())
			return

class CamHandler2(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path.endswith('.mjpg'):
			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()

			while True:
				try:
					rc,img = capture2.read()
					if not rc: continue
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
				except KeyboardInterrupt: break
			return

		if self.path.endswith('.html'):
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>'.encode())
			self.wfile.write('<img src="http://169.254.214.107:8080/cam2.mjpg"/>'.encode())
			self.wfile.write('</body></html>'.encode())
			return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ Request Handle """