import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 500, 500
TILE_SIZE = 50
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Player:
    def __init__(self, name):
        self.name = name
        self.gpa = 3.00

        # Ensure GPA does not exceed 4.00
        self.gpa = min(self.gpa, 4.50)

class FSM:
    def __init__(self, initial_state):
        # Dictionary (input_symbol, current_state) --> (action, next_state).
        self.state_transitions = {}
        self.current_state = initial_state

    def add_transition(self, input_symbol, state, action=None, next_state=None):
        if next_state is not None:
            self.state_transitions[(input_symbol, state)] = (action, next_state)
        else:
            self.state_transitions[(input_symbol, state)] = (action, state)

    def get_transition(self, input_symbol, state):
        return self.state_transitions[(input_symbol, state)]

    def process(self, input_symbol):
        update = self.get_transition(input_symbol, self.current_state)
        if update[0] is not None:
            update[0]()
        self.current_state = update[1]

class NPC:
    UP, DOWN, LEFT, RIGHT = "u", "d", "l", "r"
    TIMER_UP = "tu"
    DIRECTIONS = {UP: "npc_up.png", DOWN: "npc_down.png", LEFT: "npc_left.png", RIGHT: "npc_right.png"}

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.directions = list(self.DIRECTIONS.keys())
        self.direction = random.choice(self.directions)
        self.fsm = FSM(self.DOWN)
        self.init_fsm()

    def init_fsm(self):
        self.fsm.add_transition(self.TIMER_UP, self.DOWN, self.turn_LEFT, self.LEFT)
        self.fsm.add_transition(self.TIMER_UP, self.LEFT, self.turn_UP, self.UP)
        self.fsm.add_transition(self.TIMER_UP, self.UP, self.turn_RIGHT, self.RIGHT)
        self.fsm.add_transition(self.TIMER_UP, self.RIGHT, self.turn_DOWN, self.DOWN)

    def turn_UP(self):
        self.direction = self.UP

    def turn_DOWN(self):
        self.direction = self.DOWN

    def turn_LEFT(self):
        self.direction = self.LEFT

    def turn_RIGHT(self):
        self.direction = self.RIGHT

