def get_feedback(guess, answer):
    """
    Given a guess and the answer, compute the Wordle feedback.
    'g' = correct letter in correct place (green)
    'y' = correct letter in wrong place (yellow)
    'b' = letter not in the word (black/gray)
    This function handles repeated letters properly.
    """
    feedback = ['b'] * len(guess)
    answer_chars = list(answer)
    # First pass: mark greens and mark those letters as used.
    for i in range(len(guess)):
        if guess[i] == answer[i]:
            feedback[i] = 'g'
            answer_chars[i] = None  # Mark as used.
    # Second pass: mark yellows.
    for i in range(len(guess)):
        if feedback[i] == 'b' and guess[i] in answer_chars:
            feedback[i] = 'y'
            answer_chars[answer_chars.index(guess[i])] = None  # Mark that occurrence as used.
    return "".join(feedback)


def filter_candidates(candidates, guess, feedback):
    """
    Filters the candidate set to only those words that would yield the same
    feedback if 'guess' were applied.
    """
    return {word for word in candidates if get_feedback(guess, word) == feedback}


def score_guess_naively(guess, candidates):
    """
    Computes the worst-case partition size for a given guess by simulating all feedbacks.
    """
    partition = {}
    for candidate in candidates:
        fb = get_feedback(guess, candidate)
        partition[fb] = partition.get(fb, 0) + 1
    return max(partition.values()) if partition else 0


def best_next_guess(candidates, words, attempt):
    """
    For each possible guess, compute the worst-case candidate count if that guess is made.

    Normally, if there are 3 or fewer candidates, one might restrict the search to just those candidates.
    However, if there are exactly 3 candidates, the current attempt is less than 6, and the best guess
    from the candidate set yields a worst-case partition size of 2, then we try to find a guess outside the
    candidate set that yields a worst-case partition size of 1.
    """
    # Normally, if candidates are small, restrict search to candidates.
    # But if exactly 3 remain and we are early in the game, search among all words.
    if len(candidates) == 3 and attempt < 6:
        search_set = words
    elif len(candidates) <= 3:
        search_set = candidates
    else:
        search_set = words

    best_score = float('inf')
    best_word = None
    for word in search_set:
        score = score_guess_naively(word, candidates)
        if score < best_score:
            best_score = score
            best_word = word

    # If conditions are met, try to find a guess outside the candidate set that yields a better score.
    if attempt < 6 and len(candidates) == 3 and best_score == 2 and best_word in candidates:
        for word in words:
            if word in candidates:
                continue
            score = score_guess_naively(word, candidates)
            if score == 1:
                best_word = word
                best_score = 1
                break

    return best_word, best_score


def interactive_solver(words):
    """
    Runs an interactive Wordle helper:
      - You enter a starting word (validated against the word list).
      - Then, after trying it on Wordle, you enter the feedback (e.g. "ggyby").
      - The script filters the candidate list and suggests the next guess.
    """
    # Start with all words as possible answers.
    candidates = set(words)

    # Loop until a valid starting word (present in the list) is entered.
    while True:
        starting_word = input("Enter a 5-letter starting word: ").strip().lower()
        if starting_word not in words:
            print("Error: Starting word is not in the word list. Please try again.")
        else:
            break

    current_guess = starting_word
    attempt = 1

    while True:
        print(f"\nAttempt {attempt}: Try the word '{current_guess}'")
        # Loop until valid feedback is entered.
        while True:
            feedback = input("Enter feedback g(reen), y(ellow), b(lack), e.g. ggyby: ").strip().lower()
            if len(feedback) != 5:
                print("Error: Feedback must be exactly 5 characters long. Please try again.")
                continue
            if any(ch not in "gyb" for ch in feedback):
                print("Error: Feedback must only contain the letters 'g', 'y', or 'b'. Please try again.")
                continue
            break

        if feedback == "ggggg":
            print("Congratulations! The word has been solved.")
            break

        # Filter candidate words based on the feedback.
        candidates = filter_candidates(candidates, current_guess, feedback)
        print(f"Remaining candidates: {len(candidates)}")
        if len(candidates) < 20:
            print("Candidates:", ", ".join(sorted(candidates)))
        if not candidates:
            print("No candidates remaining. (Did you enter the feedback correctly?)")
            break

        # If there's only one candidate left, choose it directly.
        if len(candidates) == 1:
            current_guess = next(iter(candidates))
            print(f"Only one candidate left: '{current_guess}'.")
        else:
            current_guess, worst_case = best_next_guess(candidates, words, attempt)
            print(f"Suggested next guess: '{current_guess}' (worst-case partition size: {worst_case})")
        attempt += 1


if __name__ == '__main__':
    # Load the word list (assuming one 5-letter word per line).
    try:
        with open("wordlist.txt", "r", encoding="utf-8") as f:
            words = [line.strip().lower() for line in f if len(line.strip()) == 5]
        print(f"Loaded {len(words)} words from 'wordlist.txt'.")
    except FileNotFoundError:
        print("Error: 'wordlist.txt' not found.")
        exit(1)

    interactive_solver(words)
