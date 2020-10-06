import sys


def start():
	read_statement()

def mail_from_cmd(text):
	if(text[:4] != "MAIL"):
		print("ERROR -- mail-from-cmd")
		start()
	else:
		space(text[4:])

def space(text):
	if(text[0] == " " or text[0] == "\t"):
		whitespace(text[1:])
	else:
		print("ERROR -- whitespace")
		start()

def whitespace(text):
	i = 0
	if(text[i] == " " or text[i] == "\t"):
		i = i + 1
	elif(text[i] == "F"):
		mail_from_cmd_two(text[i:])
	else:
		print("ERROR -- mail-from-cmd")
		start()

	whitespace(text[i:])

def mail_from_cmd_two(text):
	email_start_loc = text.find("<")
	mail_from_text = text[:email_start_loc]
	if(mail_from_text.count(":") > 1):
		print("ERROR -- mail-from-cmd")
		start()

	j = 0
	if(text[j:j+5] != "FROM:"):
		print("ERROR -- mail-from-cmd")
		start()
	else:
		j = j + 5
		nullspace(text[j:])

def nullspace(text):
	k = 0
	if(text[k] != "<" and text[k] != " " and text[k] != "\t"):
		print("ERROR -- path")
		start()

	if(text[k] == "<"):
		k = k + 1
		if(text[k] == " "):
			print("ERROR -- path")
			start()

		mailbox(text[k:])

	if(text[k] == " " or text[k] == "\t"):
		k = k + 1
	else:
		print("ERROR -- path")
		start()

	nullspace(text[k:])

def mailbox(text):
	if(text[0] == " " or text[0] == "\t"):
		print("ERROR -- path")
		start()

	if("@" not in text):
		print("ERROR -- mailbox")
		start()
	else:
		local_part(text)

def local_part(text):
	i = 0
#	if(text.count("@") > 1):
#		print("ERROR -- domain")
#		start()

	if(text[0] == "@"):
		print("ERROR -- local-part")
		start()

	at_loc = text.find("@")
	loc = text[:at_loc]

	if(loc[-1] == " "):
		print("ERROR -- mailbox")
		start()

	if("\t" in loc or "<" in loc or ">" in loc or "(" in loc or ")" in loc or "[" in loc or "]" in loc or "\\" in loc or "." in loc or "," in loc or ";" in loc or ":" in loc or "@" in loc or "\"" in loc or " " in loc):
		print("ERROR -- local-part")
		start()

	new_loc = at_loc + 1
	new_text = text[new_loc:]

	domain(new_text)

def domain(text):
	if(text[0] == ">"):
		print("ERROR -- domain")
		start()

	if("." not in text):
		domain_two(text)

	if(text[0] == "."):
		print("ERROR -- domain")
		start()

	if(text[0] == " "):
		print("ERROR -- mailbox")
		start()

	if(text.count(">") > 1):
		print("ERROR -- domain")
		start()

	if(text[0] == "0" or text[0] == "1" or text[0] == "2" or text[0] == "3" or text[0] == "4" or text[0] == "5" or text[0] == "6" or text[0] == "7" or text[0] == "8" or text[0] == "9"):
		print("ERROR -- domain")
		start()

	dot_loc = text.find(".")
	loc = text[:dot_loc]

	if(not loc.isalnum()):
		print("ERROR -- domain")
		start()

	new_loc = dot_loc + 1
	new_text = text[new_loc:]
	domain_two(new_text)

def domain_two(text):
	if(text[0] == "."):
		print("ERROR -- domain")
		start()

	if(text[0] == ">"):
		print("ERROR -- domain")
		start()

	if(text[0] == "0" or text[0] == "1" or text[0] == "2" or text[0] == "3" or text[0] == "4" or text[0] == "5" or text[0] == "6" or text[0] == "7" or text[0] == "8" or text[0] == "9"):
                print("ERROR -- domain")
                start()

	if(text.count(".") > 0):
		dot_loc = text.find(".")
		loc = text[:dot_loc]

		if(not loc.isalnum()):
                	print("ERROR -- domain")
                	start()

		new_loc = dot_loc + 1
		new_text = text[new_loc:]
		domain_two(new_text)

	else:
		if(">" not in text):
			print("ERROR -- path")
			start()

		if(text.count(">") > 1):
			print("ERROR -- domain")
			start()

		end_loc = text.find(">")
		loc = text[:end_loc]

		if(loc[-1] == " "):
			print("ERROR -- path")
			start()

		if(not loc.isalnum()):
                	print("ERROR -- domain")
                	start()

		end_loc = end_loc+1
		new_text = text[end_loc:]
		ending(new_text)

def ending(text):
	if(text[0] != " " and text[0] != "\t" and text[0] != "\n"):
		print("ERROR -- path")
		start()

	if(not text.isspace()):
		print("ERROR -- CRLF")
		start()

#	if("\t" not in text and " " not in text and "\n" not in text):
#		print("ERROR -- CRLF")
#		start()

	else:
		print("Sender ok")
		start()

def read_statement():
	test_statement = sys.stdin.readline()
	if(test_statement == ""):
		sys.exit(1)
	print(test_statement[:-1])
	mail_from_cmd(test_statement)


start()
