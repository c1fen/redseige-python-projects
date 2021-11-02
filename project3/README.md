>Project 3 - Brute Force!
>
>Scenario: You are working on an internal penetration test for Red Planet and have found a system that your point of contact labeled as "mission critical" has SSH enabled. Due to other findings on the network you know that the security administrator has weak passwords on lots of critical systems. Knowing this, you believe that you can password spray/brute force your way to victory.
>
>Beginner Task: Write a script that will perform a password spray against the SSH service using a single username and password list. It should output each time a username/password combination is failed, and stop on a successful log in.
>
>Intermediate Task: Give your script the added functionality to spray using a list of usernames and a single password, using lists for both usernames and passwords, as well as a traditional brute force options.
>
>Expert Task: Add the option to limit login attempts based on time. Example, run 5 login attempts, wait 60 seconds, run 5 more attempts, wait 60 seconds, repeat.
>
>In order to test this you will need a service running SSH. I suggest setting up something on your local network to test against. Be mindful when setting this up, if you put something internet facing with a weak username/password combination you run the risk at someone on the internet doing the same thing we are and getting popped.

For this project, I identify a couple of problems to solve:

1. I will need to set up my user to allow password authentication and start the ssh service locally
2. SSH is an encrypted protocol. I don't know if this means I will need to encrypt the data I am sending, or even configure the TLS handshake within the python code
3. Once any necessary encryption is sorted, I need to send the data in a format compliant with the SSH protocol


One security concern mentioned is having the local ssh service enabled. I'm not too worried about this, as I'm operating this from within my Kali VM which is operating via NAT with my Windows host.
Inside the Kali VM I don't have any vpns open to the usual pentesting labs which could expose me to attacks from users in those environments.
Attacks originating from outside the VM (directly from internet rather than via vpn) are unlikely given a few reasons:

1. the Kali VM has NAT with my Windows host so they "share" an IP from the perspective of other devices in my home network, and anyone trying to connect to the ssh service would simply be attempting to ssh into my Windows machine which does not have ssh enabled
2. As part of our internet plan, our ISP provides internet access via Carrier-grade NAT (a term I learnt this week!). What this means is although devices from the home network can reach the internet, we don't have a public IP address.
3. Even if we did have a public IP address to connect to, I haven't set up port forwarding on my router to send ssh connections to my Kali VM.


Setting up password authentication is easy. I create a file named "config" in my user's .ssh directory, and inside it I enter the following info:

```
Host kali
  PasswordAuthentication yes
```

After local ssh is set up, the first thing I want to do is have a look at how the data is communicated in a ssh connection.

I open up Wireshark and listen on my loopback interface.

Following the TCP dump I see what looks like a header specifying the server SSH version ("SSH-2.0-OpenSSH_8.4p1 Debian-5") followed by the cipher suite exchange sent in the client Hello and the server Hello reply.

![image](https://user-images.githubusercontent.com/44827973/139769907-d81dc074-4aee-43ec-b4f3-1ad36ef662dd.png)

The server Hello is supposed to include the chosen cipher suite, at a glance I would guess it would be "ecdsa-sha2-nistp256". Up to here the data is in plaintext, and once the TLS handshake has been established it looks like all the data is encrypted (all the rest of the TCP dump is in funny characters).

So what happens if I try connect using netcat?

![image](https://user-images.githubusercontent.com/44827973/139771654-12d7dad4-2b15-4c14-84df-9590be7cddd7.png)

I see the same header from before. At this point I realise the project, being beginner level, probably doesn't expect us to completely rewrite the ssh protocol into the python script, and there's surely an ssh module to use instead.


I find a PoC on kite.com (changed variables obviously):

```
import paramiko

host = "test.rebex.net"
port = 22
username = "demo"
password = "password"

command = "ls"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port, username, password)

stdin, stdout, stderr = ssh.exec_command(command)
lines = stdout.readlines()
print(lines)
```
And it works nicely by itself. It's quite nice how python modules are able to abstract away complexity and allow a simple programming interface for keyboard cavemen like myself.

First Version (3_v1.py)

This version accepts two files for usernames and passwords respectively, and conducts the bruteforce againt the target host.

- accepts as arguments: user list, passwords list, hostname, port
- conducts bruteforce, trying each combination of username and password and printing out fail / success


Sources:

https://www.cloudflare.com/learning/ssl/what-happens-in-a-tls-handshake/
