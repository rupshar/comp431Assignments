import sys
import time

from socket import *

server_name = sys.argv[1]
server_port = int(sys.argv[2])

senders = []
receivers = []
subject = []
message = []

smtp_senders = []
smtp_receivers = []

client_socket = socket(AF_INET, SOCK_STREAM)

def start():
	enter_data()
	generate_smtp_lines()
	start_connection()
	initialize_contact()
	read_inputs()

def start_connection():
	try:
		client_socket.connect((server_name, server_port))
	except ConnectionRefusedError:
		print("ERROR -- connection refused")
		sys.exit(0)
	start_message = client_socket.recv(1024)
	return

def initialize_contact():
	greeting = "HELO comp431fa20b.cs.unc.edu"
	client_socket.send(greeting.encode())

	reply = client_socket.recv(1024)
	return

def read_inputs():
	reply = ''
	global senders
	global receivers
	global subject
	global message

	global smtp_senders
	global smtp_receivers

	while(reply[:3] != "221"):
		mail_from_cmd = smtp_senders[0]
		client_socket.send(mail_from_cmd.encode())

		reply = client_socket.recv(1024).decode()
		if(reply[:3] == "500" or reply[:3] == "501" or reply[:3] == "503"):
			sys.exit(0)

		for rcpt_to_cmd in smtp_receivers:
			client_socket.send(rcpt_to_cmd.encode())

			reply = client_socket.recv(1024).decode()
			if(reply[:3] == "500" or reply[:3] == "501" or reply[:3] == "503"):
				sys.exit(0)

		data_cmd = "DATA\n"
		client_socket.send(data_cmd.encode())

		reply = client_socket.recv(1024).decode()
		if(reply[:3] == "500" or reply[:3] == "501" or reply[:3] == "503"):
				sys.exit(0)

		from_line = "From: <" + senders[0] + ">\n"
		client_socket.send(from_line.encode())

		to_line = "To: "
		if(len(receivers) > 1):
			for i in range(len(receivers) - 1):
				to_line += "<" + receivers[i] + ">, "
			to_line += "<" + receivers[-1] + ">\n"
			client_socket.send(to_line.encode())
		else:
			to_line += "<" + receivers[0] + ">\n"
			client_socket.send(to_line.encode())

		subject_line = "Subject: " + subject[0] + "\n"
		client_socket.send(subject_line.encode())

		blank_line = "\n"
		client_socket.send(blank_line.encode())

		if(len(message) > 1 or (len(message) == 1 and message[0] != ".")):
			for msg in message:
				msg += "\n"
				client_socket.send(msg.encode())

			end_msg = ".\n"
			client_socket.send(end_msg.encode())

		else:
			end_msg = "\n.\n"
			client_socket.send(end_msg.encode())

		data_reply = client_socket.recv(1024)
		data_reply = data_reply.decode()

		quit_msg = "QUIT\n"
		client_socket.send(quit_msg.encode())

		quit_reply = client_socket.recv(1024)
		quit_reply = quit_reply.decode()

		if(quit_reply[:3] == "221"):
			sys.exit(0)

def enter_data():
	global senders
	global receivers
	global subject
	global message

	check_from_msg = "Missing Error."
	from_path = input("From:\n")
	while("Error" in check_from_msg):
		check_from_msg = mailbox(from_path)
		if("Error" in check_from_msg):
			print(check_from_msg)
			from_path = input("From:\n")
		elif(check_from_msg == "Sender ok"):
			senders.append(from_path)
			break

	check_to_msg = "Missing Error."
	to_msgs = []
	to_paths = []
	is_all_good = False

	while(not is_all_good):
		to_path = input("To:\n")
		to_msgs = []
		to_paths = []
		if("," in to_path):
			to_path = "".join(to_path.split())
			receivers.clear()
			to_paths = to_path.split(",")
		else:
			to_paths.append(to_path)
		for rcpt in to_paths:
			check_to_msg = mailbox(rcpt)
			to_msgs.append(check_to_msg)
		if(any("Error" in msg for msg in to_msgs)):
			is_all_good = False
			print("There was an error in at least one of your email addresses. Try again.")
		else:
			is_all_good = True
			for rcpt in to_paths:
					receivers.append(rcpt)

	subject_line = input("Subject:\n")
	subject.append(subject_line)

	message_line = input("Message:\n")
	message.append(message_line)

	while(not message_line == "."):
		message_line = input()
		if(message_line == "."):
			break
		message.append(message_line)
	return

