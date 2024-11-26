import pygame
import sys
import webbrowser

# Initialize Pygame
pygame.init()

# Load and play background music (this will be general background music for the entire game)
pygame.mixer.init()  # Initialize the mixer module
pygame.mixer.music.load(r"C:\Users\kashv\Downloads\garden-ambience-236744.mp3")
pygame.mixer.music.set_volume(0.7)  # Set the volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Play the music on loop (-1 means infinite loop)

# Load sound effect (glitter sound)
glitter_sound = pygame.mixer.Sound(r"C:\Users\kashv\Downloads\glitter-sound-effect-for-music-or-editing-224184.mp3")

# Screen dimensions
WIDTH, HEIGHT = 600, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kashvi's Portfolio")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load sprite sheets
sprite_sheet = pygame.image.load(r"C:\Users\kashv\Downloads\Fairy\Fairy\Fairy 1.png").convert_alpha()
grass_sheet = pygame.image.load(r"C:\Users\kashv\Downloads\GRASS+.png").convert_alpha()
projects_sprite_sheet = pygame.image.load(r"C:\Users\kashv\Downloads\WarpDoor.png").convert_alpha()
About_sprite_sheet = pygame.image.load(r"C:\Users\kashv\Downloads\WarpDoor.png").convert_alpha()
skills_sprite_sheet = pygame.image.load(r"C:\Users\kashv\Downloads\WarpDoor.png").convert_alpha()
Contact_sprite_sheet = pygame.image.load(r"C:\Users\kashv\Downloads\WarpDoor.png").convert_alpha()

# Extract frames from sprite sheets
def extract_frames(sheet, frame_width, frame_height, rows, cols):
    frames = []
    for row in range(rows):
        for col in range(cols):
            x = col * frame_width
            y = row * frame_height
            rect = pygame.Rect(x, y, frame_width, frame_height)
            frame = sheet.subsurface(rect)
            frames.append(frame)
    return frames

# Scale frames
def scale_frames(frames, scale_factor):
    scaled_frames = []
    for frame in frames:
        width, height = frame.get_size()
        scaled_frame = pygame.transform.scale(frame, (int(width * scale_factor), int(height * scale_factor)))
        scaled_frames.append(scaled_frame)
    return scaled_frames

# Load animations
CHARACTER_SCALE = 3
walk_frames = scale_frames(extract_frames(sprite_sheet, 32, 32, 1, 8), CHARACTER_SCALE)
TILE_SIZE = 16
ZOOM_FACTOR = 2
grass_tile = pygame.transform.scale(
    grass_sheet.subsurface(pygame.Rect(4 * TILE_SIZE, 9 * TILE_SIZE, TILE_SIZE, TILE_SIZE)),
    (TILE_SIZE * ZOOM_FACTOR, TILE_SIZE * ZOOM_FACTOR),
)

def load_zone_animations(sheet, frame_size, rows, cols, scale):
    frames = extract_frames(sheet, *frame_size, rows, cols)
    return scale_frames(frames, scale)

zones_animations = {
    "Projects": load_zone_animations(projects_sprite_sheet, (64, 64), 3, 3, 2),
    "About": load_zone_animations(About_sprite_sheet, (64, 64), 3, 3, 2),
    "Skills": load_zone_animations(skills_sprite_sheet, (64, 64), 3, 3, 2),
    "Contact": load_zone_animations(Contact_sprite_sheet, (64, 64), 3, 3, 2),
}

# Player variables
player_x, player_y = 200, 200
player_speed = 5
current_frame, last_update, animation_delay = 0, pygame.time.get_ticks(), 200

# Zone details
houses = {
    "About": (30, 30, 40, 40),  # Top-left
    "Projects": (WIDTH - 110, 30, 40, 40),  # Top-right
    "Skills": (30, HEIGHT - 160, 40, 40),  # Adjusted bottom-left
    "Contact": (WIDTH - 110, HEIGHT - 160, 40, 40),  # Adjusted bottom-right
}

