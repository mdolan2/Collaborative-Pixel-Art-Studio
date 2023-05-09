import pygame
import socket
import threading

HEADER = 64
PORT = 5555
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# Connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(ADDR)
except:
    pass

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (160, 160, 160)
BROWN = (102, 51, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255, 0, 255)
PURPLE = (148, 0, 211)
ORANGE = (255, 128, 0)
LIGHT_GREY = (224, 224, 224)
colours_list = []
colours_list.append(BLACK)
colours_list.append(WHITE)
colours_list.append(GREY)
colours_list.append(BROWN)
colours_list.append(RED)
colours_list.append(GREEN)
colours_list.append(BLUE)
colours_list.append(YELLOW)
colours_list.append(PINK)
colours_list.append(PURPLE)
colours_list.append(ORANGE)

 
# WIDTH and HEIGHT of each grid location
WIDTH = HEIGHT = 25
 
# Margin between each cell
MARGIN = 0

# Current colour
current_colour = 1
 
# Create a 2 dimensional array
grid = []
for row in range(20):
    # Add an empty array that will hold each cell in this row
    grid.append([])
    for column in range(20):
        grid[row].append(1)  # Append a cell
# --- Send colour changes made by this client to the server  ---
def send(msg):
    try:
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
        print(f"Sending message {message}")
    except:
        pass

# --- Receive colour changes made by other clients via the server ---
def receive_messages():
    while True:
        try:
            if client:
                message = client.recv(2048).decode(FORMAT)
                if message == DISCONNECT_MESSAGE:
                    break
                else:
                    x = message.split()
                    if len(x) == 3:
                        recv_column = int(x[0])
                        recv_row = int(x[1])
                        recv_colour = int(x[2])
                        grid[recv_row][recv_column] = recv_colour
                        print("Updated grid at ", recv_row, recv_column, " with colour ", recv_colour)
            else:
                break
        except:
            pass

# Create and start a message receiving thread
receive_thread = threading.Thread(target = receive_messages)
receive_thread.daemon = True
receive_thread.start()
 
# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [500, 550]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Create the colour selection bar and colour palette
selection_bar = pygame.Rect(0, 500, 500, 50)
black_box = pygame.Rect(15, 520, 20, 20)
white_box = pygame.Rect(60, 520, 20, 20)
grey_box = pygame.Rect(105, 520, 20, 20)
brown_box = pygame.Rect(150, 520, 20, 20)
red_box = pygame.Rect(195, 520, 20, 20)
green_box = pygame.Rect(240, 520, 20, 20)
blue_box = pygame.Rect(285, 520, 20, 20)
yellow_box = pygame.Rect(330, 520, 20, 20)
pink_box = pygame.Rect(375, 520, 20, 20)
purple_box = pygame.Rect(420, 520, 20, 20)
orange_box = pygame.Rect(465, 520, 20, 20)

# Put all the colour palette boxes in a list
boxes = []
boxes.append(black_box)
boxes.append(white_box)
boxes.append(grey_box)
boxes.append(brown_box)
boxes.append(red_box)
boxes.append(green_box)
boxes.append(blue_box)
boxes.append(yellow_box)
boxes.append(pink_box)
boxes.append(purple_box)
boxes.append(orange_box)
 
# Set title of screen
pygame.display.set_caption("Pixel Art Studio")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            if pos[1] < 500:
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                # Set that location to value of the current colour
                grid[row][column] = current_colour
                print("Click ", pos, "Grid coordinates: ", row, column)
                # --- Broadcast this colour change ----
                send(str(column) + " " + str(row) + " " + str(current_colour))
            else:
                # User has selected one of the colour palettes to change colour
                for idx, box in enumerate(boxes):
                    if box.collidepoint(pos[0],pos[1]):
                        current_colour = idx

 
    # Set the screen background
    screen.fill(BLACK)

    # Set the selection bar and colour palette circles
    pygame.draw.rect(screen, LIGHT_GREY, selection_bar)
    pygame.draw.rect(screen, BLACK, boxes[0])
    pygame.draw.rect(screen, WHITE, boxes[1])
    pygame.draw.rect(screen, GREY, boxes[2])
    pygame.draw.rect(screen, BROWN, boxes[3])
    pygame.draw.rect(screen, RED, boxes[4])
    pygame.draw.rect(screen, GREEN, boxes[5])
    pygame.draw.rect(screen, BLUE, boxes[6])
    pygame.draw.rect(screen, YELLOW, boxes[7])
    pygame.draw.rect(screen, PINK, boxes[8])
    pygame.draw.rect(screen, PURPLE, boxes[9])
    pygame.draw.rect(screen, ORANGE, boxes[10])
 
    # Draw the grid
    for row in range(20):
        for column in range(20):
            colour = WHITE
            block_colour = grid[row][column]
            if block_colour != 1:
                colour = colours_list[block_colour]
            pygame.draw.rect(screen,
                             colour,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
 
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Update the screen with what has been drawn.
    pygame.display.flip()

send(DISCONNECT_MESSAGE)
client.close()
print("Client connection closed successfully")
pygame.quit()
print("Pygame closed successfully")
