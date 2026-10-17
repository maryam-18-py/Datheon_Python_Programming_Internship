import random
from pathlib import Path

MAX_ATTEMPTS = 6

HANGMAN_STAGES = [
    r"""
     +---+
     |   |
         |
         |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
         |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|\  |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|\  |
    /    |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|\  |
    / \  |
         |
    =========
    """
]


def load_words():
    """Load suitable words from the supplied word list."""
    word_file = Path(__file__).with_name("google-10000-english-no-swears.txt")

    if word_file.exists():
        with word_file.open("r", encoding="utf-8") as file:
            words = [
                line.strip().lower()
                for line in file
                if line.strip().isalpha() and 4 <= len(line.strip()) <= 10
            ]
        if words:
            return words

    # Fallback words let the game run even without the text file.
    return [
        "python", "computer", "software", "hangman",
        "keyboard", "program", "student", "developer"
    ]


def play_game():
    """Run one round of Hangman."""
    secret_word = random.choice(load_words()).upper()
    guessed_letters = set()
    wrong_guesses = 0

    print("=" * 35)
    print("          PYTHON HANGMAN")
    print("=" * 35)
    print(f"Guess the hidden word one letter at a time. You have {MAX_ATTEMPTS} incorrect guesses.")

    while wrong_guesses < MAX_ATTEMPTS:
        masked_word = " ".join(
            letter if letter in guessed_letters else "_"
            for letter in secret_word
        )

        print(HANGMAN_STAGES[wrong_guesses])
        print("Word:", masked_word)
        print("Guessed letters:", " ".join(sorted(guessed_letters)) or "None")
        print(f"Incorrect guesses: {wrong_guesses}/{MAX_ATTEMPTS}")

        if all(letter in guessed_letters for letter in secret_word):
            print(f"\nCongratulations! You won. The word was {secret_word}.")
            return

        guess = input("\nEnter one letter: ").strip().upper()

        if len(guess) != 1 or not guess.isalpha():
            print("Invalid input. Please enter a single letter (A-Z).")
            continue

        if guess in guessed_letters:
            print(f"You already guessed '{guess}'. No attempt was lost.")
            continue

        guessed_letters.add(guess)

        if guess in secret_word:
            print("Correct! That letter is in the word.")
        else:
            wrong_guesses += 1
            print("Sorry, that letter is not in the word.")

    print(HANGMAN_STAGES[wrong_guesses])
    print("Word:", " ".join(secret_word))
    print(f"\nGame over! The word was {secret_word}.")


if __name__ == "__main__":
    play_game()
