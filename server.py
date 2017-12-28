import socket
from threading import Thread
from scrape import return_category

# Will be altered for the protocol we decide
def receive(conn):
	return conn.recv(1024).decode('utf-8')

# Will be altered for the protocol we decide
def send(conn, data):
	conn.send(data.encode('utf-8'))	

def shutdown(conn):
	try:
		conn.shutdown(socket.SHUT_RDWR)
		conn.close()
	except OSError:
		pass
	except Exception as e:
		print("Failure closing socket:\n" + str(e))
	exit()
	
def server_loop(ip, max_listen_threads=15):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		server.bind(ip)
	except:
		print("Could not bind to", ip)
		exit()

	server.listen(max_listen_threads)

	def fork_thread(client):
		data = receive(client)
		category = return_category(data)
		send(client, category)
		shutdown(client)
		
	while True:
		client, addr = server.accept()
		print("Received connection from", addr)
		Thread(target=fork_thread, args=(client,)).start()
		

if __name__ == "__main__":
	from argparse import ArgumentParser

	parser = ArgumentParser(description="Starts a server that returns categories for Android applications")
	parser.add_argument("ip", type=str, help="What IPs you want to serve (0.0.0.0 for everything) and what ports, separated by :.")
	parser.add_argument("--max-listeners", type=int, help="How many devices you want to serve at once", choices=range(0,26), default=15)
	args = parser.parse_args()

	ip = None
	try:
		ip = list(args.ip.split(':'))
		ip[1] = int(ip[1])
	except:
		print("Your IP:Port combination is invalid, exiting")
		exit()
		
	server_loop(tuple(ip), args.max_listeners)
