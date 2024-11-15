import pygame
import csv
from button import Button
from datetime import datetime 

def menu(screen):
    input_box = pygame.Rect(200, 250, 400, 50)
    font = pygame.font.Font('pixel_font.ttf', 35)
    player_name = ""

    # Create the Start button
    start_button = Button(275, 350, 250, 50, "Start Game", font, (255, 105, 180), (255, 20, 147))

    menu_running = True
    while menu_running:
        screen.fill((255, 255, 255))
        
        # Draw UI elements
        title_text = font.render("Enter Player Name:", True, (0, 0, 0))
        screen.blit(title_text, (200, 200))

        pygame.draw.rect(screen, (0, 0, 0), input_box, 2)
        text_surface = font.render(player_name, True, (0, 0, 0))
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))

        # Draw the Start button
        start_button.draw(screen)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and player_name:
                    start_time = datetime.now()  # Record the start time
                    return player_name, start_time  # Exit menu and start the game
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

                           
            # Check if the Start button is clicked
            # if start_button.is_clicked(event) and player_name:
            #     start_time = datetime.now()  # Record the start time
            #     with open('players.csv', 'a', newline='') as file:
            #         writer = csv.writer(file)
            #         writer.writerow([player_name, start_time, "In Progress", 0])  # Initial CSV entry
            #     return player_name, start_time  # Exit menu and start the game
            
            if start_button.is_clicked(event) and player_name:
                 start_time = datetime.now()  # Record the start time
                 return player_name, start_time  # Exit menu and start the game