portfolio_info = {
    "Projects": [
        "1. Movie Reccomendation System using FastAPI for the backend ",
        "   and HTML/CSS/JavaScript for the frontend.",
        "2. Exploratory Data Analysis on my personal Letterboxd Data",
        "3. Emotion Detector using CNN, trained on FER2013 dataset",
        "4. News Summariser using BART & ",
        "   fine-tuned on CNN Dailymail dataset",
        "5. Stock Predictor full stack web app using LSTM model",
        "6. Sticky Notes web app allowing users to create notes",
        "7. Hangman using Javascript with integrated responsive design"
    ],
    "About": [
    "I'm Kashvi Srivastava, a passionate computer science",
    "student with a strong background in programming and",
    "software development. I’m pursuing my BTech in ",
    "Computer Science from VIT, Vellore. I am proficient in",
    "Python and Java and I enjoy tackling challenges in AI, ML,",
    "data engineering, and NLP. Always looking to learn and push",
    "my boundaries, both technically and socially",
    
],
    "Skills": [
    "",
    "",
    "Python, C/C++, HTML, CSS, Java, SQL, Pygame", 
    "Git, Flask, MySQL, JavaScript, FastApi, Postman, Pytest", 
    "pandas, numpy, Matplotlib,Tensorflow, Scikit-Learn, Pytorch", 
    ],
    "Contact": ["Email: kashvi.0508@gmail.com", "Phone: +91-9662049106"],
}

# Function to display text
def draw_text(text, x, y, color=WHITE):
    font = pygame.font.Font(None, 24)
    screen.blit(font.render(text, True, color), (x, y))

