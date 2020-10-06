import sys

is_mail = False
is_rcpt = False
is_data = False
test_statement = ""

senders = []
receivers = []
inputs = []

def start():
	read_statement()

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
			receivers.append(test_statement[path_start_loc:path_end_loc])
		return "250 OK"
		start()

def read_statement():
	global test_statement
	test_statement = sys.stdin.readline()
	if(test_statement == ""):
		sys.exit(0)
	print(test_statement[:-1])
	if(test_statement[0] == "M"):
		print(mail_from_cmd(test_statement))
	elif(test_statement[0] == "R"):
		print(rcpt_to_cmd(test_statement))
	elif(test_statement[0] == "D"):
		print(data_cmd(test_statement))
	else:
		print("500 Syntax error: command unrecognized")
		start()
	start()

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
		print("354 Start mail input; end with <CRLF>.<CRLF>")
		return data_input()

def data_input():
	global is_mail
	global is_rcpt
	global is_data

	global senders
	global receivers
	global inputs

	data = sys.stdin.readline()
	print(data[:-1])
	if(data == ".\n"):
		is_mail = False
		is_rcpt = False
		is_data = False
		create_files()
		senders.clear()
		receivers.clear()
		inputs.clear()
		return "250 OK"
	else:
		inputs.append(data)
		return data_input()

def create_files():
	global senders
	global receivers
	global inputs

	for i in range(len(receivers)):
		filename = receivers[i]
		filename = filename[1:-1]
		new_file = open("./forward/" + filename, "a+")
		new_file.write("From: " + senders[0] + "\n")
		for j in range(len(receivers)):
			new_file.write("To: " + receivers[j] + "\n")
		for k in range(len(inputs)):
			new_file.write(inputs[k])
		new_file.close()

start()
