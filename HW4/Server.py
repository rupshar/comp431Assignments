import sys

from socket import *

server_port = int(sys.argv[1])
server_socket = socket(AF_INET, SOCK_STREAM)

connection_socket = ""

is_mail = False
is_rcpt = False
is_data = False
test_statement = ""

senders = []
receivers = []
inputs = []
domains = {}

line = ''

def start():
	start_connection()

def start_connection():
	global connection_socket
	server_socket.bind(('', server_port))
	server_socket.listen(1)
	while True:
		connection_socket, address = server_socket.accept()
		accepted_message = "220 comp431fa20.cs.unc.edu"
		connection_socket.send(accepted_message.encode())
		helo_cmd()
		read_statement()

def helo_cmd():
	global connection_socket
	client_greeting = connection_socket.recv(1024)
	client_greeting = client_greeting.decode()
	if(client_greeting[:4] != "HELO"):
		reply = "500 Syntax error: command not recognized"
		connection_socket.send(reply.encode())
	else:
		is_whitespace = helo_whitespace(client_greeting[4:])
		if(is_whitespace[:3] == "250"):
			reply = "250 Hello " + client_greeting[5:] + ", pleased to meet you"
			connection_socket.send(reply.encode())
		else:
			reply = "501 Syntax error in parameters or arguments"
			connection_socket.send(reply.encode())
	return

def helo_whitespace(text):
	i = 0
	if(text[i] == " " or text[i] == "\t"):
		i = i + 1
	elif(not(text[i].isspace())):
		return helo_domain(text[i:])

	return helo_whitespace(text[i:])

def helo_domain(text):
	if(text[0] == ">"):
		return "501 Syntax error in parameters or arguments"

	if("." not in text):
		return helo_domain_two(text)

	if(text[0] == "." or text[0] == " " or text.count(">") > 1):
		return "501 Syntax error in parameters or arguments"

	if(text[0] == "0" or text[0] == "1" or text[0] == "2" or text[0] == "3" or text[0] == "4" or text[0] == "5" or text[0] == "6" or text[0] == "7" or text[0] == "8" or text[0] == "9"):
		return "501 Syntax error in parameters or arguments"

	dot_loc = text.find(".")
	loc = text[:dot_loc]

	if(not loc.isalnum()):
		return "501 Syntax error in parameters or arguments"

	new_loc = dot_loc + 1
	new_text = text[new_loc:]
	return helo_domain_two(text)

def helo_domain_two(text):
	if(text[0] == "." or text[0] == ">"):
		return "501 Syntax error in parameters or arguments"
	if(text[0] == "0" or text[0] == "1" or text[0] == "2" or text[0] == "3" or text[0] == "4" or text[0] == "5" or text[0] == "6" or text[0] == "7" or text[0] == "8" or text[0] == "9"):
		return "501 Syntax error in parameters or arguments"

	if(text.count(".") > 0):
		dot_loc = text.find(".")
		loc = text[:dot_loc]

		if(not loc.isalnum()):
			return "501 Syntax error in parameters or arguments"

		new_loc = dot_loc + 1
		new_text = text[new_loc:]
		return helo_domain_two(new_text)

	else:
		if(text.count(">") > 0):
			return "501 Syntax error in parameters or arguments"

		end_loc = text.find("\n")
		loc = text[:end_loc]

		if(" " in loc or "\t" in loc):
			return "501 Syntax error in parameters or arguments"

		if(not loc.isalnum()):
			return "501 Syntax error in parameters or arguments"

		return "250 OK"

def mail_from_cmd(text):
	if(text[:4] != "MAIL"):
		return "500 Syntax error: command unrecognized"
	else:
		return space(text[4:])

def space(text):
	if(text[0] == " " or text[0] == "\t"):
		return whitespace(text[1:])
	else:
		return "500 Syntax error: command unrecognized"

def whitespace(text):
	i = 0
	if(text[i] == " " or text[i] == "\t"):
		i = i + 1
	elif(text[i] == "F"):
		return mail_from_cmd_two(text[i:])
	else:
		return "500 Syntax error: command unrecognized"

	return whitespace(text[i:])

def mail_from_cmd_two(text):
	global is_mail
	global senders
	email_start_loc = text.find("<")
	mail_from_text = text[:email_start_loc]
	if(mail_from_text.count(":") > 1):
		return "500 Syntax error: command unrecognized"

	j = 0
	if(text[j:j+5] != "FROM:"):
		return "500 Syntax error: command unrecognized"
	else:
		if(len(senders) == 1):
			return "503 Bad sequence of commands"
		j = j + 5
		is_mail = True
		return nullspace(text[j:])

