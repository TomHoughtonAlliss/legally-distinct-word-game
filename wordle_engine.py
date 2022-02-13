import random
import copy

with open("words", "r") as f:
    words = [line.rstrip("\n\r") for line in f.readlines()]


class Wordle:
    def __init__(self):
        self.word = random.choice(words)
        self.current_guess = 0
        self.number_of_guesses = 0

    def get_guess_results(self, guess):
        self.number_of_guesses += 1

        if guess == self.word:
            return [2 for _ in range(len(self.word))], True

        temp_word = copy.copy(self.word)

        correct_place = [0 for _ in range(len(self.word))]
        word_contains = []
        for i in range(len(temp_word)):
            if guess[i] == temp_word[i]:
                correct_place[i] = 2
                temp_word = list(temp_word)
                temp_word[i] = "_"
                temp_word = ''.join(temp_word)
            else:
                if guess[i] in temp_word:
                    correct_place[i] = 1
                    temp_word = list(temp_word)
                    temp_word[temp_word.index(guess[i])] = "_"
                    temp_word = ''.join(temp_word)

        return correct_place, False

    def check_if_valid_guess(self, guess):
        state = guess in words
        return state