# Zone display functions
def display_zone_info(zone_name):
    clock = pygame.time.Clock()
    running = True
    # Load the contact background image (only when in the Contact section)
    contact_bg = pygame.image.load(r"C:\Users\kashv\Downloads\contact\Free-Castle-Interior-Pixel-Game-Backgrounds\PNG\background 1\background 1.png")
    # Scale the contact background to window size (550x450)
    contact_bg_scaled = pygame.transform.scale(contact_bg, (WIDTH, HEIGHT)) if zone_name == "Contact" else None
    project_bg=pygame.image.load(r"C:\Users\kashv\Downloads\projects\underwater-fantasy-files\underwater-fantasy-files\PNG\underwater-fantasy-preview.png")
    project_bg_scaled = pygame.transform.scale(project_bg, (WIDTH, HEIGHT)) if zone_name == "Projects" else None
    about_bg=pygame.image.load(r"C:\Users\kashv\Downloads\about\space_background_pack\space_background_pack\Assets\Blue Version\blue-preview.png")
    about_bg_scaled = pygame.transform.scale(about_bg, (WIDTH, HEIGHT)) if zone_name == "About" else None
    skills_bg=pygame.image.load(r"C:\Users\kashv\Downloads\skills\sky.png")
    skills_bg_scaled=pygame.transform.scale(skills_bg, (WIDTH, HEIGHT)) if zone_name == "Skills" else None
    while running:
        screen.fill(BLACK)
        for y in range(0, HEIGHT, TILE_SIZE * ZOOM_FACTOR):
            for x in range(0, WIDTH, TILE_SIZE * ZOOM_FACTOR):
                screen.blit(grass_tile, (x, y))

        # Only display contact background image when in the Contact section
        if zone_name == "Contact" and contact_bg_scaled:
            screen.blit(contact_bg_scaled, (0, 0))  # Scale and display the image
        if zone_name == "Projects" and project_bg_scaled:
            screen.blit(project_bg_scaled, (0, 0))
        if zone_name == "About" and about_bg_scaled:
            screen.blit(about_bg_scaled, (0, 0))
        if zone_name == "Skills" and skills_bg_scaled:
            screen.blit(skills_bg_scaled, (0, 0))

        draw_text(f"{zone_name} Section", WIDTH // 2 - 80, 20, WHITE)
        for i, line in enumerate(portfolio_info[zone_name]):
            draw_text(line, 40, 80 + i * 30, WHITE)
        draw_text("Press 'B' and Arrow Keys to exit", 40, HEIGHT - 40, WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if pygame.key.get_pressed()[pygame.K_b]:
            running = False

        pygame.display.flip()
        clock.tick(30)

# Update animation
def update_zone_animation(zone_name, frame_vars):
    now = pygame.time.get_ticks()
    if now - frame_vars["last_update"] > frame_vars["delay"]:
        frame_vars["last_update"] = now
        frame_vars["current_frame"] = (frame_vars["current_frame"] + 1) % len(zones_animations[zone_name])

zone_frames = {
    zone: {"current_frame": 0, "last_update": pygame.time.get_ticks(), "delay": 300}
    for zone in houses
}

# Define the timer for the sound effect
sound_played = False
sound_play_time = 0

# Function to play the glitter sound for 1 second when entering a zone
def play_glitter_sound_for_1_second():
    global sound_played, sound_play_time
    if not sound_played:
        glitter_sound.play()  # Play the sound
        sound_played = True
        sound_play_time = pygame.time.get_ticks()  # Set the time when the sound was played

# Main game loop
def main():
    global player_x, player_y, current_frame, last_update, sound_played, sound_play_time
    contact_music_playing = False  # Track if the Contact music is playing
    clock = pygame.time.Clock()
    running = True
    moving, facing_left = False, False

    while running:
        screen.fill(BLACK)
        for y in range(0, HEIGHT, TILE_SIZE * ZOOM_FACTOR):
            for x in range(0, WIDTH, TILE_SIZE * ZOOM_FACTOR):
                screen.blit(grass_tile, (x, y))

        for zone_name, (x, y, w, h) in houses.items():
            update_zone_animation(zone_name, zone_frames[zone_name])
            screen.blit(zones_animations[zone_name][zone_frames[zone_name]["current_frame"]], (x, y))

        keys = pygame.key.get_pressed()
        moving = False
        if keys[pygame.K_UP]: player_y -= player_speed; moving = True
        if keys[pygame.K_DOWN]: player_y += player_speed; moving = True
        if keys[pygame.K_LEFT]: player_x -= player_speed; moving = True; facing_left = True
        if keys[pygame.K_RIGHT]: player_x += player_speed; moving = True; facing_left = False

        player_x = max(0, min(WIDTH - 96, player_x))
        player_y = max(0, min(HEIGHT - 96, player_y))

        # Update character animation
        now = pygame.time.get_ticks()
        if moving and now - last_update > animation_delay:
            last_update = now
            current_frame = (current_frame + 1) % len(walk_frames)

        # Render player
        frame = walk_frames[current_frame] if moving else walk_frames[0]
        if facing_left: frame = pygame.transform.flip(frame, True, False)
        screen.blit(frame, (player_x, player_y))

        # Check collisions with zones
        player_rect = pygame.Rect(player_x, player_y, 96, 96)
        for zone_name, (x, y, w, h) in houses.items():
            if player_rect.colliderect(pygame.Rect(x, y, w, h)):
                play_glitter_sound_for_1_second()  # Play glitter sound for 1 second
                if zone_name == "Contact" and not contact_music_playing:
                    # Play the medieval sound when entering the Contact section
                    pygame.mixer.music.load(r"C:\Users\kashv\Downloads\contact\medeival-sound.mp3")
                    pygame.mixer.music.play()
                    contact_music_playing = True  # Set flag that music is playing
                if zone_name == "About" and not contact_music_playing:
                    # Play the medieval sound when entering the Contact section
                    pygame.mixer.music.load(r"C:\Users\kashv\Downloads\about\space-rumble-29970.mp3")
                    pygame.mixer.music.play()
                    contact_music_playing = True  # Set flag that music is playing
                if zone_name == "Skills" and not contact_music_playing:
                    # Play the medieval sound when entering the Contact section
                    pygame.mixer.music.load(r"C:\Users\kashv\Downloads\skills\wind-whispers-with-birds-ambiance-209840.mp3")
                    pygame.mixer.music.play()
                    contact_music_playing = True  # Set flag that music is playing
                if zone_name == "Projects" and not contact_music_playing:
                    # Play the medieval sound when entering the Contact section
                    pygame.mixer.music.load(r"C:\Users\kashv\Downloads\underwater-cavern-159985.mp3")
                    pygame.mixer.music.play()
                    contact_music_playing = True  # Set flag that music is playing
                display_zone_info(zone_name)

        # Stop the sound after 1 second
        if sound_played and pygame.time.get_ticks() - sound_play_time > 1000:
            sound_played = False  # Reset flag after 1 second

        # Stop music if player leaves the Contact section
        if contact_music_playing and not any(player_rect.colliderect(pygame.Rect(x, y, w, h)) for zone_name, (x, y, w, h) in houses.items() if zone_name == "Contact"):
            pygame.mixer.music.stop()
            contact_music_playing = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
