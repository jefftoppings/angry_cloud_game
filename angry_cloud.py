import pygame
import time
import random

pygame.init()

# initialize default display size
display_width = 800
display_height = 600

# define colours to be used
colours = {
    'black' : (0,0,0),
    'white' : (255,255,255),
    'red' : (200,0,0),
    'green' : (0,200,0),
    'blue' : (0,0,255),
    'brown' : (141,101,71),
    'bright_red' : (255,0,0),
    'bright_green' : (0,255,0),
    'light_gray' : (192,192,192),
    'dark_gray' : (173,173,173) }

# sound effects
game_over = pygame.mixer.Sound('game_over.wav')
ding = pygame.mixer.Sound('ding.wav')
splash = pygame.mixer.Sound('splash.wav')
explosion = pygame.mixer.Sound('Explosion.wav')

# background music (randomized)
selection = random.randint(1, 3)
music = {1: 'Mr_Tea.mp3',
         2: 'Race_Car.mp3',
         3: 'background_music.mp3'}
pygame.mixer.music.load(music[selection])

# create size of frame
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Angry Cloud")
clock = pygame.time.Clock()

# car image
car_image = pygame.image.load('racecar.png')
car_width = 100
flaming_car = pygame.image.load('flaming_racecar.png')

# set icon for game (proper size is 32x32)
pygame.display.set_icon(pygame.image.load('raincloud.png'))

# raindrop
raindrop = pygame.image.load('raindrop.png')
raindrop_small = pygame.image.load('raindrop_small.png')  # 30w x 49h


# Background object to display image
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


# background image
bg_image = Background("cloud_background.png", [0, 0])


def score(count):
    """
    Displays the current score in the game window
    :param count: the current score
    """
    font = pygame.font.SysFont(None, 25)
    text = font.render('Score: ' + str(count), True, colours['black'])
    screen.blit(text, (0, 0))


def level(count):
    """
    Displays the current level in the game window
    :param count: the current level
    """
    font = pygame.font.SysFont(None, 25)
    text = font.render('Level: ' + str(count), True, colours['black'])
    screen.blit(text, (0, 30))


def draw_rectangle(rect_x, rect_y, rect_width, rect_height, colour):
    """
    Draws a rectangle
    :param rect_x: starting x coordinate
    :param rect_y: starting y coordinate
    :param rect_width: width of rectangle
    :param rect_height: height of rectangle
    :param colour: colour of rectangle
    """
    pygame.draw.rect(screen, colour, [rect_x, rect_y, rect_width, rect_height])


def new_drop(x, y):
    """
    Puts a new raindrop in the game display
    :param x: x coordinate
    :param y: y coordinate
    """
    screen.blit(raindrop_small, (x, y))


def car(x, y):
    """
    Updates the car position in the game display
    :param x: x coordinate
    :param y: y coordinate
    """
    screen.blit(car_image, (x, y))


def text_objects_black(text, font):
    """
    Displays text with black font onto the game display
    :param text: message to display
    :param font: font type
    :return: tuple containing the object
    """
    surface = font.render(text, True, colours['black'])
    return surface, surface.get_rect()


def text_objects_white(text, font):
    """
    Displays text with white font onto the game display
    :param text: message to display
    :param font: font type
    :return: tuple containing the object
    """
    surface = font.render(text, True, colours['white'])
    return surface, surface.get_rect()


def game_over_message(text):
    """
    Displays message at the end of the game
    :param text: text to display
    """
    large_text = pygame.font.SysFont("comicsansms", 100)
    text_surface, text_rect = text_objects_black(text, large_text)
    text_rect.center = (display_width/2, display_height/2)
    screen.blit(text_surface, text_rect)
    pygame.display.update()
    time.sleep(3)
    game_intro()


def crash():
    """
    Sequence of events when a raindrop hits the car
    """
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(game_over)
    pygame.mixer.Sound.play(splash)
    pygame.mixer.Sound.play(explosion)
    game_over_message('Game Over')


