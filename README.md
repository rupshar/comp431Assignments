# comp431Assignments
These are the four assignments done for COMP 431. It encapsulates building a mail client/server from scratch.

# HW1
This assignment was the first part of the server, where I created a parser that identifies proper "MAIL FROM" SMTP commands. This is an older version, with the more complete version being in HW2.

# HW2
This assignment was an expansion of the parser created in HW1, where I added more functionalities to my parser, including correctly identifying "RCPT TO" and "DATA"
SMTP commands, generating proper response codes for each response, and identifying the point when a message was done being sent with the <CRLF>.<CRLF> sequence. This project also builds a forward file for each recipient and puts all the information about an email into this forward file.
  
# HW3
This assignment started to build the client. This client reads from a forward file, converts all of the english text into proper SMTP commands as such:

- From: <name@email.com> will become MAIL FROM: <name@email.com>

Then, this client waits for the user to input a response code, and terminates the program if an error code or an unrecognized code is received. 

# HW4
This assignment hooks my client and server together. By using Python's socket library, I made my client read in four inputs: a sender, one or more recipients, a 
subject, and a message of zero or more lines. The client checks the input emails, makes sure that the inputs follow the proper rules, and converts these inputs into 
proper SMTP commands, before sending them to the server, which remains running until the user forces the server to shut down with the ^C input.
