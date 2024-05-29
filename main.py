# Import necessary modules and classes
import sys
import pygame
from pygame.locals import *
from buttons import Button
from gameConstants import *
from scores import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from fruit import Fruit
from pauser import Pause
from text import TextGroup
from sprites import LifeSprites
from sprites import MazeSprites
from mazedata import MazeData


# GameController class responsible for managing the game state and flow
class GameController(object):
    def __init__(self):
        # Initialize pygame
        pygame.init()
        # Add this line at the beginning of your script
        pygame.mixer.init()
        # Create the game window
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        print(SCREENSIZE)
        # Background surfaces for normal and flashing states
        self.background = None
        self.background_norm = None
        self.background_flash = None
        # Game clock for controlling frame rate
        self.clock = pygame.time.Clock()
        # Initialize game entities and variables
        self.fruit = None
        self.pause = Pause(True)
        self.level = 0
        self.lives = 3
        self.score = 0
        self.textgroup = TextGroup()
        self.lifesprites = LifeSprites(self.lives)
        self.flashBG = False
        self.flashTime = 0.2
        self.flashTimer = 0
        self.fruitCaptured = []
        self.fruitNode = None
        self.mazedata = MazeData()
        self.lastEatTime = 0
        self.minSoundPlay = 0.17
        self.pacmanMunchSound = pygame.mixer.Sound(
            "assets/sounds/pacman_chomp.mp3")
        self.pacmanEatGhost = pygame.mixer.Sound(
            "assets/sounds/pacman_eatghost.wav")
        self.pacmanDies = pygame.mixer.Sound(
            "assets/sounds/pacman_death.wav")
        self.topScores = loadTopScores()
        self.pacmanBeginningSound = pygame.mixer.Sound(
            "assets/sounds/pacman_beginning.wav")
        self.leaderBoardSound = pygame.mixer.Sound(
            "assets/sounds/leaderBoard.mp3")
        self.pacmanBeginningSound.play()

    def mainMenu(self):
        pygame.display.set_caption("Main Menu")
        self.bg = pygame.image.load("assets/mainMenu.jpg")

        while True:
            self.screen.blit(self.bg, (0, 0))
            mouse_pos = pygame.mouse.get_pos()

            # Display main menu text
            menu_text = pygame.font.Font("assets/PressStart2P-Regular.ttf", 32).render(
                "MAIN MENU", True, "#b68f40"
            )
            menu_rect = menu_text.get_rect(
                center=(SCREENWIDTH//2, SCREENHEIGHT//2 - 115)
            )

            # Create play, leaderboard, and quit buttons
            playButton = Button(
                btnImage=pygame.image.load("assets/play.png"),
                pos=(SCREENWIDTH // 2, SCREENHEIGHT//2 - 50),
                btnTxtInput="PLAY", btnFont=pygame.font.Font("assets/PressStart2P-Regular.ttf", 24),
                btnColor="#dfffdb", hovering_color="#c9ffc4"
            )
            leaderBoard = Button(
                btnImage=pygame.image.load("assets/leaderBoard.png"),
                pos=(SCREENWIDTH // 2, SCREENHEIGHT//2 + 10),
                btnTxtInput="LEADERBOARD", btnFont=pygame.font.Font("assets/PressStart2P-Regular.ttf", 24),
                btnColor="#dfffdb", hovering_color="#c9ffc4"
            )
            quitButton = Button(
                btnImage=pygame.image.load("assets/quit.png"),
                pos=(SCREENWIDTH // 2, SCREENHEIGHT//2 + 70),
                btnTxtInput="QUIT", btnFont=pygame.font.Font("assets/PressStart2P-Regular.ttf", 24),
                btnColor="#dfffdb", hovering_color="#c9ffc4"
            )

            self.screen.blit(menu_text, menu_rect)

            # Check for button events
            for button in [playButton, leaderBoard, quitButton]:
                button.changeColor(mouse_pos)
                button.update(self.screen)

            # Check for mouse and quit events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if playButton.checkForInput(mouse_pos):
                        self.startGame()
                        while True:
                            self.update()
                    elif leaderBoard.checkForInput(mouse_pos):
                        self.leaderBoard()
                    if quitButton.checkForInput(mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
            self.clock.tick(60)

    def leaderBoard(self):
        pygame.display.set_caption("Leaderboard")
        self.bg = pygame.image.load("assets/leaderBoard.jpg")
        self.leaderBoardSound.play()

        while True:
            self.screen.blit(self.bg, (0, 0))
            mouse_pos = pygame.mouse.get_pos()

            # Display leaderboard text
            menu_text = pygame.font.Font("assets/PressStart2P-Regular.ttf", 32).render(
                "PAC MASTERS", True, "#b68f40"
            )
            menu_rect = menu_text.get_rect(
                center=(SCREENWIDTH//2, 100)
            )
            self.screen.blit(menu_text, menu_rect)

            # Render top scores
            buttonsOffset = 50
            left_margin = 180
            for i in range(5):
                leaderBoardScores = pygame.font.Font("assets/PressStart2P-Regular.ttf", 23).render(
                    f"{i+1}. {self.topScores[i]}", True, "#dfffdb"
                )
                score_rect = leaderBoardScores.get_rect(
                    topleft=(left_margin, 180 + i * buttonsOffset)
                )
                self.screen.blit(leaderBoardScores, score_rect)

            # Create and render the back button
            backButton = Button(
                btnImage=None, pos=(SCREENWIDTH // 2, SCREENHEIGHT - 100),
                btnTxtInput="BACK", btnFont=pygame.font.Font("assets/PressStart2P-Regular.ttf", 25),
                btnColor="White", hovering_color="Green"
            )
            backButton.changeColor(mouse_pos)
            backButton.update(self.screen)

            # Check for events related to the back button and quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if backButton.checkForInput(mouse_pos):
                        self.mainMenu()

            pygame.display.update()
            self.clock.tick(60)

    def gameOver(self):

        self.restartGame()
        pygame.display.set_caption("Gameover")
        self.bg = pygame.image.load("assets/gameOver.jpg")

        while True:
            self.screen.blit(self.bg, (0, 0))
            mouse_pos = pygame.mouse.get_pos()

            # Create and render the back button
            mainMenuBtn = Button(
                btnImage=None, pos=(SCREENWIDTH - 65, SCREENHEIGHT - 30),
                btnTxtInput="MENU", btnFont=pygame.font.Font("assets/PressStart2P-Regular.ttf", 21),
                btnColor="#E5C454", hovering_color="#ffbb33"
            )
            mainMenuBtn.changeColor(mouse_pos)
            mainMenuBtn.update(self.screen)

            # Create and render the back button
            playAgainBtn = Button(
                btnImage=None, pos=(127, SCREENHEIGHT - 30),
                btnTxtInput="PLAY AGAIN", btnFont=pygame.font.Font("assets/PressStart2P-Regular.ttf", 21),
                btnColor="#E5C454", hovering_color="#ffbb33"
            )
            playAgainBtn.changeColor(mouse_pos)
            playAgainBtn.update(self.screen)

            # Check for events related to the back button and quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mainMenuBtn.checkForInput(mouse_pos):
                        self.mainMenu()
                    elif playAgainBtn.checkForInput(mouse_pos):
                        self.startGame()
                        while True:
                            self.update()

            pygame.display.update()
            self.clock.tick(60)

    # Set up the game background
    def setGameBackground(self):
        # Create normal and flashing background surfaces
        self.background_norm = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_norm.fill(BLACK)
        self.background_flash = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_flash.fill(BLACK)
        # Construct background from maze data
        self.background_norm = self.mazesprites.constructBackground(
            self.background_norm, self.level % 5)
        self.background_flash = self.mazesprites.constructBackground(
            self.background_flash, 5)
        self.flashBG = False
        self.background = self.background_norm

    # Initialize the game and set up initial configurations
    def startGame(self):
        pygame.display.set_caption("Pacman")
        # Load maze data for the current level
        self.mazedata.loadMaze(self.level)
        # Create maze sprites
        self.mazesprites = MazeSprites(
            self.mazedata.obj.name+".txt", self.mazedata.obj.name+"_rotation.txt")
        # Set up the game background
        self.setGameBackground()
        # Create node group and connect portal pairs
        self.nodes = NodeGroup(self.mazedata.obj.name+".txt")
        self.mazedata.obj.setPortalPairs(self.nodes)
        self.mazedata.obj.connectHomeNodes(self.nodes)
        # Create Pacman, pellets, ghosts, and set their initial positions
        self.pacman = Pacman(self.nodes.getNodeFromTiles(
            *self.mazedata.obj.pacmanStart))
        self.pellets = PelletGroup(self.mazedata.obj.name+".txt")
        self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman)
        # Set initial positions for each ghost
        self.ghosts.pinky.setStartNode(
            self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))
        self.ghosts.inky.setStartNode(
            self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(0, 3)))
        self.ghosts.clyde.setStartNode(
            self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(4, 3)))
        self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(
            *self.mazedata.obj.addOffset(2, 3)))
        self.ghosts.blinky.setStartNode(
            self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 0)))
        # Deny access to home nodes for Pacman and ghosts
        self.nodes.denyHomeAccess(self.pacman)
        self.nodes.denyHomeAccessList(self.ghosts)
        self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)
        # Deny access to specific paths for ghosts
        self.mazedata.obj.denyGhostsAccess(self.ghosts, self.nodes)

    # Update method called every frame to update game state
    def update(self):

        # Calculate delta time
        dt = self.clock.tick(30) / 1000.0
        # Update text group, pellets, ghosts, and check various events
        self.textgroup.update(dt)
        self.pellets.update(dt)
        if not self.pause.paused:
            self.ghosts.update(dt)
            if self.fruit is not None:
                self.fruit.update(dt)
            self.checkPelletEvents()
            self.checkGhostEvents()
            self.checkFruitEvents()

        # Update Pacman if alive
        if self.pacman.alive:
            if not self.pause.paused:
                self.pacman.update(dt)
        else:
            self.pacman.update(dt)

        # Handle flashing background effect
        if self.flashBG:
            self.flashTimer += dt
            if self.flashTimer >= self.flashTime:
                self.flashTimer = 0
                # Toggle between normal and flashing background
                if self.background == self.background_norm:
                    self.background = self.background_flash
                else:
                    self.background = self.background_norm

        # Execute pause-related methods
        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        # Check for user input events
        self.checkEvents()
        # Render the game entities on the screen
        self.render()

    # Check for user input events
    def checkEvents(self):
        for event in pygame.event.get():
            # Check if the event is a quit event
            if event.type == QUIT:
                exit()
            # Check if a key is pressed down
            elif event.type == KEYDOWN:
                # Check if the pressed key is the space key
                if event.key == K_SPACE:
                    if self.pacman.alive:
                        # Set or unset the game pause based on Pacman's status
                        self.pause.setPause(playerPaused=True)
                        if not self.pause.paused:
                            # If game is unpaused, hide pause text and show entities
                            self.textgroup.hideText()
                            self.showEntities()
                        else:
                            # If game is paused, show pause text and hide entities
                            self.textgroup.showText(PAUSETXT)
                            # self.hideEntities()

                elif event.key == K_ESCAPE:
                    self.restartGame()
                    self.mainMenu()

    # Check events related to pellets being eaten

    def checkPelletEvents(self):
        # Check if Pacman has eaten a pellet
        pellet = self.pacman.eatPellets(self.pellets.pelletList)

        if pellet:

            currentTime = pygame.time.get_ticks() / 1000  # Get current time in seconds
            if currentTime - self.lastEatTime > self.minSoundPlay:
                self.pacmanMunchSound.play()  # Play the eat sound
                self.lastEatTime = currentTime  # Update the last eat time

            # Increment the number of pellets eaten and update the score
            self.pellets.numEaten += 1
            self.updateScore(pellet.points)
            # Enable ghost modes at specific pellet counts
            if self.pellets.numEaten == 30:
                self.ghosts.inky.startNode.allowAccess(RIGHT, self.ghosts.inky)
            if self.pellets.numEaten == 70:
                self.ghosts.clyde.startNode.allowAccess(
                    LEFT, self.ghosts.clyde)
            # Remove eaten pellet
            self.pellets.pelletList.remove(pellet)
            # Activate power pellet effect
            if pellet.name == POWERPELLET:
                self.ghosts.startFreight()
            # Check if all pellets are eaten and trigger next level
            if self.pellets.isEmpty():
                self.flashBG = True
                self.hideEntities()
                # Pause for a short duration and move to the next level
                self.pause.setPause(pauseTime=3, func=self.nextLevel)
    # Check events related to interactions with ghosts

    def checkGhostEvents(self):
        # Check collision between Pacman and each ghost
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                # Check if the ghost is in FREIGHT mode (eaten by Pacman)
                if ghost.mode.current is FREIGHT:
                    self.pacmanEatGhost.play()
                    # Handle ghost eaten by Pacman
                    self.pacman.visible = False
                    ghost.visible = False
                    self.updateScore(ghost.points)
                    # Display points text and update ghost points
                    self.textgroup.addText(
                        str(ghost.points), WHITE, ghost.position.x, ghost.position.y, 8, time=1)
                    self.ghosts.updatePoints()
                    # Pause for a short duration and reset ghost to spawn
                    self.pause.setPause(pauseTime=1, func=self.showEntities)
                    ghost.startSpawn()
                    self.nodes.allowHomeAccess(ghost)
                # Check if the ghost is not in SPAWN mode (normal collision)
                elif ghost.mode.current is not SPAWN:
                    # Handle Pacman collision with non-freight ghost
                    if self.pacman.alive:
                        self.pacmanDies.play()
                        self.lives -= 1
                        self.lifesprites.removeImage()
                        self.pacman.die()
                        self.ghosts.hide()
                        # Check for game over or reset level
                        if self.lives <= 0:
                            self.textgroup.showText(GAMEOVERTXT)
                            self.pause.setPause(
                                pauseTime=3, func=self.gameOver)
                        else:
                            self.pause.setPause(
                                pauseTime=3, func=self.resetLevel)

    # Check events related to fruit
    def checkFruitEvents(self):
        # Check if specific pellet counts are reached to spawn fruit
        if self.pellets.numEaten == 50 or self.pellets.numEaten == 140:
            if self.fruit is None:
                # Spawn fruit at specific pellet counts
                if self.level % 2 == 0:
                    self.fruit = Fruit(
                        self.nodes.getNodeFromTiles(9, 20), self.level)
                else:
                    self.fruit = Fruit(
                        self.nodes.getNodeFromTiles(11, 20), self.level)

        if self.fruit is not None:
            if self.pacman.collideCheck(self.fruit):
                # Handle fruit eaten by Pacman
                self.updateScore(self.fruit.points)
                self.textgroup.addText(str(
                    self.fruit.points), WHITE, self.fruit.position.x, self.fruit.position.y, 8, time=1)
                fruitCaptured = False
                for fruit in self.fruitCaptured:
                    if fruit.get_offset() == self.fruit.image.get_offset():
                        fruitCaptured = True
                        break
                if not fruitCaptured:
                    self.fruitCaptured.append(self.fruit.image)
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None

    # Show Pacman and ghosts on the screen
    def showEntities(self):
        self.pacman.visible = True
        self.ghosts.show()

    # Hide Pacman and ghosts on the screen
    def hideEntities(self):
        self.pacman.visible = False
        self.ghosts.hide()

    # Move to the next level
    def nextLevel(self):
        self.showEntities()
        self.level += 1
        self.pause.paused = True
        self.startGame()
        self.textgroup.updateLevel(self.level)

    # Restart the game
    def restartGame(self):
        if self.score > 0 and self.score > min(self.topScores):
            self.topScores.append(self.score)
            self.topScores.sort(reverse=True)
            self.topScores = self.topScores[:5]
            saveTopScores(self.topScores)

        self.lives = 3
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.startGame()
        self.score = 0
        self.textgroup.updateScore(self.score)
        self.textgroup.updateLevel(self.level)
        self.textgroup.showText(READYTXT)
        self.lifesprites.resetLives(self.lives)
        self.fruitCaptured = []

    # Reset the current level
    def resetLevel(self):
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()
        self.fruit = None
        self.textgroup.showText(READYTXT)

    # Update the current score
    def updateScore(self, points):
        self.score += points
        self.textgroup.updateScore(self.score)

    # Render all game entities on the screen
    def render(self):
        # Blit background, pellets, fruit, Pacman, ghosts, and text on the screen
        self.screen.blit(self.background, (0, 0))
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.textgroup.render(self.screen)

        # Blit player lives and captured fruit icons
        for i in range(len(self.lifesprites.images)):
            x = 10 + self.lifesprites.images[i].get_width() * i
            y = SCREENHEIGHT - self.lifesprites.images[i].get_height() - 10
            self.screen.blit(self.lifesprites.images[i], (x, y))

        for i in range(len(self.fruitCaptured)):
            x = SCREENWIDTH - self.fruitCaptured[i].get_width() * (i+1) - 10
            y = SCREENHEIGHT - self.fruitCaptured[i].get_height() - 8
            self.screen.blit(self.fruitCaptured[i], (x, y))

        # Update the display
        pygame.display.update()


if __name__ == "__main__":
    # Create an instance of GameController
    game = GameController()
    game.mainMenu()
