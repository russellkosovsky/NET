from socket import *
import ssl
import base64

# Gmail SMTP server details
mailserver = ('smtp.gmail.com', 587)

# Your Gmail credentials (replace with your actual email and password)
email = 'russellkosovsky@gmail.com'
#password = ''

# Create socket and connect
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)

# Receive initial response
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send EHLO command
ehloCommand = 'EHLO Alice\r\n'
clientSocket.send(ehloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send STARTTLS command
starttlsCommand = 'STARTTLS\r\n'
clientSocket.send(starttlsCommand.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)
if recv2[:3] != '220':
    print('220 reply not received after STARTTLS')

# Wrap the socket in SSL using ssl.create_default_context()
context = ssl.create_default_context()
clientSocket = context.wrap_socket(clientSocket, server_hostname=mailserver[0])

# Re-send EHLO after STARTTLS
clientSocket.send(ehloCommand.encode())
recv3 = clientSocket.recv(1024).decode()
print(recv3)
if recv3[:3] != '250':
    print('250 reply not received after EHLO')

# Authenticate using SMTP AUTH
# Encode credentials in base64
authCommand = 'AUTH LOGIN\r\n'
clientSocket.send(authCommand.encode())
recv4 = clientSocket.recv(1024).decode()
print(recv4)
if recv4[:3] != '334':
    print('334 reply not received after AUTH LOGIN')

# Send base64-encoded email
clientSocket.send(base64.b64encode(email.encode()) + b'\r\n')
recv5 = clientSocket.recv(1024).decode()
print(recv5)
if recv5[:3] != '334':
    print('334 reply not received after sending email')

# Send base64-encoded password
clientSocket.send(base64.b64encode(password.encode()) + b'\r\n')
recv6 = clientSocket.recv(1024).decode()
print(recv6)
if recv6[:3] != '235':
    print('235 reply not received after sending password')

# Send MAIL FROM command
mailFromCommand = f'MAIL FROM: <{email}>\r\n'
clientSocket.send(mailFromCommand.encode())
recv7 = clientSocket.recv(1024).decode()
print(recv7)
if recv7[:3] != '250':
    print('250 reply not received after MAIL FROM')

# Send RCPT TO command
rcptToCommand = 'RCPT TO: <rkosovsky@conncoll.edu>\r\n'  # Replace with recipient's email
clientSocket.send(rcptToCommand.encode())
recv8 = clientSocket.recv(1024).decode()
print(recv8)
if recv8[:3] != '250':
    print('250 reply not received after RCPT TO')

# Send DATA command
dataCommand = 'DATA\r\n'
clientSocket.send(dataCommand.encode())
recv9 = clientSocket.recv(1024).decode()
print(recv9)
if recv9[:3] != '354':
    print('354 reply not received after DATA')

# Send email headers and body
headers = f'From: {email}\r\nTo: rkosovsky@conncoll.edu\r\nSubject: Test Email\r\n\r\n'
body = 'This is a test email sent using SMTP.\r\n'
clientSocket.send(headers.encode())
clientSocket.send(body.encode())

# End the email with a single period
endmsg = '\r\n.\r\n'
clientSocket.send(endmsg.encode())
recv10 = clientSocket.recv(1024).decode()
print(recv10)
if recv10[:3] != '250':
    print('250 reply not received after sending message data')

# Send QUIT command
quitCommand = 'QUIT\r\n'
clientSocket.send(quitCommand.encode())
recv11 = clientSocket.recv(1024).decode()
print(recv11)

# Close the socket
clientSocket.close()