class PokemonGame:
    def __init__(self):
        pygame.init()

        self.forest_map = [
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 0, 0, 1],
            [1, 0, 0, 0, 1, 1, 1, 0, 0, 1],
            [1, 1, 0, 1, 0, 0, 1, 0, 0, 1],
            [1, 1, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 1, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        self.player = Player("Ash")
        self.npc = NPC(8, 6)
        self.question_initiated = False
        # Font for displaying text
        self.font = pygame.font.Font(None, 25)

        # Question and answer data
        self.question_data = {
            "question": "If D has spatial coordinates of 12 years and b has time coordinates of 40 years and Event A has time coordinates of 16 years, what is the age of Eddie when they meet up? Assume they are both 18 years old at the origin (event 0)",
            "answers": ["51.23", "49.36", "47.85", "58"],
            "correct_answer": "49.36"
        }


        # Create the game window
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pokemon Forest")

        # Set initial player position
        self.player_x, self.player_y = 2, 9

        # NPC behavior - Change direction every 5 seconds
        self.npc_last_change_time = pygame.time.get_ticks()
        self.npc_change_interval = 1000  # Change direction every second
        self.npc_engage_distance = 1

        # Load and resize player and NPC character images
        self.player_image = pygame.image.load("player.png")  # Replace with your player image
        self.player_image = pygame.transform.scale(self.player_image, (TILE_SIZE, TILE_SIZE))

        self.npc_images = {direction: pygame.transform.scale(pygame.image.load(image_path), (TILE_SIZE, TILE_SIZE))
                           for direction, image_path in self.npc.DIRECTIONS.items()}
        self.tree_image = pygame.transform.scale(pygame.image.load("tree.png"), (TILE_SIZE, TILE_SIZE))


    def display_gpa(self):
        gpa_text = self.font.render(f"GPA: {self.player.gpa:.2f}", True, (237, 97, 255))
        self.screen.blit(gpa_text, (WIDTH - 150, HEIGHT - 30))

    def question_sequence(self):
        # Function to handle the question sequence

        # Create a new Pygame window for the question
        question_screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Question Time")

        # Draw a blank white background
        question_screen.fill(WHITE)

        # Display feedback text
        feedback_text = self.font.render("", True, (0, 0, 0))  # Initialize feedback text

        # Display question and answers
        question_text = self.font.render(self.question_data["question"], True, (0, 0, 0))

        # Calculate the number of lines needed for the question
        question_lines = self.calculate_wrapped_text(self.question_data["question"], self.font, WIDTH - 40)

        # Render each line of the question
        for i, line in enumerate(question_lines):
            line_text = self.font.render(line, True, (0, 0, 0))
            question_screen.blit(line_text, (20, HEIGHT // 2 - 100 + i * 30))

        # Display answer texts
        answer_texts = []
        for i, answer in enumerate(self.question_data["answers"]):
            answer_text = self.font.render(f"{i + 1}. {answer}", True, (0, 0, 0))
            answer_texts.append(answer_text)
            question_screen.blit(answer_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50 + len(question_lines) * 30 + i * 30))

        pygame.display.flip()

        # Wait for player input
        selected_answer = None
        while selected_answer is None:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if pygame.K_1 <= event.key <= pygame.K_4:
                        answers = self.question_data["answers"]
                        selected_answer = answers[int(event.key - pygame.K_1)]
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            # Check the selected answer
            if selected_answer is not None:
                correct_answer = self.question_data["correct_answer"]
                if selected_answer == correct_answer:
                    feedback_text = self.font.render("Correct!", True, (0, 255, 0))
                    # Handle correct answer
                    self.player.gpa += 1.00
                else:
                    feedback_text = self.font.render("Incorrect!", True, (255, 0, 0))
                    # Handle incorrect answer
                    self.player.gpa -= 1.00

                # Display feedback text at the top
                question_screen.blit(feedback_text, (WIDTH // 2 - 50, 20))

                # Display player's updated GPA in the bottom right corner
                self.display_gpa()

                pygame.display.flip()

                # Wait for a moment to display feedback
                pygame.time.delay(2000)

                # Reset to the original Pokemon Forest screen
                break



    def calculate_wrapped_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            if font.size(' '.join(current_line + [word]))[0] <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]

        lines.append(' '.join(current_line))
        return lines
    
    def college_submission_sequence(self):
        # Create a new Pygame window for the college submission
        submission_screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("College Submission")

        # Draw a blank white background
        submission_screen.fill(WHITE)

        # Display submission prompt
        prompt_text = self.font.render("Are you ready to submit? (Press Enter to submit, Esc to return to the game)", True, (0, 0, 0))
        submission_screen.blit(prompt_text, (WIDTH // 2 - 250, HEIGHT // 2 - 30))

        pygame.display.flip()

        # Wait for player input
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Check GPA for college acceptance
                        if self.player.gpa >= 3.8:
                            message_text = self.font.render("You got into college!", True, (0, 255, 0))
                        else:
                            message_text = self.font.render("Sorry, try again next year.", True, (255, 0, 0))
                        
                        # Display the acceptance message
                        submission_screen.fill(WHITE)
                        submission_screen.blit(message_text, (WIDTH // 2 - 150, HEIGHT // 2 - 30))
                        pygame.display.flip()

                        # Wait for a moment to display the message
                        pygame.time.delay(2000)

                        # Return to the original Pokemon Forest screen
                        return
                    elif event.key == pygame.K_ESCAPE:
                        # Return to the game
                        return

    def run_game(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(10)  # Adjust the speed of the game

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Player movement
            keys = pygame.key.get_pressed()
            next_x, next_y = self.player_x, self.player_y

            if keys[pygame.K_LEFT]:
                next_x -= 1
            elif keys[pygame.K_RIGHT]:
                next_x += 1
            elif keys[pygame.K_UP]:
                next_y -= 1
            elif keys[pygame.K_DOWN]:
                next_y += 1

            # Check if the next position is valid (not occupied by the NPC or a tree)
            if self.forest_map[next_y][next_x] == 0 and (next_x != self.npc.x or next_y != self.npc.y):
                self.player_x, self.player_y = next_x, next_y

            # NPC behavior - Change direction every 5 seconds
            current_time = pygame.time.get_ticks()
            if current_time - self.npc_last_change_time >= self.npc_change_interval:
                self.npc_last_change_time = current_time
                self.npc.fsm.process(self.npc.TIMER_UP)

            if not self.question_initiated:
                if self.npc.x == self.player_x:
                    if self.npc.y < self.player_y:
                        self.npc.direction = self.npc.DOWN
                    elif self.npc.y > self.player_y:
                        self.npc.direction = self.npc.UP
                elif self.npc.y == self.player_y:
                    if self.npc.x < self.player_x:
                        self.npc.direction = self.npc.RIGHT
                    elif self.npc.x > self.player_x:
                        self.npc.direction = self.npc.LEFT

                if (self.npc.x - self.npc_engage_distance <= self.player_x <= self.npc.x + self.npc_engage_distance
                        and self.npc.y - self.npc_engage_distance <= self.player_y <= self.npc.y + self.npc_engage_distance):
                    # Engage in a question sequence
                    self.question_initiated = True
                    self.question_sequence()

            # Draw background
            self.screen.fill(GREEN)

            # Draw forest map
            for y, row in enumerate(self.forest_map):
                for x, tile in enumerate(row):
                    if tile == 1:
                        self.screen.blit(self.tree_image, (x * TILE_SIZE, y * TILE_SIZE))


            # Draw player character
            self.screen.blit(self.player_image, (self.player_x * TILE_SIZE, self.player_y * TILE_SIZE))

            # Draw NPC character
            npc_image = self.npc_images[self.npc.direction]
            self.screen.blit(npc_image, (self.npc.x * TILE_SIZE, self.npc.y * TILE_SIZE))

            # Display player's GPA in the bottom right corner
            self.display_gpa()

            # Update display
            pygame.display.flip()

        pygame.quit()
        sys.exit()

# Run the game
game = PokemonGame()
game.run_game()
