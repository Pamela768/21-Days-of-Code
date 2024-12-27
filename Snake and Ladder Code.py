import pygame
from random import randint
from time import sleep 
from sys import exit

def main():
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()
    

    # Create the game window
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Snakes and Ladders")
    menu_image = pygame.image.load(r"menu_2.png").convert()
    click_sound = r"music.mp3" # Replace with your sound file
    
    pygame.mixer.music.load(click_sound)
    pygame.mixer.music.play()
    # Define colors
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    DARK_BLUE = (0, 0, 139)
    LIGHT_BLUE = (173, 216, 230)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    PURPLE= (128, 0, 128)
    
    ladder = {6:27, 19:57, 33:85, 63:85, 72:94 }
    snakes = {30:8, 46:25, 58:37, 74:55, 96:61, 84:65 }
    
    # Define button properties
    button_rects = {
        "Player Alone": pygame.Rect(275, 200, 250, 80),
        "Play with Computer": pygame.Rect(275, 350, 340, 80)
    }
    
    shown_button = True
    # Define font
    font = pygame.font.Font(None, 50)

    
    # Function to draw buttons with hover effect
    def draw_buttons():
        if shown_button:
                screen.blit(menu_image, (0,0))
                mouse_pos = pygame.mouse.get_pos()
                for text, rect in button_rects.items():
                    color = DARK_BLUE if rect.collidepoint(mouse_pos) else BLUE
                    pygame.draw.rect(screen, color, rect, border_radius=10)
                    button_text = font.render(text, True, WHITE)
                    text_rect = button_text.get_rect(center=rect.center)
                    screen.blit(button_text, text_rect)

    clock = pygame.time.Clock()
    game_mode = None  # None, "alone", or "computer"
    
    def flash_message(screen, text, duration):
    # Render the message
        message = font.render(text, True, BLACK)
        text_rect = message.get_rect(center=(250, 250))
        
        # Draw a white rectangle behind the text
        padding = 10  # Add some padding around the text
        background_rect = pygame.Rect(
        text_rect.x - padding,
        text_rect.y - padding,
        text_rect.width + 2 * padding,
        text_rect.height + 2 * padding,
)
        pygame.draw.rect(screen, WHITE, background_rect)  # White rectangle
        screen.blit(message, text_rect)
        
    # Update the display
        pygame.display.flip()
    
    # Wait for the specified duration
        clock.tick(duration)
    
    
    
    # Function to handle button clicks
    def handle_button_click(event):
        if event.type == pygame.MOUSEBUTTONDOWN: 
            for text, rect in button_rects.items():
                if rect.collidepoint(event.pos):
                    if text == "Player Alone":
                        screen.fill(BLACK)
                        screen.blit(image, (20, 20))
                        pygame.draw.circle(screen, GREEN, (500, 500), 10 ) # Player marker
                        screen.blit(dice_image,(650, 300))
                        
                        
                        
                        alone()
                        
                    elif text == "Play with Computer":
                        screen.blit(image, (20,20))
                        screen.blit(dice_image, (650, 300))
                        computer()
    
    image = pygame.image.load("board(1).jpg").convert()  # Replace with your image file
    dice_image= pygame.image.load("dice_3.png").convert()
    #image_rect = dice_image.get_rect() 

    def get_square_coordinates(square_number):
        # Board constants
        SQUARE_SIZE = 60  # Size of one square in pixels
        GRID_SIZE = 10    # Number of squares per row/column

        # Calculate row and column
        
        if square_number == 0:
            x , y = 39, 590
            return x, y
        
        else:
            row = (square_number - 1) // GRID_SIZE
            if row % 2 == 0:  # Even row (left to right)
                column = (square_number - 1) % GRID_SIZE
        
    
            
            else:  # Odd row (right to left)
                column = GRID_SIZE - 1 - ((square_number - 1) % GRID_SIZE)
            
            x = column * SQUARE_SIZE + SQUARE_SIZE // 2
            y = (GRID_SIZE - 1 - row) * SQUARE_SIZE + SQUARE_SIZE // 2
            return x, y
        
    
    
   
    def alone():
        current_position = 0
            
            
        
        global turn 
        turn = None
        running = True
        sound_on = True
        
        dice_button_rect = dice_image.get_rect(topleft=(650, 300))
        back_button_rect = pygame.Rect(0, 0, 40, 30)  # Back button rectangle
        sound_button_rect = pygame.Rect(650, 0, 100, 50)  # x, y, width, height
      

        while running:
            font = pygame.font.Font(None, 20) 
            
           
        
           
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Handle quit event
                    running = False
                    exit()  # Exit the function
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if sound_button_rect.collidepoint(event.pos):
                        sound_on = not sound_on  # Toggle sound state
                        pygame.mixer.music.pause()
                        if sound_on:
                            pygame.mixer.music.unpause()  # Play sound when turn
                    if back_button_rect.collidepoint(event.pos):  # Back button clicked
                        return  # Go back to the main menu
                    if dice_button_rect.collidepoint(event.pos):  # Dice button clicked
                        dice_roll = randint(1, 6)
                        flash_message(screen, f" You rolled a {dice_roll}", 2)


                

                   
                    # Calculate target position
                        
                        target_position = current_position + dice_roll
                        start_coords = get_square_coordinates(current_position)
                        end_coords = get_square_coordinates(target_position)
                        
                        move_icon(start_coords, end_coords)
                            
                        print(f"Dice rolled: {dice_roll}, you are now on {target_position}") 
                        
                        if target_position > 100:  # Assume 100 is the last square
                            continue

                        if target_position in ladder:
                            
                            
                            target_position = ladder[target_position]  # Update position
                        
                            print(f"You have climbed up a ladder, your position is now {current_position}")
                            pygame.time.delay(60)
                            
                        elif target_position in snakes:

                            
                            target_position = snakes[target_position]  # Update position
                            
                        
                            print(f"You slipped down a snake. Your position is now {current_position}")
                            pygame.time.delay(60)
                    
                            
                        
                        current_position = target_position
                        
                        if current_position == 100:
                            running = False
                        
            screen.fill(WHITE)
            screen.blit(image, (20, 20))  # Redraw the board
            screen.blit(dice_image, (650, 300))  # Redraw the dice button
            
            
            pygame.draw.rect(screen, BLACK, back_button_rect, border_radius=5)
            
            back_text = font.render("Back", True, WHITE)
            back_text_rect = back_text.get_rect(center=back_button_rect.center)
            screen.blit(back_text, back_text_rect)
            
            button_color = PURPLE if sound_on else BLACK
            pygame.draw.rect(screen, button_color, sound_button_rect)
            sound_text = font.render("Sound ON" if sound_on else "Sound OFF", True, WHITE)
            sound_text_rect = sound_text.get_rect(center=sound_button_rect.center)
            screen.blit(sound_text, sound_text_rect)
            
          

        # Draw the player's current position
            current_coords = get_square_coordinates(current_position)
            pygame.draw.circle(screen, GREEN, current_coords, 10)  # Player marker
            
            
        
            pygame.display.update()
            clock.tick(60)

    def computer():
        current_player_position = 0
        current_computer_position = 0
        target_position_1 = 0
        target_position_2 = 0
        running = True
        sound_on = True
        global turn
        turn = "player"  # Keeps track of whose turn it is
        dice_button_rect = dice_image.get_rect(topleft=(650, 300))
        back_button_rect = pygame.Rect(0, 0, 40, 30)  # Back button rectangle
        sound_button_rect = pygame.Rect(650, 0, 100, 50)  # x, y, width, height

        while running:
            font = pygame.font.Font(None, 20) 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Handle quit event
                    running = False
                    exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse clicks
                    if back_button_rect.collidepoint(event.pos):  # Back button clicked
                        return  # Go back to the main menu
                    
                    if sound_button_rect.collidepoint(event.pos):
                        sound_on = not sound_on  # Toggle sound state
                        pygame.mixer.music.pause()
                        if sound_on:
                            pygame.mixer.music.unpause()  # Play sound when turn
                
            
                if event.type == pygame.MOUSEBUTTONDOWN and turn == "player":  # Player's turn
                    if dice_button_rect.collidepoint(event.pos):
                        dice_roll = randint(1, 6)
                        print(f"Player rolled: {dice_roll}")
                        
                        target_position_1= current_player_position + dice_roll
                        
                        player_start_coords = get_square_coordinates(current_player_position)
                        player_end_coords = get_square_coordinates(target_position_1)
                        move_icon(player_start_coords, player_end_coords)
                        
                        if target_position_1 > 100:
                            continue

                        if target_position_1 in ladder:  # Check ladders
                            target_position_1 = ladder[target_position_1]
                            print("Player climbed a ladder!")

                        elif target_position_1 in snakes:  # Check snakes
                            target_position_1 = snakes[target_position_1]
                            print("Player got bitten by a snake!")

                       
                    
                       
                    
                        if current_player_position == 100:
                            print("Player wins!")
                            running = False
                            continue
                    
                        turn = "computer"  # Switch to computer's turn

            if turn == "computer" and running:  # Computer's turn
                pygame.time.delay(3000)  # Pause for realism
                dice_roll = randint(1, 6)
                print(f"Computer rolled: {dice_roll}")
                
                target_position_2= current_computer_position + dice_roll
                computer_start_coords = get_square_coordinates(current_computer_position)
                computer_end_coords = get_square_coordinates(target_position_2)
                move_icon(computer_start_coords, computer_end_coords)
                
                
                if target_position_2 > 100:
                    turn = "player"
                    continue

                if target_position_2 in ladder:  # Check ladders
                    target_position_2 = ladder[target_position_2]
                    print("Computer climbed a ladder!")

                elif target_position_2 in snakes:  # Check snakes
                    target_position_2 = snakes[target_position_2]
                    print("Computer got bitten by a snake!")

               
                current_player_position = target_position_1
                print(f"Player is now at position {current_player_position}")
                
                current_computer_position = target_position_2
                print(f"Computer is now at position {current_computer_position}")
                

                if current_computer_position == 100:
                    print("Computer wins!")
                    running = False
                    continue

                turn = "player"  # Switch to player's turn

        # Drawing the screen
            screen.fill(WHITE)
            screen.blit(image, (20, 20))  # Redraw the board
            screen.blit(dice_image, (650, 300))  # Redraw the dice button

            pygame.draw.rect(screen, BLACK, back_button_rect, border_radius=5)
            font = pygame.font.Font(None, 20) 
            back_text = font.render("Back", True, WHITE)
            back_text_rect = back_text.get_rect(center=back_button_rect.center)
            screen.blit(back_text, back_text_rect)
            
            button_color = PURPLE if sound_on else BLACK
            pygame.draw.rect(screen, button_color, sound_button_rect)
            sound_text = font.render("Sound ON" if sound_on else "Sound OFF", True, WHITE)
            sound_text_rect = sound_text.get_rect(center=sound_button_rect.center)
            screen.blit(sound_text, sound_text_rect)
            
        # Draw the player's and computer's positions
            global player_coords
            player_coords = get_square_coordinates(target_position_1)
            pygame.draw.circle(screen, GREEN, player_coords, 10)  # Player marker
           
            global computer_coords
            computer_coords = get_square_coordinates(current_computer_position)
            pygame.draw.circle(screen, PURPLE, computer_coords, 10)  # Computer marker
        
            pygame.display.update()
            clock.tick(60)
      
    def move_icon(start_coords, end_coords):              
    # Convert coordinates to Vector2 for calculations
        start_pos = pygame.math.Vector2(start_coords)
        end_pos = pygame.math.Vector2(end_coords)
        position = pygame.math.Vector2(start_pos)

        speed = 10  # Speed of movement
        direction = (end_pos - start_pos).normalize()  # Normalized direction vector

