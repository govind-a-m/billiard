import time
import socket
import  re

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',5003))
s.listen(5)
c,addr = s.accept()
print('connected')
count = 0
while True:
	try:
		data = c.recv(1024).decode()
		if data:
			count = count+len(re.findall('\n', data))
			print(data,count)
		else:
			break
	except:
		break