def nullspace(text):
	k = 0
	if(text[k] != "<" and text[k] != " " and text[k] != "\t"):
		return "501 Syntax error in parameters or arguments"

	if(text[k] == "<"):
		k = k + 1
		if(text[k] == " "):
			return "501 Syntax error in parameters or arguments"

		return mailbox(text[k:])

	if(text[k] == " " or text[k] == "\t"):
		k = k + 1
	else:
		return "501 Syntax error in parameters or arguments"

	return nullspace(text[k:])

def mailbox(text):
	if(text[0] == " " or text[0] == "\t"):
		return "501 Syntax error in parameters or arguments"

	if("@" not in text):
		return "501 Syntax error in parameters or arguments"
	else:
		return local_part(text)

def local_part(text):
	i = 0

	if(text[0] == "@"):
		return "501 Syntax error in parameters or arguments"

	at_loc = text.find("@")
	loc = text[:at_loc]

	if(loc[-1] == " "):
		return "501 Syntax error in parameters or arguments"

	if("\t" in loc or "<" in loc or ">" in loc or "(" in loc or ")" in loc or "[" in loc or "]" in loc or "\\" in loc or "." in loc or "," in loc or ";" in loc or ":" in loc or "@" in loc or "\"" in loc or " " in loc):
		return "501 Syntax error in parameters or arguments"

	new_loc = at_loc + 1
	new_text = text[new_loc:]

	return domain(new_text)

def domain(text):
	if(text[0] == ">"):
		return "501 Syntax error in parameters or arguments"

	if("." not in text):
		return domain_two(text)

	if(text[0] == "."):
		return "501 Syntax error in parameters or arguments"

	if(text[0] == " "):
		return "501 Syntax error in parameters or arguments"

	if(text.count(">") > 1):
		return "501 Syntax error in parameters or arguments"

	if(text[0] == "0" or text[0] == "1" or text[0] == "2" or text[0] == "3" or text[0] == "4" or text[0] == "5" or text[0] == "6" or text[0] == "7" or text[0] == "8" or text[0] == "9"):
		return "501 Syntax error in parameters or arguments"

	dot_loc = text.find(".")
	loc = text[:dot_loc]

	if(not loc.isalnum()):
		return "501 Syntax error in parameters or arguments"

	new_loc = dot_loc + 1
	new_text = text[new_loc:]
	return domain_two(new_text)

def domain_two(text):
	if(text[0] == "."):
		return "501 Syntax error in parameters or arguments"

	if(text[0] == ">"):
		return "501 Syntax error in parameters or arguments"

	if(text[0] == "0" or text[0] == "1" or text[0] == "2" or text[0] == "3" or text[0] == "4" or text[0] == "5" or text[0] == "6" or text[0] == "7" or text[0] == "8" or text[0] == "9"):
                return "501 Syntax error in parameters or arguments"

	if(text.count(".") > 0):
		dot_loc = text.find(".")
		loc = text[:dot_loc]

		if(not loc.isalnum()):
                	return "501 Syntax error in parameters or arguments"

		new_loc = dot_loc + 1
		new_text = text[new_loc:]
		return domain_two(new_text)

	else:
		if(">" not in text):
			return "501 Syntax error in parameters or arguments"

		if(text.count(">") > 1):
			return "501 Syntax error in parameters or arguments"

		end_loc = text.find(">")
		loc = text[:end_loc]

		if(loc[-1] == " "):
			return "501 Syntax error in parameters or arguments"

		if(not loc.isalnum()):
                	return "501 Syntax error in parameters or arguments"

		end_loc = end_loc+1
		new_text = text[end_loc:]
		return ending(new_text)

def ending(text):
	global is_rcpt
	global test_statement
	global senders
	global receivers

	global domains

	if(text[0] != " " and text[0] != "\t" and text[0] != "\n"):
		return "501 Syntax error in parameters or arguments"

	if(not text.isspace()):
		return "501 Syntax error in parameters or arguments"

	else:
		if(is_mail and not is_rcpt):
			path_start_loc = test_statement.find("<")
			path_end_loc = test_statement.find(">")
			path_end_loc = path_end_loc + 1
			senders.append(test_statement[path_start_loc:path_end_loc])
		elif(is_rcpt and is_mail):
			path_start_loc = test_statement.find("<")
			path_end_loc = test_statement.find(">")
			path_end_loc = path_end_loc + 1
			if(test_statement[0] == "M" and len(senders) == 0):
				senders.append(test_statement[path_start_loc:path_end_loc])
				return "250 OK"
			if(test_statement[0] == "R" and len(senders) == 0):
				return "503 Bad sequence of commands"
			path_start_loc = test_statement.find("<")
			path_end_loc = test_statement.find(">")
			path_end_loc = path_end_loc + 1
			domain_start_loc = test_statement.find("@")
			domain_end_loc = test_statement.find(">")
			domain_start_loc += 1
			receivers.append(test_statement[path_start_loc:path_end_loc])
			if(test_statement[domain_start_loc:domain_end_loc] not in domains):
				domains[test_statement[domain_start_loc:domain_end_loc]] = 1
			else:
				domains[test_statement[domain_start_loc:domain_end_loc]] += 1

		return "250 OK"
		start()

