import pygame
import sys
import random
import button

pygame.init()

width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
fps = 60

# images
background = pygame.image.load("images/background.png").convert_alpha()
ground1 = pygame.image.load("images/ground.png").convert_alpha()
ground1b = pygame.image.load("images/5ground.png").convert_alpha()
ground2 = pygame.image.load("images/road.png").convert_alpha()
train = pygame.image.load("images/train.png").convert_alpha()
back_img = pygame.image.load("images/back_btn.png").convert_alpha()

bird1 = pygame.image.load("images/1bird.png").convert_alpha()
bird2 = pygame.image.load("images/2bird.png").convert_alpha()
pipe1 = pygame.image.load("images/pipe.png").convert_alpha()
rotatedPipe1 = pygame.image.load("images/rotated_pipe.png").convert_alpha()
pipe3 = pygame.image.load("images/3pipe.png").convert_alpha()
rotatedPipe3 = pygame.image.load("images/3rotated_pipe.png").convert_alpha()

rotatedPipe = rotatedPipe1
pipe = pipe3
bird = bird1

red = (255, 0, 0)

choice_list = [1, 2]

myChoice = random.choice(choice_list)

if myChoice == 1:
    rotatedPipe = rotatedPipe1
else:
    rotatedPipe = rotatedPipe3

myChoice = random.choice(choice_list)
if myChoice == 2:
    pipe = pipe3
else:
    pipe = pipe1

# sounds
point = pygame.mixer.Sound("sounds/sfx_point.wav")
hit = pygame.mixer.Sound("sounds/sfx_hit.wav")
music = pygame.mixer.Sound("sounds/FoamRubber-320bit.wav")

# Game Caption
pygame.display.set_caption("Flappy Bird")


def get_highest_score():

    with open("highest_score.txt", "r") as f:
        return f.read()


class Game:
    def __init__(self):
        self.gameOn = True
        self.state = True

        self.birdX = 100
        self.birdY = 100

        self.rotated_pipe = self.pipe_color_r()
        self.pipe = self.pipe_color()
        self.pipesX = [width, width + 400, width + 800, width + 1200]
        self.lowerPipeY = [self.random_pipe(), self.random_pipe(), self.random_pipe(), self.random_pipe()]
        self.upperPipeY = [self.random_rotated_pipe(), self.random_rotated_pipe(), self.random_rotated_pipe(),
                           self.random_rotated_pipe()]
        self.gravity = 0
        self.pipeVel = 0
        self.ground1X = 100
        self.ground1bX = 1050
        self.trainX = -1300
        self.bridgeVel = 0
        self.trainVel = 0
        self.flap = 0
        self.score = 0
        self.rotateAngle = 0
        self.is_game_over = False
        self.playSound = True
        self.background_x = 0
        self.background_y = 0
        self.background_x_vel = 0
        self.ground2_x = 0
        self.ground2_y = 665
        self.ground2_x_vel = 0

    def moving_pipe(self):

        self.trainX += self.trainVel * 3
        if self.trainX > width + 1300:
            self.trainX = -650

        self.ground1X += -self.bridgeVel * 3
        self.ground1bX += -self.bridgeVel * 3
        if self.ground1X < -250:
            self.ground1X = width + 150
        if self.ground1bX < -250:
            self.ground1bX = width + 150

        for i in range(0, 4):
            self.pipesX[i] += -self.pipeVel

        for i in range(0, 4):
            if self.pipesX[i] < -50:
                self.rotated_pipe = self.pipe_color_r()
                self.pipe = self.pipe_color()
                self.pipesX[i] = width + 100
                self.lowerPipeY[i] = self.random_pipe()
                self.upperPipeY[i] = self.random_rotated_pipe()

    def moving_background(self, background_x, background_y, my_background):
        screen.blit(my_background, (background_x, background_y))
        screen.blit(my_background, (background_x + width, background_y))

    def moving_ground2(self, ground2_x, ground2_y, my_ground2):
        screen.blit(my_ground2, (ground2_x, ground2_y))
        screen.blit(my_ground2, (ground2_x + width, ground2_y))

    @staticmethod
    def random_pipe():
        return random.randrange(int(height / 2) + 50, height - 200)

    @staticmethod
    def pipe_color_r():
        choice_lists = [1, 2]
        my_choice = random.choice(choice_lists)

        if my_choice == 1:
            return rotatedPipe1
        else:
            return rotatedPipe3

    @staticmethod
    def pipe_color():
        choice_lists = [1, 2]
        my_choice = random.choice(choice_lists)

        if my_choice == 2:
            return pipe1
        else:
            return pipe3

    def random_rotated_pipe(self):
        return random.randrange(-int(height / 2) + 50, -200)

    def flapping(self):
        if self.state:
            self.birdY += self.gravity
            if not self.is_game_over:
                self.flap -= 1
                self.birdY -= self.flap

    def is_collide(self):
        for i in range(0, 4):
            if (self.birdX >= self.pipesX[i] and self.birdX <= (self.pipesX[i] + pipe.get_width())
                    and ((self.birdY + bird.get_height() - 15) >= self.lowerPipeY[i] or
                         self.birdY <= self.upperPipeY[i] + self.rotated_pipe.get_height() - 15)):
                return True

            elif (self.birdX == self.pipesX[i] and (
                    self.birdY <= self.lowerPipeY[i] and self.birdY >= self.upperPipeY[i])):
                if not self.is_game_over:
                    self.score += 1
                    pygame.mixer.Channel(1).play(point)

        if self.birdY <= 0:
            return True

        elif self.birdY + bird.get_height() >= height:
            self.gravity = 0
            return True

        return False

    def game_over(self):
        if self.is_collide():
            self.is_game_over = True
            self.screen_text("Game Over!", (133, 26, 3), 450, 300, 84, "Fixedsys", bold=True)
            self.screen_text("Press Enter To Play Again", (255, 255, 255), 400, 600, 48, "Fixedsys", bold=True)
            self.pipeVel = 0
            self.bridgeVel = 0
            self.trainVel = 0
            self.flap = 0
            self.rotateAngle = -90
            self.background_x_vel = 0
            self.ground2_x_vel = 0
            if self.playSound:
                pygame.mixer.Channel(1).play(hit)
                self.playSound = False

    def screen_text(self, text, color, x, y, size, style, bold=False):
        font = pygame.font.SysFont(style, size, bold=bold)
        screen_text = font.render(text, True, color)
        screen.blit(screen_text, (x, y))

    def main_game(self):

        try:
            highest_score = int(get_highest_score())
        except:
            highest_score = 0

        while self.gameOn:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_LALT or event.key == pygame.K_SPACE) and self.state:
                        if not self.is_game_over:
                            self.state = True
                            self.pipeVel = 5
                            self.bridgeVel = 2
                            self.trainVel = 2
                            self.gravity = 5
                            self.flap = 18
                            self.rotateAngle = 20

                        if self.score > 10:
                            self.pipeVel = 8
                            self.bridgeVel = 3
                            self.trainVel = 2

                        if self.score > 15:
                            self.pipeVel = 10
                            self.bridgeVel = 4
                            self.trainVel = 3

                    if event.key == pygame.K_RETURN:
                        self.state = True
                        new_game = Game()
                        new_game.main_game()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.rotateAngle = 0

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.is_game_over = False
                        self.pipeVel = 0
                        self.bridgeVel = 0
                        self.trainVel = 0
                        self.flap = 18
                        self.gravity = 0
                        self.rotateAngle = 20
                        self.background_x_vel = 5
                        self.ground2_x_vel = 8

                        self.state = False

                    if event.key == pygame.K_q:
                        self.state = True

            # blitting images