def generate_smtp_lines():
	global senders
	global receivers

	global smtp_senders
	global smtp_receivers

	mail_from_txt = "MAIL FROM: <" + senders[0] + ">\n"
	smtp_senders.append(mail_from_txt)

	for rcpt in receivers:
		rcpt_to_txt = "RCPT TO: <" + rcpt + ">\n"
		smtp_receivers.append(rcpt_to_txt)

	return

def mailbox(text):
	if(text[0] == " " or text[0] == "\t"):
		return "Path Error. Make sure you don't start your email with a space!"

	if("@" not in text):
		return "Mailbox Error. You need to have an '@' character to separate your name and domain!"
	else:
		return local_part(text)

def local_part(text):
	i = 0

	if(text[0] == "@"):
		return "Local Part Error. Make sure your email address has a name"

	at_loc = text.find("@")
	loc = text[:at_loc]

	if(loc[-1] == " "):
		return "Mailbox Error. Don't end your name with a space!"

	if("\t" in loc or "<" in loc or ">" in loc or "(" in loc or ")" in loc or "[" in loc or "]" in loc or "\\" in loc or "." in loc or "," in loc or ";" in loc or ":" in loc or "@" in loc or "\"" in loc or " " in loc):
		return "Local Part Error. Don't add any special characters or spaces to your name!"

	new_loc = at_loc + 1
	new_text = text[new_loc:]

	return domain(new_text)

def domain(text):
	if(text == ""):
		return "Domain Error. Make sure you have a domain!"
	if("." not in text):
		return domain_two(text)

	if(text[0] == "."):
		return "Domain Error. Don't begin your domain with a period!"

	if(text[0] == " "):
		return "Mailbox Error. Don't start your domain with a space!"

	if(text[0] == "0" or text[0] == "1" or text[0] == "2" or text[0] == "3" or text[0] == "4" or text[0] == "5" or text[0] == "6" or text[0] == "7" or text[0] == "8" or text[0] == "9"):
		return "Domain Error. You cannot begin any part of the domain with a number!"

	dot_loc = text.find(".")
	loc = text[:dot_loc]

	if(not loc.isalnum()):
		return "Domain Error. Your domain can only consist of letters or numbers."

	new_loc = dot_loc + 1
	new_text = text[new_loc:]
	return domain_two(new_text)

def domain_two(text):
	if(text == ""):
		return "Domain Error. Don't end your domain with any symbol!"
	if(text[0] == "."):
		return "Domain Error. You cannot have two consecutive periods in your domain."

	if(text[0] == "0" or text[0] == "1" or text[0] == "2" or text[0] == "3" or text[0] == "4" or text[0] == "5" or text[0] == "6" or text[0] == "7" or text[0] == "8" or text[0] == "9"):
		return "Domain Error. You cannot begin any part of the domain with a number!"

	if(text.count(".") > 0):
		dot_loc = text.find(".")
		loc = text[:dot_loc]

		if(not loc.isalnum()):
			return "Domain Error. Your domain can only consist of letters or numbers."

		new_loc = dot_loc + 1
		new_text = text[new_loc:]
		return domain_two(new_text)

	else:
		if(text[-1] == " "):
			return "Path Error. Don't end your email address with a space!"

		if(not text.isalnum()):
			return "Domain Error. Your domain can only consist of letters or numbers."

		return "Sender ok"

start()
