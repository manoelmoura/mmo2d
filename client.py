import socket
import pygame
import pickle
import random

# Configurações de rede
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 65432        # Porta do servidor

# Inicializa o Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("MMO-2D")

# Cores e FPS
if random.randint(1,4) == 1:
    color = (255, 0, 0)
elif random.randint(1,4) == 2:
    color = (0, 225, 0)
elif random.randint(1,4) == 3:
    color = (0, 0, 255)
elif random.randint(1,4) == 4:
    color = (0, 255, 255)

WHITE = (0, 0, 0)
FPS = 60

# Posição inicial do círculo
radius = 15
speed = 10

# player
class Player:
    def __init__(self, pos, size, speed, color):
        self.pos = pos
        self.size = size
        self.speed = speed
        self.color = color

    def move(self, keys):
        if keys[pygame.K_w]:
            self.pos[1] -= self.speed
        if keys[pygame.K_s]:
            self.pos[1] += self.speed
        if keys[pygame.K_a]:
            self.pos[0] -= self.speed
        if keys[pygame.K_d]:
            self.pos[0] += self.speed

player = Player([400,300], 20, 10, (0, 255, 0))
        

# Conecta ao servidor
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Função principal do cliente
def main():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        keys = pygame.key.get_pressed()
        player.move(keys)
        # Envia a posição atual para o servidor
        client_socket.sendall(pickle.dumps(player))

        # Recebe as posições de todos os jogadores conectados
        data = client_socket.recv(1024)
        all_clients_data = pickle.loads(data)

        # Desenha os círculos de cada jogador
        screen.fill(WHITE)
        for client_obj in all_clients_data.values():
            pygame.draw.circle(screen, client_obj.color, client_obj.pos, client_obj.radius)

        pygame.display.flip()
        clock.tick(FPS)

# Executa o cliente
try:
    main()
finally:
    client_socket.close()
    pygame.quit()