def button(msg, x, y, width, height, inactive_colour, active_colour, action=None):
    """
    Create a button on the game display
    :param msg: text on the button
    :param x: x coordinate
    :param y: y coordinate
    :param width: width of button
    :param height: height of button
    :param inactive_colour: colour when inactive
    :param active_colour: colour when active
    :param action: action performed when clicked
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    global screen

    # determine if button is clicked
    if x < mouse[0] < x+width and y < mouse[1] < y+height:
        pygame.draw.rect(screen, active_colour, (x, y, width, height))
        if click[0] == 1 and action is not None:
            if action == "play":
                main()
            elif action == "quit":
                pygame.quit()
                quit()
            elif action == 'fullscreen':
                screen = pygame.display.set_mode((display_width, display_height), pygame.FULLSCREEN)
    else:
        pygame.draw.rect(screen, inactive_colour, (x, y, width, height))

    # put text on button
    small_text = pygame.font.SysFont("comicsansms", 20)
    text_surf, text_rect = text_objects_black(msg, small_text)
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    screen.blit(text_surf, text_rect)


def game_intro():
    """
    Main menu that is displayed when the game is opened initially and after a current game is lost
    """
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # display title of game at top
        screen.fill(colours['white'])
        screen.blit(bg_image.image, bg_image.rect)
        large_text = pygame.font.SysFont("comicsansms", 90)
        text_surf, text_rect = text_objects_black("Angry Cloud", large_text)
        text_rect.center = (display_width/2, 315)
        screen.blit(text_surf, text_rect)

        # display credits at bottom
        credits_text = pygame.font.SysFont("comicsansms", 10)
        text_surf1, text_rect1 = text_objects_white("Developed by Jeffrey Toppings", credits_text)
        text_rect1.center = (display_width/2, 580)
        screen.blit(text_surf1, text_rect1)

        # display simple directions
        help_text = pygame.font.SysFont("comicsansms", 15)
        text_surf2, text_rect2 = text_objects_white("Use arrow keys to dodge the raindrops!", help_text)
        text_rect2.center = (display_width/2, 530)
        screen.blit(text_surf2, text_rect2)

        # create buttons for play and quit
        button("Play", 150, 425, 100, 50, colours['dark_gray'], colours['light_gray'], "play")
        button("Quit", 550, 425, 100, 50, colours['dark_gray'], colours['light_gray'], "quit")
        button("Full Screen", 338, 425, 120, 50, colours['dark_gray'], colours['light_gray'], "fullscreen")

        pygame.display.update()
        clock.tick(10)


def main():
    """
    Main program that runs an instance of the game
    """
    # loop music
    pygame.mixer.music.play(-1)

    # initial car position
    car_x = display_width*0.45
    car_y = display_height*0.8
    car_height = 56
    x_change = 0

    # stats
    dodged = 0
    current_level = 1

    # initialize raindrops
    drop_x = random.randrange(0, display_width)
    drop_y = -600
    drop_speed = 7
    drop_width = 30
    drop_height = 49

    game_exit = False
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # move car
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    x_change = -5
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or \
                                event.key == pygame.K_a or event.key == pygame.K_d:
                    x_change = 0 

        # update car position
        car_x += x_change

        # enable background
        screen.fill(colours['white'])
        screen.blit(bg_image.image, bg_image.rect)

        # initialize next drop
        car(car_x, car_y)
        new_drop(drop_x, drop_y)
        drop_y += drop_speed

        # update stats
        score(dodged)
        level(current_level)

        # handle logic
        # successfully dodged raindrop
        if drop_y > display_height:
            drop_y = 0 - drop_height
            drop_x = random.randrange(0, display_width)
            dodged += 1
            pygame.mixer.Sound.play(ding).set_volume(0.3)

            # advance levels
            if dodged % 10 == 0:
                current_level += 1
                large_text = pygame.font.SysFont("comicsansms", 80)
                text_surface, text_rect = text_objects_black('Level ' + str(current_level), large_text)
                text_rect.center = (display_width / 2, display_height / 2)
                screen.blit(text_surface, text_rect)
                pygame.display.update()
                time.sleep(0.3)
                drop_speed *= 1.2

        # detect if collision occurred
        if car_y <= drop_y <= car_y + car_height - 20:
            if (car_x <= drop_x <= car_x + car_width) and (car_x <= drop_x + drop_width <= car_x + car_width):
                screen.blit(flaming_car, (car_x, car_y))
                crash()

        # update display
        pygame.display.update()
        clock.tick(60)


game_intro()        
main()
pygame.quit()
quit()

