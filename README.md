# CineGuess - Movie Guessing AI

CineGuess is an interactive game that guesses the movie you are thinking of by asking a series of yes/no questions. It uses a decision tree algorithm to narrow down movie choices and fetches movie data from the TMDB API.

## Features
- **Decision Tree Algorithm**: The game uses a decision tree to guess movies efficiently.
- **TMDB API Integration**: Fetches movie data dynamically to keep the database updated.
- **User-Friendly Questions**: The game asks intuitive yes/no questions to determine the movie.
- **Expandable Movie Database**: Automatically updates with new movies using TMDB API.
- **Fast and Efficient**: Uses machine learning techniques for quick and accurate predictions.

## How It Works
1. The user thinks of a movie.
2. The system asks a series of yes/no questions.
3. The decision tree processes answers to narrow down choices.
4. The system predicts the movie.
5. If incorrect, the user can provide feedback to improve future guesses.

## Installation
### Prerequisites
- Python 3.x
- TMDB API Key

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/AbdulRafay819/CineGuess.git
   cd CineGuess
   ```
2. Set up your TMDB API key in a `.env` file:
   ```sh
   TMDB_API_KEY=your_api_key_here
   ```
3. Run the game:
   ```sh
   python main.py
   ```

## Technologies Used
- **Python**: Core programming language
- **Decision Tree Algorithm**: For guessing movies
- **TMDB API**: Fetches movie data
- **SQLite (optional)**: To store past guesses and improve accuracy

## Future Improvements
- **Enhance Question Logic**: Improve the decision tree for better accuracy.
- **Add More Question Types**: Support more than just yes/no questions.
- **Web Interface**: Create a web-based version using Flask or Django.
- **Multiplayer Mode**: Allow multiple users to play together.

## Contribution
Contributions are welcome! If you find bugs or have suggestions, feel free to create an issue or submit a pull request.



## Contact
For any inquiries, reach out via email or open an issue on GitHub.

