import pygame
from button import Button
import csv

def read_player_data(csv_file):
    players = []

    # Read CSV file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            player_name = row[0]
            try:
                score = int(row[4])
            except (IndexError, ValueError):
                score = -1  # Assuming the score is in the 5th column (index 4)

            players.append((player_name, score))

    # Sort players by score in descending order
    players.sort(key=lambda x: x[1], reverse=True)
    return players

def display_leaderboard(screen, players):
    # Set up fonts and colors
    font = pygame.font.Font('pixel_font.ttf', 48)
    small_font = pygame.font.Font('pixel_font.ttf', 36)
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)

    # Fill screen with background color
    screen.fill(background_color)

    # Title
    title_text = font.render("Leaderboard", True, text_color)
    screen.blit(title_text, (200, 20))

    # Display player names and scores
    y_offset = 100
    for index, (player_name, score) in enumerate(players[:10]):  # Show top 10 players
        # Display "N" instead of -1 for missing scores
        display_score = score if score != -1 else "N"
        leaderboard_text = f"{index + 1}. {player_name}: {display_score}"
        text_surface = small_font.render(leaderboard_text, True, text_color)
        screen.blit(text_surface, (100, y_offset))
        y_offset += 40  # Move down for the next player

    # Add a button to go back to the main menu or quit
    back_button = Button(250, 500, 200, 50, "Back", font, (0, 255, 0), (0, 150, 0))
    back_button.draw(screen)

    pygame.display.update()

    # Leaderboard loop to keep the screen displayed until user action
    leaderboard_open = True
    while leaderboard_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                leaderboard_open = False
                pygame.quit()
                exit()  # Ensure the entire program quits
            if back_button.is_clicked(event):
                leaderboard_open = False  # Exit the leaderboard and go back to the main game



    pygame.display.update()