def read_statement():
	global connection_socket
	global test_statement
	test_statement = connection_socket.recv(1024).decode()
	if(test_statement[0] == "M"):
		reply = mail_from_cmd(test_statement)
		connection_socket.send(reply.encode())
	elif(test_statement[0] == "R"):
		reply = rcpt_to_cmd(test_statement)
		connection_socket.send(reply.encode())
	elif(test_statement[0] == "D"):
		reply = data_cmd(test_statement)
		connection_socket.send(reply.encode())
	elif(test_statement[0] == "Q"):
		reply = quit_cmd(test_statement)
		connection_socket.send(reply.encode())
		if(reply[:3] == "221"):
			connection_socket.close()
			return
	else:
		error_string = "500 Syntax error: command unrecognized"
		connection_socket.send(error_string.encode())
	read_statement()

def rcpt_to_cmd(text):
	if(text[:4] != "RCPT"):
		return "500 Syntax error: command unrecognized"
	else:
		return rcpt_space(text[4:])

def rcpt_space(text):
	if(text[0] == " " or text[0] == "\t"):
		return rcpt_whitespace(text[1:])
	else:
		return "500 Syntax error: command unrecognized"

def rcpt_whitespace(text):
	i = 0
	if(text[i] == " " or text[i] == "\t"):
		i = i + 1
	elif(text[i] == "T"):
		return rcpt_to_cmd_two(text[i:])
	else:
		return "500 Syntax error: command unrecognized"

	return rcpt_whitespace(text[i:])

def rcpt_to_cmd_two(text):
	global is_rcpt
	global is_mail
	email_start_loc = text.find("<")
	rcpt_to_text = text[:email_start_loc]
	if(rcpt_to_text.count(":") > 1):
		return "500 Syntax error: command unrecognized"

	j = 0
	if(text[j:j+3] != "TO:"):
		return "500 Syntax error: command unrecognized"
	else:
		if(not is_mail or len(senders) == 0):
			return "503 Bad sequence of commands"
		j = j + 3
		is_rcpt = True
		return nullspace(text[j:])

def data_cmd(text):
	global is_data
	global receivers
	global connection_socket
	if(text[:4] != "DATA"):
		return "500 Syntax error: command unrecognized"
	else:
		if(not text[4:].isspace()):
			return "500 Syntax error: command unrecognized"
		if(is_rcpt and len(receivers) == 0):
			return "503 Bad sequence of commands"
		is_data = True
		if(is_data and not is_rcpt):
			return "503 Bad sequence of commands"
		reply = "354 Start mail input; end with <CRLF>.<CRLF>"
		connection_socket.send(reply.encode())
		return data_input()

def quit_cmd(text):
	if(text[:4] != "QUIT"):
		return "500 Syntax error: command unrecognized"
	else:
		if(not text[4:].isspace()):
			return "500 Syntax error: command unrecognized"
		return "221 comp431fa20.cs.unc.edu closing connection"

def data_input():
	global is_mail
	global is_rcpt
	global is_data

	global senders
	global receivers
	global inputs

	global domains

	global line

	global connection_socket

	line = ''

	while not line.endswith("\n.\n"):
		data = connection_socket.recv(2048).decode()
		line += data
		if(line.endswith("\n.\n")):
			is_mail = False
			is_rcpt = False
			is_data = False
			create_files()
			senders.clear()
			receivers.clear()
			domains.clear()
			inputs.clear()
			return "250 OK"
		else:
			inputs.append(line)

def create_files():
	global senders
	global receivers
	global inputs

	global domains

	global line

	for key in domains.keys():
		filename = key
		new_file = open("./forward/" + filename, "a+")
		if(line.endswith("\n\n.\n")):
			line = line.replace("\n.\n", "\n\n")
			new_file.write(line)
		else:
			new_file.write(line[:-2])
		new_file.close()

start()
