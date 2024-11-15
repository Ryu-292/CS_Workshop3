import pygame
import random
from character import Character
from datetime import datetime
import csv
from button import Button
from result import read_player_data, display_leaderboard
from plot import generate_and_save_plot

def game(screen, background, background1, gameover, player_name, start_time):

    

    def countdown(screen, font, countdown_from=3):
        font = pygame.font.Font('pixel_font.ttf', 100)
        for i in range(countdown_from, 0, -1):
            screen.blit(background1, (0, 0))
            countdown_text = font.render(str(i), True, (255, 255, 255))
            screen.blit(countdown_text, (screen.get_width() // 2 - countdown_text.get_width() // 2, screen.get_height() // 2 - countdown_text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(1000)

    clock = pygame.time.Clock()
    
    # Load and set up the hammer image, sounds, and scoring variables
    hammer_img = pygame.image.load('hammer.png')
    hammer_img = pygame.transform.scale(hammer_img, (150, 230))
    hammer_angle = 0

    crush_sound = pygame.mixer.Sound('crush_sound.wav')
    scream = pygame.mixer.Sound('scream.wav')
   

    score = 0
    feedback = ""
    lives = 3

    font = pygame.font.Font('pixel_font.ttf', 26)

    leaderboard_button = Button(300, 340, 200, 50, "Leaderboard", font, (0, 0, 255), (0, 0, 150))
    restart2_button = Button(50, 340, 200, 50, "Restart", font, (255, 255, 0), (200, 200, 0))
    quit2_button = Button(550, 340, 200, 50, "Quit", font, (255, 0, 0), (200, 0, 0))
   

    # Pause button setup    
    pause_button = Button(700, 10, 80, 40, "Pause", font, (255, 105, 180), (255, 20, 147))

    # Pause menu buttons
    resume_button = Button(300, 200, 200, 50, "Resume", font, (0, 255, 0), (0, 150, 0), (0, 0, 0))
    restart_button = Button(300, 270, 200, 50, "Restart", font, (255, 255, 0), (200, 200, 0), (0, 0, 0))
    quit_button = Button(300, 340, 200, 50, "Quit", font, (255, 0, 0), (200, 0, 0), (0, 0, 0))
    

    # Display hammer above Opanchu's head
    hammer_x = 30
    hammer_y = 200

    # Opanchu management variables
    opanchus = []  # Keep track of all active Opanchus
    next_spawn_time = 0  # Time to spawn the next Opanchu

    # Game loop
    running = True
    game_over = False
    csv_written = False
    paused = False
    scream_played = False

    level_rythm = 50
    current_level = 1

    countdown(screen, font)

    while running:
        current_time = pygame.time.get_ticks()


        # If game is paused, display the pause menu
        if paused:
            screen.fill((0, 0, 0))
            resume_button.draw(screen)
            restart_button.draw(screen)
            quit_button.draw(screen)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if resume_button.is_clicked(event):
                    paused = False
                if restart_button.is_clicked(event):
                    return True  # Indicate that the game should restart
                if quit_button.is_clicked(event):
                    game_over=True
                    paused = False
            continue

        # Update game screen and logic when not paused
        screen.blit(background1, (0, 0))

        # Draw the pause button
        pause_button.draw(screen)

        if current_time >= next_spawn_time:
            # Spawn a new Opanchu and add it to the list
            start_x = random.randint(800, 850)
            new_opanchu = Character(start_x)
            opanchus.append(new_opanchu)
            next_spawn_time = current_time + random.randint(500, 2000)

        if lives > 0:
            
            for opanchu in opanchus:
                opanchu.update(screen)
                if not opanchu.flattened and opanchu.x < -100:
                    feedback = "Byee~~~"
                    lives -= 1
                    opanchus.remove(opanchu)

                if lives == 0:
                    game_over = True

        if game_over:
            screen.blit(background, (0, 0))
            game_over_font = pygame.font.Font('pixel_font.ttf', 72)
            game_over_text = game_over_font.render("GAME OVER!", True, (255, 0, 0))
            screen.blit(game_over_text, (250, 50))
            screen.blit(gameover, (250, 100))
            if not scream_played:
                scream.play()
                scream_played = True
            restart2_button.draw(screen)
            quit2_button.draw(screen)
            leaderboard_button.draw(screen)            
            pygame.display.update()

            # Record end time, calculate duration, and update CSV with final score if not already done
            if not csv_written:
                end_time = datetime.now()
                duration = end_time - start_time
                with open('players.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([player_name, start_time, end_time, duration, score])
                csv_written = True

                # # Read player data and display the leaderboard
                # players = read_player_data('players.csv')
                # display_leaderboard(screen, players)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if restart2_button.is_clicked(event):
                    return True  # Restart the game
                if leaderboard_button.is_clicked(event):
                    players = read_player_data('players.csv')
                    generate_and_save_plot(players)
                    display_leaderboard(screen, players)
                if quit2_button.is_clicked(event):
                    running = False
                    

            continue

        # Event handling and game updates
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not game_over:
                if pause_button.is_clicked(event):
                    paused = True

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    hammer_angle = 60
                    hit_successful = False

                    for opanchu in opanchus:
                        if not opanchu.flattened and 105 <= opanchu.x <= 180:
                            opanchu.flatten()
                            feedback = "Nice!"
                            score += 5
                            crush_sound.play()
                            hit_successful = True
                            break

                    if not hit_successful:
                        feedback = "Are You F*cking Blind?"
                        score -= 2

                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    hammer_angle = 0

        # Draw hammer
        hammer_rotated = pygame.transform.rotate(hammer_img, -hammer_angle)
        hammer_rect = hammer_rotated.get_rect(center=(hammer_x + hammer_img.get_width() // 2, hammer_y + hammer_img.get_height() // 2))
        screen.blit(hammer_rotated, hammer_rect.topleft)

        # Display score and feedback
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        life_text = font.render(f"Lives: {lives}", True, (0, 0, 0))
        feedback_text = font.render(feedback, True, (0, 255, 0) if feedback == "Nice!" else (255, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(life_text, (10, 50))
        screen.blit(feedback_text, (250, 50))

        # Update display and control game speed
        pygame.display.update()
        clock.tick(level_rythm)

        # Update level speed logic
        if score >= 50 and current_level == 1:
            target_rythm = level_rythm + 40  # Set target value for gradual increase
            while level_rythm < target_rythm:
                level_rythm += 5  # Increment gradually
            current_level += 1
        elif score >= 100 and current_level == 2:
            target_rythm = level_rythm + 40  # Set target value for gradual increase
            while level_rythm < target_rythm:
                level_rythm += 5  # Increment gradually
            
            current_level += 1
        elif score >= 150 and current_level == 3:
            target_rythm = level_rythm + 50  # Set target value for gradual increase
            while level_rythm < target_rythm:
                level_rythm += 5  # Increment gradually
           
            current_level += 1
        elif score >= 200 and current_level == 4:
            target_rythm = level_rythm + 50
            while level_rythm < target_rythm:
                level_rythm += 5
            
            current_level += 1
        elif score >= 250 and current_level == 5:
            target_rythm = level_rythm + 50
            while level_rythm < target_rythm:
                level_rythm += 5
            
            current_level += 1


    pygame.quit()

