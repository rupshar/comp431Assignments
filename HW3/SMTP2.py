import sys

input_lines = []

sys.setrecursionlimit(8000)

def start():
	read_inputs()
	input_trav(0)

def read_inputs():
	global input_lines
	try:
		input_file = open(sys.argv[1], "r")
	except FileNotFoundError:
		sys.exit(0)
	input_lines = input_file.readlines()
	input_lines.append("")
	return

def input_trav(data_start):
	global input_lines
	global data_is_input
	global mail_from
	global rcpt_to
	for i in range(data_start, len(input_lines)):
		if(input_lines[i][:5] == "From:"):
			if(input_lines[i-1][:3] == "To:"):
				empty_message()
			print(from_cmd(input_lines[i]))
			resp_number(False)
		elif(input_lines[i][:3] == "To:"):
			print(to_cmd(input_lines[i]))
			resp_number(False)
		elif(input_lines[i] == ""):
			if(input_lines[i-1][:3] == "To:"):
				end_empty_message()
			sys.exit(0)
		else:
			i = read_data_lines(i)

def from_cmd(text):
	path_start_loc = text.find("<")
	path_end_loc = text.find(">")
	path_end_loc = path_end_loc + 1
	reverse_path = text[path_start_loc:path_end_loc]
	return "MAIL FROM: " + reverse_path

def to_cmd(text):
	path_start_loc = text.find("<")
	path_end_loc = text.find(">")
	path_end_loc = path_end_loc + 1
	forward_path = text[path_start_loc:path_end_loc]
	return "RCPT TO: " + forward_path

def resp_number(is_data):
	resp = input()
	sys.stderr.write(resp + "\n")
	if(resp[:3] == "500" or resp[:3] == "501"):
		print("QUIT")
		sys.exit(0)
	elif(resp[:3] == "354"):
		if(resp[3:].isspace() or resp[3:] == ""):
			print("QUIT")
			sys.exit(0)
		if(not(resp[3].isspace())):
			print("QUIT")
			sys.exit(0)
		if(not is_data):
			print("QUIT")
			sys.exit(0)
		else:
			return
	elif(resp[:3] == "250"):
		if(resp[3:].isspace() or resp[3:] == ""):
			print("QUIT")
			sys.exit(0)
		if(not(resp[3].isspace())):
			print("QUIT")
			sys.exit(0)
		if(is_data):
			print("QUIT")
			sys.exit(0)
		else:
			return
	else:
		print("QUIT")
		sys.exit(0)

def read_data_lines(data_start):
	print("DATA")
	data_is_input = True
	resp_number(True)
	for i in range(data_start, len(input_lines)):
		if(input_lines[i] == ""):
			print(".")
			resp_number(False)
			print("QUIT")
			sys.exit(0)
		elif(input_lines[i][:5] == "From:"):
			print(".")
			resp_number(False)
			input_trav(i)
		print(input_lines[i][:-1])

def empty_message():
	print("DATA")
	resp_number(True)
	print(".")
	resp_number(False)
	return

def end_empty_message():
	print("DATA")
	resp_number(True)
	print(".")
	resp_number(False)
	print("QUIT")
	sys.exit(0)

start()
