import pygame
import sys
import math

pygame.init()


# Initital Constants

# Screen settings
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Triangle properties
triangle_color = ("white")
triangle_size = 10
triangle_position = [width // 2, height // 2]       # Sentrere spilleren
triangle_angle = 0



# Movement settings
speed_up_down = 0
speed_left_right = 0
rotation_speed = 5




class Player():
    pass


class Bullet():
    pass

class Asteroid():
    pass



def gameloop():
    pass






# Main game loop
running = True
while running:
    
    # Create triangle points and  (format: høyde, bredde)
    point1 = (0, -triangle_size)
    point2 = (-triangle_size, triangle_size)
    point3 = (triangle_size, triangle_size)
    
    rotated_points = []
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        triangle_angle -= rotation_speed
    if keys[pygame.K_RIGHT]:
        triangle_angle += rotation_speed
   
   
    if keys[pygame.K_w]:
        
        speed_up_down += 0.1
    if keys[pygame.K_s]:
        speed_up_down -= 0.1
    
    if keys[pygame.K_a]:
        
        speed_left_right += 0.1
    if keys[pygame.K_d]:
        speed_left_right -= 0.1

    triangle_position[1] += speed_up_down
    triangle_position[0] -= speed_left_right

    
    # apply rotation
    for point in [point1, point2, point3]:
        # Regner ut hvor mye X og Y forandres på hvert punkt når trianglets vinkel endres
        rotated_x = point[0] * math.cos(math.radians(triangle_angle)) - point[1] * math.sin(math.radians(triangle_angle))    
        rotated_y = point[0] * math.sin(math.radians(triangle_angle)) + point[1] * math.cos(math.radians(triangle_angle)) 
        # Legger sammen rotasjonen og posisjonen
        rotated_points.append((rotated_x + triangle_position[0], rotated_y + triangle_position[1]))

    # triangle_position[0] += 0.0
    # triangle_position[1] += 0.6

    print(rotated_points)
    
    
    # Draw triangle
    screen.fill((0, 0, 0))
    pygame.draw.polygon(screen, triangle_color, rotated_points, width=1)
    pygame.display.flip()
    clock.tick(80)

pygame.quit()
sys.exit()
