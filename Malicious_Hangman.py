"""
Malicious_Hangman.py
Brianna Brost
4/23/23
This code is a version of Hangman where the computer maximizes the challenge. Instead of picking a word at the start, it waits, eliminating as many words as possible based on the player’s guesses. The word is only chosen when no further eliminations can be made, making each guess a strategic challenge.
"""
import random
class Hangman:
    """
    hangman but its a bully so it doesnt choose a word until there are like no more words left after getting rid of as many letters as possible
    """
    def __init__(self, word_length, attempts_left)->None:
        """
            Description of Function: inits variables
            Parameters: word_length - number of words, attempts_left - number of guesses
            Return: None
        """
        self.word_dict = self.make_dict()
        self.words_remaining = self.word_dict[word_length]
        self.word_length = word_length
        self.attempts_left = attempts_left
        self.guesses = set()
        self.correct_guess = False
        self.word_print = " _ " * self.word_length

    def make_dict(self)->dict:
        """
            Description: makes dict of words
            Parameters: none
            Return: dict 
        """
        word_dict = {}
        with open("usaWords.txt", "r") as a_file:
            for line in a_file:
                data = line.strip().split(' ')
                word = data[0].upper()
                length = len(data[0])
                if length in word_dict:
                    word_dict[length].append(word)
                else:
                    word_dict[length] = [word]

        return word_dict

    def user_guess(self)->str:
        """
            Description of Function: prompts user to input letter
            Parameters: None
            Return: str
        """
        guess = input("Guess a letter: ").upper()
        return guess

    def check_guess(self, guess)->None:
        """
            Description of Function: checks if valid guess
            Parameters: guess - letter being guessed
            Return: None
        """
        if len(guess) == 1:
            if guess in self.guesses:
                print(f"You have already guessed the letter: {guess}")
            else:
                self.guesses.add(guess)
                self.attempts_left -= 1
        else:
            print(f"Invalid guess. Enter either one letter or a word that is {self.word_length} letters long. ")

    def play_again(self)->None:
        """
            Description of Function: ask to play again and do what is wanted 
            Parameters: None
            Return: None
        """
        restart = input("Play again? Enter YES or NO.")
        restart = restart.upper()
        while restart != "YES" or restart != "NO":
            if restart == "YES":
                lets_play()
            elif restart == "NO":
                print("Bye")
                exit()
            else:
                print("ONLY TYPE YES or NO.")
                self.play_again()

    def print_word(self)->str:
        """
            Description of Function: prints word will filled out letters
            Parameters:
                None
            Return:str
        """
        printed_word = ""
        for letter in self.words_remaining[0]:
            if letter in self.guesses:
                printed_word += letter
            else:
                printed_word += "_"
        print(printed_word)
        return printed_word

    def malicious_hangman(self)->None:
        """
            Description of Function: goes through the words to remove words with the letters if it leaves words remaining
            Parameters:None
            Return:None
        """
        while self.attempts_left > 0:
            print("Attempts remaining: ", self.attempts_left)
            self.print_word()
            guess = self.user_guess()
            self.check_guess(guess)
            word_groups = {}
            # Group words by their pattern of guessed and unguessed letters
            for word in self.words_remaining:
                key = "".join([letter if letter in self.guesses else "_" for letter in word])
                if key in word_groups:
                    word_groups[key].append(word)
                else:
                    word_groups[key] = [word]
            # If the guessed letter appears in any of the groups, remove those groups
            word_groups = {key: words for key, words in word_groups.items() if guess not in key}
            if word_groups:
                self.words_remaining = max(word_groups.values(), key = len)
            else:
                # If all groups were removed, this means the guessed letter is in all remaining words
                # In this case, choose a random word and reveal the guessed letter
                self.word = random.choice(self.words_remaining)
                self.hangman(self.word)
        if self.attempts_left == 0:
            print("You lose...")
            # Ensure the revealed word matches the correctly guessed letters
            matching_words = [word for word in self.words_remaining if all(guess in word for guess in self.guesses)]
            print("The word was:", random.choice(matching_words) if matching_words else "No matching words found")
        self.play_again()



    def hangman(self, word)->None:
        """
            Description of Function: just the normal hangman stuff
            Parameters:None
            Return:None
        """
        correct_guess = False
        while not correct_guess and self.attempts_left > 0:
            print("Number of attempts remaining: ", self.attempts_left)
            self.print_word()
            guess = self.user_guess()
            self.check_guess(guess)
            if "_" not in self.print_word():
                print(f"Yessssssssssssss you did it, you dont completely suck i guess")
                print(f"You had {self.attempts_left} attempts remaining. ")
                correct_guess = True
        if self.attempts_left == 0:
            print("You lose...")
            print("The word is:", word)
        self.play_again()

def lets_play()->None:
    """
        Description of Function: asks player for word length and attempts wanted and then plays the game
        Parameters:None
        Return:None
    """
    word_length = int(input("What length would you like the word? "))
    attempts_left = int(input("How many guesses would you like? "))
    game = Hangman(word_length, attempts_left)
    game.malicious_hangman()

lets_play()
