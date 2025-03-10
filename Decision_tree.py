import json
import math
from collections import Counter


class Decision_tree:
    def __init__(self, question=None, yes=None, no=None, is_leaf=False, answer=None):
        self.question = question
        self.yes = yes
        self.no = no
        self.is_leaf = is_leaf
        self.answer = answer

    def print_tree(self, indent=""):

        if self.is_leaf:
            print(f"{indent}Leaf: {self.answer}")
        else:
            print(f"{indent}Question: {self.question}")
            print(f"{indent}  --> Yes:")
            if self.yes:
                self.yes.print_tree(indent + "    ")
            print(f"{indent}  --> No:")
            if self.no:
                self.no.print_tree(indent + "    ")


def load_movies_from_json(filepath):

    with open(filepath, 'r') as file:
        movies = json.load(file)
        for movie in movies:
            movie['genre'] = movie.get('genre', [])
            movie['release_year'] = movie.get('release_year', "Unknown")
            movie['actors'] = movie.get('actors', [])
        return movies


def entropy(movies):

    total = len(movies)
    if total == 0:
        return 0

    counts = Counter(movie['title'] for movie in movies)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


def information_gain(movies, question_type, question_value, yes_movies, no_movies):

    current_entropy = entropy(movies)
    p_yes = len(yes_movies) / len(movies)
    p_no = len(no_movies) / len(movies)
    weighted_entropy = p_yes * entropy(yes_movies) + p_no * entropy(no_movies)
    return current_entropy - weighted_entropy


def best_split(movies):

    best_gain = 0
    best_question = None
    best_question_type = None
    best_yes_movies = None
    best_no_movies = None

    # Generate all possible questions
    for movie in movies:
        for genre in movie['genre']:
            question = f"Is the movie a {genre} film?"
            yes_movies = filter_movies(movies, "genre", True, genre)
            no_movies = filter_movies(movies, "genre", False, genre)
            gain = information_gain(movies, "genre", genre, yes_movies, no_movies)
            if gain > best_gain:
                best_gain, best_question, best_question_type = gain, question, "genre"
                best_yes_movies, best_no_movies = yes_movies, no_movies

        # Add other question types (e.g., release_year, actors)
        if movie['release_year'].isdigit():  # Skip "Unknown" release years
            year_question = f"Was the movie released after {movie['release_year']}?"
            yes_movies = filter_movies(movies, "release_year", True, movie['release_year'])
            no_movies = filter_movies(movies, "release_year", False, movie['release_year'])
            gain = information_gain(movies, "release_year", movie['release_year'], yes_movies, no_movies)
            if gain > best_gain:
                best_gain, best_question, best_question_type = gain, year_question, "release_year"
                best_yes_movies, best_no_movies = yes_movies, no_movies

        for actor in movie['actors']:
            actor_question = f"Does the movie star {actor}?"
            yes_movies = filter_movies(movies, "actor", True, actor)
            no_movies = filter_movies(movies, "actor", False, actor)
            gain = information_gain(movies, "actor", actor, yes_movies, no_movies)
            if gain > best_gain:
                best_gain, best_question, best_question_type = gain, actor_question, "actor"
                best_yes_movies, best_no_movies = yes_movies, no_movies

    return best_question, best_question_type, best_yes_movies, best_no_movies


def build_id3_tree(movies, depth=0, max_depth=20):

    if not movies:
        return Decision_tree(is_leaf=True, answer="No movie found.")
    if len(movies) == 1 or depth >= max_depth:
        return Decision_tree(is_leaf=True, answer=movies[0]['title'])


    question, question_type, yes_movies, no_movies = best_split(movies)
    if not question or not yes_movies or not no_movies:
        return Decision_tree(is_leaf=True, answer=movies[0]['title'])


    return Decision_tree(
        question=question,
        yes=build_id3_tree(yes_movies, depth + 1, max_depth),
        no=build_id3_tree(no_movies, depth + 1, max_depth)
    )


def filter_movies(movies, question_type, answer, question_value):

    if question_type == "genre":
        return [movie for movie in movies if (question_value in movie['genre']) == answer]
    if question_type == "release_year":
        return [
            movie for movie in movies
            if movie['release_year'].isdigit() and (int(movie['release_year']) > int(question_value)) == answer
        ]
    if question_type == "actor":
        return [movie for movie in movies if (question_value in movie['actors']) == answer]
    return movies


# Example usage:
if __name__ == "__main__":
    movies = load_movies_from_json("movies.json")  # Path to your movie dataset file

    # Build the decision tree
    tree = build_id3_tree(movies)

    # Print the decision tree
    tree.print_tree()
