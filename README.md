# Wordle-Solver

This repository contains an interactive Wordle helper written in Python. The solver assists you in finding the best guess by filtering a list of candidate words based on feedback from Wordle. It uses a simple, naive approach to score potential guesses by simulating the worst-case scenario for each guess. The attached list is a list of German words but can be replaced by any other file named wordlist.txt

## Features

- **Interactive Session:** Enter a starting word and, after each guess, input the feedback you receive (using `g` for green, `y` for yellow, and `b` for black/gray).
- **Feedback Processing:** The program accurately computes feedback for each guess (handling repeated letters correctly).
- **Candidate Filtering:** It narrows down the list of possible answers based on the provided feedback.
- **Best Guess Suggestion:** Suggests the next best guess by choosing the word with the smallest worst-case partition size.
- **Simple Setup:** No external dependencies—just Python 3 and a word list.

## Files

- **`main.py`**: The main Python script.
- **`wordlist.txt`**: A text file containing a list of German 5-letter words (one word per line).

## Requirements

- Python 3.6 or above

## Usage

1. **Prepare the Word List:**

   Make sure you have a `wordlist.txt` file in the repository’s root directory. Each line should contain a single 5-letter word.
   

2. **Follow the On-Screen Prompts:**

   - **Enter a starting word:**  
     The solver will prompt you to enter a 5-letter starting word.
   
   - **Provide Feedback:**  
     After trying the word on Wordle, input the feedback using letters:
     - `g` for a correct letter in the correct position (green)
     - `y` for a correct letter in the wrong position (yellow)
     - `b` for a letter that is not in the word (black/gray)
   
     **Example:**  
     If your feedback is "green, green, yellow, black, yellow", type:  
     ```
     ggyby
     ```

   - The solver will display the remaining number of candidate words and suggest your next guess.

   - The process repeats until you solve the puzzle (when you input `ggggg`).
  

## Code Overview

Below is a summary of the main functions:

- **`get_feedback(guess, answer)`**  
  Computes the feedback string (e.g., `"ggyby"`) for a given guess compared to the answer.

- **`filter_candidates(candidates, guess, feedback)`**  
  Filters the set of candidate words to only those that would produce the same feedback when compared to the guess.

- **`score_guess_naively(guess, candidates)`**  
  Simulates all possible feedback outcomes for a guess and returns the size of the worst-case candidate partition.

- **`best_next_guess(candidates, words)`**  
  Iterates through the full word list to determine the best next guess based on the worst-case scenario.

- **`interactive_solver(words)`**  
  Runs the interactive loop that:
  1. Prompts for a starting word.
  2. Accepts feedback after each guess.
  3. Filters candidates and suggests the next guess.

## Example Session


   - ![Wordle Solver Screenshot](wordle1.jpg)
   - ![Wordle Solver Screenshot](wordle2.jpg)


## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests if you have suggestions or improvements.