#            screen.blit(background, (0, 0))

            self.moving_background(self.background_x, self.background_y, background)


            for i in range(0, 4):

                choice_lists = [1, 2]
                my_choice = random.choice(choice_lists)

                if my_choice == 1:
                    self.bird = bird1
                else:
                    self.bird = bird2

                # lower Pipe
                screen.blit(self.pipe, (self.pipesX[i], self.lowerPipeY[i]))
                # upper pipe
                screen.blit(self.rotated_pipe, (self.pipesX[i], self.upperPipeY[i]))

            screen.blit(pygame.transform.rotozoom(self.bird, self.rotateAngle, 1), (self.birdX, self.birdY))

            screen.blit(ground1, (self.ground1X, 235))
            screen.blit(ground1b, (self.ground1bX, 235))
            #   screen.blit(ground1, (self.ground1X + 635, 235))

            # screen.blit(ground2, (0, 665))
            self.moving_ground2(self.ground2_x, self.ground2_y, ground2)

            #            self.screenText("Flappy Bird Game", (255, 255, 255), 400, 600, 48, "Fixedsys", bold=True)

            screen.blit(train, (self.trainX, 439))

            back_button = button.Button(5, 2, back_img, 0.8)
            if back_button.draw(screen):
                flappy.main_menu()
            # go back to Menu screen

            # moving pipe
            self.moving_pipe()
            # flapping

            self.flapping()
            # game over
            self.game_over()
            # displaying score
            if self.score > 0:
                self.screen_text(str(self.score), (10, 1, 61), 600, 50, 68, "Fixedsys", bold=True)

            pygame.mixer.Sound.play(music)
            music.set_volume(0.03)

            # checking highest Score
            if highest_score < self.score:
                highest_score = self.score
            with open("highest_score.txt", "w") as f:
                f.write(str(highest_score))

            self.screen_text(f"Highest Score {highest_score}", red, width - 200, 10, size=20, style="Calibri")

            pygame.display.update()

            clock.tick(fps)

            if not self.is_game_over:
                self.background_x_vel = 1
                # moving background
                self.background_x += -self.background_x_vel
                if self.background_x <= -width:
                    self.background_x = 0

                self.ground2_x_vel = 6
                self.ground2_x += -self.ground2_x_vel
                if self.ground2_x <= -width:
                    self.ground2_x = 0


class Menu:
    def __init__(self):
        pass

    def main_menu(self):

        # create MENU display window
        screen_height = 720
        screen_width = 1280

        self.menuscreen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Flappy Bird Game')

        # load button images
        start_img = pygame.image.load('images/start_btn.png').convert_alpha()
        exit_img = pygame.image.load('images/exit_btn.png').convert_alpha()

        # create button instances
        self.start_button = button.Button(500, 300, start_img, 0.8)
        self.exit_button = button.Button(500, 450, exit_img, 0.8)

        # game loop
        run = True
        while run:

            self.menuscreen.blit(background, (0, 0))
            self.menuscreen.blit(ground1, (100, 235))
            self.menuscreen.blit(ground2, (0, 665))


            self.menufont = pygame.font.SysFont("Fixedsys", 60, bold=True)
            screen_text1 = self.menufont.render("Flappy Bird Game", True, (0, 0, 0))
            screen.blit(screen_text1, (380, 100))

            if self.start_button.draw(self.menuscreen):
                flappy_bird = Game()
                flappy_bird.main_game()

            if self.exit_button.draw(self.menuscreen):
                pygame.quit()
                sys.exit()

            # event handler

            for event in pygame.event.get():

                # quit game

                if event.type == pygame.QUIT:
                    run = False

            pygame.display.update()

        pygame.quit()


flappy = Menu()
flappy.main_menu()
