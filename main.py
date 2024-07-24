import pygame
import time
import random
pygame.font.init()

WIDTH =700
HEIGHT=500
PLAYER_HEIGHT=30
PLAYER_WIDTH=20
PLAYER_VEL = 3
STAR_WIDTH = 5
STAR_HEIGHT = 20
STAR_VEL = 3

PLAYER_IMG = pygame.image.load('roc2.png')
BOOM_IMG = pygame.image.load('boom.png')
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("star dodge")


BG = pygame.transform.scale(pygame.image.load("bg.gif").convert(), (WIDTH, HEIGHT))

FONT = pygame.font.SysFont("comicsans" , 30)

def draw_start_screen():
    WIN.blit(BG, (0, 0))
    start_text = FONT.render("Press SPACE to start", True, "white")
    WIN.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2 - start_text.get_height()//2))
    pygame.display.update()

def draw(player,elaspsed_time,stars):
    WIN.blit(BG, (0, 0))
    
    time_text = FONT.render(f"Time:{round(elaspsed_time)}s" , 1 , "white")
    
    WIN.blit(time_text , (10,10))
    
    WIN.blit(PLAYER_IMG, (player.x, player.y))
    
    for star in stars:
        pygame.draw.rect(WIN , "White" , star)
    
    pygame.display.update()

def main():
    
    pygame.mixer.init()  # Initialize Pygame mixer
    GAME_OVER_SOUND = pygame.mixer.Sound('gameover.wav')
    pygame.mixer.music.load('bgm.mp3')  # Example background music (optional)
    pygame.mixer.music.play(-1)
    
    run = True
    game_started = False
    player=pygame.Rect(200,HEIGHT-PLAYER_HEIGHT,PLAYER_WIDTH,PLAYER_HEIGHT)
    
    clock = pygame.time.Clock() 
    start_time = time.time()
    elapsed_time = 0
    
    star_add_increment = 2000
    star_count = 0
    
    stars = []
    hit = False
    
    draw_start_screen()
    
    while not game_started:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_started = True
                elif event.type == pygame.QUIT:
                    run = False
                    game_started = True
                    break
    
    while run:
        
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time
        
        if star_count > star_add_increment:
            for i in range(5):
                star_x = random.randint(0,WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x , -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
                
            star_add_increment = max(200,star_add_increment - 50)
            star_count = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                break
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >=0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT]and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VEL  
            
        for star in stars[:]:
            star.y+=STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break
        
        if hit:
            pygame.mixer.music.stop()
            scaled_boom_img = pygame.transform.scale(BOOM_IMG, (PLAYER_IMG.get_width()*2, PLAYER_IMG.get_height()/2))
            WIN.blit(scaled_boom_img,(player.x, player.y))
            GAME_OVER_SOUND.play()
            lost_text=FONT.render(f"GAME OVER !!",1,"white")
            WIN.blit(lost_text,(WIDTH/2 - lost_text.get_width()/2 ,HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(5000)
            break
        
        draw(player,elapsed_time,stars)
    pygame.mixer.quit()
    pygame.quit()
    
if __name__ == "__main__":
    main()
       