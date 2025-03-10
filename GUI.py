import os 
import urllib
import requests
import pygame
from Decision_tree import load_movies_from_json, build_id3_tree, Decision_tree

pygame.init()
TMDB_API_KEY = os.getenv("API_KEY")
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Movie Guessing Game")
BACKGROUND_IMAGE_PATH = "Resources/images.jpg"
background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

BACKGROUND = (18, 18, 24)  # Darker blue-black
BUTTON_COLOR = (45, 45, 55)  # Deep slate
BUTTON_HOVER_COLOR = (75, 75, 85)  # Lighter slate
TEXT_COLOR = (229, 229, 229)  # Soft white
HIGHLIGHT_COLOR = (255, 215, 0)  # Golden yellow for movie-theme emphasis


SECONDARY_ACCENT = (138, 43, 226)  # Deep purple for special elements
SUCCESS_COLOR = (46, 139, 87)  # Sea green for success messages
ERROR_COLOR = (178, 34, 34)  # Firebrick red for error messages


FONT_PATH = "Resources/PlayfairDisplay-VariableFont_wght.ttf"
FONT_LARGE = pygame.font.Font(FONT_PATH, 48)
FONT_MEDIUM = pygame.font.Font(FONT_PATH, 36)
FONT_SMALL = pygame.font.Font(FONT_PATH, 24)


class GUI():
    def __init__(self, x, y, width, height, text, color, hover_color, text_color, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = font

    def draw(self, screen):
        current_color = self.hover_color if self.is_hovered() else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())


def fetch_movie_poster(movie_title, api_key):
    base_url = "https://api.themoviedb.org/3"
    search_endpoint = f"{base_url}/search/movie"
    image_base_url = "https://image.tmdb.org/t/p/w500"

    params = {
        "api_key": api_key,
        "query": movie_title,
    }
    response = requests.get(search_endpoint, params=params)
    if response.status_code == 200:
        results = response.json().get("results")
        if results:
            poster_path = results[0].get("poster_path")
            if poster_path:
                return f"{image_base_url}{poster_path}"
    return None


def load_image_from_url(url):
    image_path = "temp_poster.jpg"
    urllib.request.urlretrieve(url, image_path)
    return pygame.image.load(image_path)


def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


def main():
    filepath = "movies.json"
    movies = load_movies_from_json(filepath)
    decision_tree = build_id3_tree(movies)

    current_node = decision_tree
    game_state = "start"
    user_input = ""

    yes_button = GUI(WIDTH // 2 - 110, HEIGHT - 180, 100, 50, "Yes", BUTTON_COLOR, BUTTON_HOVER_COLOR, TEXT_COLOR,
                     FONT_MEDIUM)
    no_button = GUI(WIDTH // 2 + 10, HEIGHT - 180, 100, 50, "No", BUTTON_COLOR, BUTTON_HOVER_COLOR, TEXT_COLOR,
                    FONT_MEDIUM)
    try_again_button = GUI(WIDTH // 2 - 120, HEIGHT - 150, 100, 50, "Try Again", BUTTON_COLOR, BUTTON_HOVER_COLOR,
                           TEXT_COLOR, FONT_SMALL)
    exit_button = GUI(WIDTH // 2 + 20, HEIGHT - 150, 100, 50, "Exit", BUTTON_COLOR, BUTTON_HOVER_COLOR, TEXT_COLOR,
                      FONT_MEDIUM)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_state in ["question", "guess"]:
                    if yes_button.is_hovered():
                        user_input = "yes"
                    elif no_button.is_hovered():
                        user_input = "no"
                elif game_state == "start":
                    if yes_button.is_hovered():
                        game_state = "question"
                        current_node = decision_tree
                    elif no_button.is_hovered():
                        running = False
                elif game_state in ["success", "failure"]:
                    if try_again_button.is_hovered():
                        game_state = "start"
                        current_node = decision_tree
                    elif exit_button.is_hovered():
                        running = False

        screen.blit(background_image, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        if game_state == "start":
            question_counter = 0  # Reset counter when game starts
            draw_text(screen, "Movie Guessing Game", FONT_LARGE, HIGHLIGHT_COLOR, WIDTH // 2, 100)
            draw_text(screen, "Think of a movie and I'll try to guess it!", FONT_MEDIUM, TEXT_COLOR, WIDTH // 2, 200)
            draw_text(screen, "Are you ready to play?", FONT_MEDIUM, TEXT_COLOR, WIDTH // 2, 300)
            yes_button.draw(screen)
            no_button.draw(screen)

        elif game_state == "question":
            # Display question counter
            draw_text(screen, f"Question {question_counter + 1}", FONT_SMALL, SECONDARY_ACCENT, WIDTH // 2, 100)
            draw_text(screen, current_node.question, FONT_MEDIUM, TEXT_COLOR, WIDTH // 2, 200)
            yes_button.draw(screen)
            no_button.draw(screen)

            if user_input:
                question_counter += 1  # Increment counter when user answers
                current_node = current_node.yes if user_input == "yes" else current_node.no
                user_input = ""

                if current_node.is_leaf:
                    game_state = "guess"

        elif game_state == "guess":
            # Display final question count
            draw_text(screen, f"After {question_counter} questions...", FONT_SMALL, SECONDARY_ACCENT, WIDTH // 2, 100)
            draw_text(screen, f"Is the movie '{current_node.answer}'?", FONT_MEDIUM, TEXT_COLOR, WIDTH // 2, 200)
            poster_url = fetch_movie_poster(current_node.answer, TMDB_API_KEY)
            if poster_url:
                poster_image = load_image_from_url(poster_url)
                poster_image = pygame.transform.scale(poster_image, (200, 300))
                screen.blit(poster_image, (WIDTH // 2 - 100, HEIGHT // 2 - 120))
            yes_button.draw(screen)
            no_button.draw(screen)

            if user_input:
                if user_input == "yes":
                    game_state = "success"
                elif user_input == "no":
                    game_state = "failure"
                user_input = ""

        elif game_state == "success":
            draw_text(screen, f"Yay, I guessed it in {question_counter} questions!",
                      FONT_MEDIUM, SUCCESS_COLOR, WIDTH // 2, 200)
            try_again_button.draw(screen)
            exit_button.draw(screen)

        elif game_state == "failure":
            draw_text(screen, f"Sorry! I couldn't guess after {question_counter} questions",
                      FONT_MEDIUM, ERROR_COLOR, WIDTH // 2, 200)
            try_again_button.draw(screen)
            exit_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def cleanup_temp_files():
    if os.path.exists("temp_poster.jpg"):
        os.remove("temp_poster.jpg")


if __name__ == "__main__":
    try:
        main()
    finally:
        cleanup_temp_files()