# Function to draw the tokens at specific positions
        def draw_tokens():
            screen.fill(WHITE)  # Clear the screen
            screen.blit(image, (20, 20))  # Redraw the board
            screen.blit(dice_image, (650, 300))

            if turn == "player":
                pygame.draw.circle(screen, PURPLE, computer_coords, 10)
                pygame.draw.circle(screen, GREEN, (int(position.x), int(position.y)), 10)
            elif turn == "computer":
                pygame.draw.circle(screen, PURPLE, (int(position.x), int(position.y)), 10)
                pygame.draw.circle(screen, GREEN, player_coords, 10)
            elif turn is None:
                pygame.draw.circle(screen, GREEN, (int(position.x), int(position.y)), 10)

# Step 1: Pause at the start position to show the position
        draw_tokens()
        pygame.display.update()
        pygame.time.wait(500)  # Pause for 500ms (half a second)

# Step 2: Move diagonally up the ladder
        while position.distance_to(end_pos) > speed:
            position += direction * speed
            draw_tokens()  # Redraw the tokens at the current position
            pygame.display.update()
            pygame.time.delay(90)  # Control animation speed

# Ensure the final position is exact
        position = start_pos
        draw_tokens()  # Final position
        pygame.display.update()



    

    running = True
    while running:
        screen.fill(WHITE)
        draw_buttons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            handle_button_click(event)
        
        pygame.display.update()
        clock.tick(60)

    pygame.quit()


main()
