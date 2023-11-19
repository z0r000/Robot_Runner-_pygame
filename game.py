import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player_walk_11.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player_walk_22.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/jumpp.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 510))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('graphics/jump.mp3')
        self.jump_sound.set_volume(0.5)


    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 510:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 0.75
        self.rect.y += self.gravity
        if self.rect.bottom >= 510:
            self.rect.bottom = 510

    def animation_state(self):
        if self.rect.bottom < 510:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly11.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly22.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 410
        else:
            monster_1 = pygame.image.load('graphics/11.png').convert_alpha()
            monster_2 = pygame.image.load('graphics/55.png').convert_alpha()
            self.frames = [monster_1, monster_2]
            y_pos = 515

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(1100, 1300), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -150:
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))

    score_rect = score_surf.get_rect(center=(600, 40))

    screen.blit(score_surf, score_rect)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


pygame.init()
screen = pygame.display.set_mode((1200, 670))
pygame.display.set_caption('Robot Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('graphics/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
highscore = 0
bg_music = pygame.mixer.Sound('graphics/ff.wav')
bg_music.play(loops=-1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

bg = pygame.image.load('graphics/bg6.jpg').convert()


# Intro screen
player_stand = pygame.image.load('graphics/player_standd.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(600, 335))

game_name = test_font.render('Robot Runner', False, 'white')
game_name_rect = game_name.get_rect(center=(600, 175))

game_message = test_font.render('Press space to run', False, 'white')
game_message_rect = game_message.get_rect(center=(600, 530))




# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)
#counter
i = 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'monster', 'fly', 'monster'])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        screen.blit(bg, (0,0))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()


    else:
        screen.fill((85,107,47))
        pygame.draw.rect(screen,'white',player_stand_rect,10)
        screen.blit(player_stand, player_stand_rect)
        score_message = test_font.render(f'Your score: {score}', False, 'white')
        score_message_rect = score_message.get_rect(center=(600, 550))
        newhighscore_message = test_font.render('New highscore!!!', False, 'white')
        newhighscore_message_rect = newhighscore_message.get_rect(center=(600, 140))
        file = "highscores.csv"
        prev_high_scores = []

        with open(file, "a") as f:
            f.write(f'{score}\n')

        with open(file, "r") as f:
            for line in f:
                k =int(line.strip())
                prev_high_scores.append(k)
        highscore = max(prev_high_scores)
        screen.blit(game_name, game_name_rect)
        highscore_message = test_font.render(f'highscore: {highscore}', False, 'white')
        highscore_message_rect = highscore_message.get_rect(center=(600, 100))

        if score ==0:
            screen.blit(game_message, game_message_rect)

        else:
            screen.blit(highscore_message, highscore_message_rect)
            screen.blit(score_message, score_message_rect)
            if score == highscore:
                screen.blit(newhighscore_message,newhighscore_message_rect)

    pygame.display.update()
    clock.tick(60)





