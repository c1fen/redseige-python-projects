#!/usr/bin/env python3

import sys
import requests
import argparse
import socket

parser = argparse.ArgumentParser(description='Loads header info based on url/file input')
parser.add_argument('-u','--url', help='webpage to load')
parser.add_argument('-f','--file', help='read from file')

args = vars(parser.parse_args())

lines = []

if args['url']:
	lines.append(args['url'])

if args['file']:
	f = open(args['file'],"r")
	for line in f.readlines():
		lines.append(line.strip("\n"))

for line in lines:

  #do the thing
	try:
		response = requests.get(line)

		#variables
		protocol = ' '
		sts = ' '
		csp = ' '
		xfo = ' '
		svr = ''

		prefix = line.split("://")[0]
		hostname = line.split("://")[1].split("/")[0]

		if prefix == 'http':
			protocol = 'http'
		elif prefix == 'https':
			protocol = 'https'
		else:
			protocol = 'unknown protocol'

		r = requests.get(line)
		ip_addr = socket.gethostbyname(hostname)

		#check sts
		if 'Strict-Transport-Security' in r.headers:
			if protocol == 'http':
				sts = 'Ignore'
			else:
				sts = '+'

		#check Content-Security-Policy
		if 'Content-Security-Policy' in r.headers:
			csp = '+'

		#check X-Frame-Options
		if 'Content-Security-Policy' in r.headers:
			xfo = '+'

		#check if any server headers
		if 'Server' in r.headers:
			svr = r.headers['server']
		
		print("========================================")
		print(f"{'URL: ':<5}{line:<40}")
		print("========================================")
		print(
			f"{'IP: ':<5}{str(ip_addr):>35}",
			f"\n{'Server: ':<5}{svr:>32}",
			f"\n{'Protocol: ':<30}{protocol:>10}",
			f"\n{'Strict-Transport-Security: ':<30}{'[' + sts + ']':>10}",
			f"\n{'Content-Security-Policy: ':<30}{'[' + csp + ']':>10}",
			f"\n{'X-Frame-Options: ':<30}{'[' + xfo + ']':>10}"
		)
		print("----------------------------------------\n")

	except:
		print("========================================")
		print(f"{'URL: ':<5}{line:<40}")
		print("========================================")
		print("url not recognized :(")
		print("----------------------------------------\n")
		

