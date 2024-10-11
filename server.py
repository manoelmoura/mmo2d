import socket
import threading
import pickle

# Configuração do servidor
HOST = '127.0.0.1'  # Endereço IP local
PORT = 65432        # Porta do servidor

# Dicionário para armazenar as posições dos clientes
clients_data = {}

# Função para lidar com cada cliente
def handle_client(conn, addr):
    global clients_data
    print(f'Cliente conectado: {addr}')
    
    while True:
        try:
            # Recebe os dados de posição do cliente
            data = conn.recv(1024)
            if not data:
                break

            # Atualiza a posição do cliente
            player = pickle.loads(data)
            clients_data[addr] = player

            # Envia os dados de todos os clientes conectados
            conn.sendall(pickle.dumps(clients_data))
        except:
            break

    print(f'Cliente desconectado: {addr}')
    del clients_data[addr]
    conn.close()

# Configura o socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f'Servidor ouvindo em {HOST}:{PORT}')

# Loop para aceitar conexões de clientes
while True:
    conn, addr = server_socket.accept()
    threading.Thread(target=handle_client, args=(conn, addr)).start()

