#!/usr/bin/python


################################################################################
#
# Created By : Egbie Anderson 
# Name Of The Program : GuessWordGame.Py 
# Created on the 09/08/2015 at 21:05:12 hrs
# This is version : 1 
#
#
# File description 
#
# A twist of the famous hang man game but without the hang man.
# Does not work in codeSkultor due to the fact it does not have urllib
################################################################################

import random
import string
from time import sleep
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import urllib

SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600


class ImageInfo(object):
    """Deals with images"""

    def __init__(self, img):
        self._img =  simplegui.load_image(img)

    def get_center(self):
        return [self._img.get_width()/2.0, self._img.get_height()/2.0]

    def get_size(self):
        return [self._img.get_width(), self._img.get_height()]

    def get_img_height(self):
        return self._img.get_height()

    def get_img_width(self):
        return self._img.get_width()

    def get_img(self):
        return self._img

class Mode(object):
    """Handles the diffuculty for the game"""

    def __init__(self, wordlist):

        self._word_dict = {}
        word_list = wordlist.split("\n")

        for word in word_list:
            len_word = len(word)
            if len_word not in self._word_dict:
                self._word_dict.setdefault(len_word, [word.strip("\n")])
            else:
                self._word_dict[len_word].append(word)


        # level of diffuculty for the game picks words of length n based on mode
        self._easy   = [num for num in xrange(4, 8)]
        self._medium = [num for num in xrange(8, 17)]
        self._hard   = [num for num in xrange(17, 22)]


    def _get_word(self, num_list):
        """check if the word length is in the dictionary"""
        while True:
            num  = random.choice(num_list)
            word = self._word_dict.get(num, False)
            if not word:
                num_list.pop(num) # remove the num from the word list as there is no word by that length
            else:
                return word

    def easy(self):
        random.shuffle(self._easy)
        return self._get_word(self._easy)
        
    def medium(self):
        random.shuffle(self._medium)
        return self._get_word(self._medium)

    def diffuculty(self):
        random.shuffle(self._hard)
        return self._get_word(self._hard)


class GuessWordGame(Mode):

    def __init__(self, game_start=False):

        # 
        self._dictionary = urllib.urlopen("https://dl.dropbox.com/s/otmc56fnpakbbdi/dictionary.txt?dl=0").read()
        # uncomment the 6 lines and comment the top line if you want to load you own dictionary words
        # try:
        #     with open( "/home/ab/Documents/MyProjects/guess_game/dictionary.txt") as f:
        #         self._dictionary = f.read()
        # except IOError:
        #     print "[!] File does not exists"
        #     exit(0)

        self._game_mode = Mode(self._dictionary)   # controls the game diffuculty
        self._dictionary = self._game_mode.easy()  # start of with the easiest level
        self._secret_word, self._available_letters = "", ""
        self._remaining_guess, self._correct_guess = 7, 0
        self._game_over, self._game_start = False, game_start
        self._used_letters = []
        random.shuffle(self._dictionary)                                   # shuffle the words
        self.__create_alphabet_list()
        self.chose_random_word()                                           # select random word
        self._word_so_far  = self._turn_word_into_dash(self._secret_word) # turn word into dash
    
    def game_mode(self, mode):
        """select the mode for the game"""

        if mode == "easy":
            self._dictionary = self._game_mode.easy()
            self.reset_game()
        elif mode == "medium":
            self._dictionary = self._game_mode.medium()
            self.reset_game()
        elif mode == "diffuculty":
            self._dictionary = self._game_mode.diffuculty()
            self.reset_game()

    def _get_secret_word(self):
        """return the secret word chosen"""
        return self._secret_word

    def _is_guess_correct(self):
        return (True if self._correct_guess == len(self._secret_word) else False)

    def _reset_guesses(self):
        """reset guess back to default"""
        self._remaining_guess = 7      # reset the remaining guess to 7

    def _reset_correct_guesses(self):
        """reset the correct guess back to default"""
        self._correct_guess = 0
    
    def __create_alphabet_list(self):
        """create alphabets for the entire game A-Z"""
        self._available_letters = [char for char in string.ascii_uppercase]
                              
    def get_available_alphabets(self):
        """return the letters available to the user"""
        return " ".join(self._available_letters)

    def _reset_available_alphabets(self):
        """reset the alphabets available the user to A-Z"""
        self.__create_alphabet_list()

    def _remove_letter(self, char):
        """remove letter from available letters"""
        self._available_letters.remove(char)


    def get_used_letters(self):
        """return the letters already used by the user"""
        return " ".join(self._used_letters)

    def _reset_used_letters(self):
        """reset the letter used by the user"""
        self._used_letters = []  

    def get_word_so_far(self):
        """returns the string containing the letters for the
        secret word that user has already guessed or not guessed
        """
        return "   ".join(self._word_so_far)

    def game_over(self):
        """return the state of the game"""
        return self._game_over

    def reset_game(self):
        """reset_game the game"""
        
        self._reset_available_alphabets()   # reset available letters
        self.chose_random_word()            # chose a new random word
        self._reset_guesses()               # reset the remaining guess to 7
        self._reset_used_letters()          # reset used letters to an empty list
        self._game_over = False
        self._reset_correct_guesses()       # reset correct guess to 0
        
    def chose_random_word(self):
        """chose a random word from the word list"""
        self._secret_word = random.choice(self._dictionary)                # set the secret word to a new one
        self._word_so_far = self._turn_word_into_dash(self._secret_word)   # recreate a new dashes
        
    def _turn_word_into_dash(self, word):
        """turn the secret word into a string of dashes"""
        return ["_" for char in xrange(len(word))]

    def _deduct_guesses(self):
        """deduct the guess by one"""
        self._remaining_guess -= 1

    def get_remaining_guesses(self):
        return self._remaining_guess
    
    def _add_used_letter(self, letter):
        self._used_letters.append(letter)

    def _insert_char(self, char):
        """_insert_char(str) -> return (str)
        Enter characters into the dash
        """
        
        for num in xrange(len(self._secret_word)):
            if self._secret_word[num] == char:
                self._add_char_to_dash(char, num)  # add the char to words so far i.e string of dashes
                self._correct_guess += 1
        
        self._remove_letter(char)       # Remove the letter from available letters
        self._add_used_letter(char)     # add letter to used words
        

    # helpher function adds a word to dash
    def _add_char_to_dash(self, char, pos):
        """Enter characters into the dash depending on the position"""
        self._word_so_far[pos] = char

    def check_guess(self, guess):
        """checks whether the user has made a valid guess"""

        if self.get_remaining_guesses():

            guess = guess.upper()[0]
            if guess in self.get_used_letters():
                print "[+] you have already used that letter" # display message in graphic form
                
            else:

                if guess in self._get_secret_word():
                    self._insert_char(guess)
                    
                else:
                    self._deduct_guesses()                  # deduct the user guess by 1
                    
                    try:
                        
                        self._remove_letter(guess)         # Remove the letter from available letters
                        self._add_used_letter(guess)       # Append the used letter to list
                    except ValueError:
                        pass        
        else:

            self._game_over = True
            print "\n[+] The word was {}".format(self._get_secret_word()) # display word the user has gues

              
def new_game():
    """starts a new game"""

    guess_game.reset_game()
    Frame.set_canvas_background('White')
    guess_game._game_start = True
    game_start = True
    guess_game.game_mode("easy")

def easy():
    guess_game.game_mode("easy")
    print "Game play level : Easy"

def medium():
    guess_game.game_mode("medium")
    print "Game play level : Medium"

def diffuculty():
    guess_game.game_mode("diffuculty")
    print "Game play level : Diffuculty"

def random_word():
    """starts a new game"""

    print "Choosing random word at random diffuculty level"
    level = ["easy", "medium", "diffuculty"]
    random.shuffle(level)
    level = random.choice(level)
    
    guess_game.game_mode(level)
    print "Choosen level : {} ".format(level)
    
def user_guess(guess):
    """Allows the user to add make a guess"""

    # check if guess is not None
    if guess:
        guess_game.check_guess(guess)

def draw(canvas):
    title = []
    name = "hangman"

    if not guess_game._game_start:
        
        canvas.draw_image(img_info.get_img(), img_info.get_center(), img_info.get_size(), 
                          (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

        canvas.draw_text("The Word Game", (SCREEN_WIDTH/5, SCREEN_HEIGHT/5), 70, 'Red')
        canvas.draw_text("Learning spelling by guessing the word", (SCREEN_WIDTH/5, SCREEN_HEIGHT/2+180), 35, 'Green')
        canvas.draw_text("Over 60,000 words to play with !!", (SCREEN_WIDTH/5, SCREEN_HEIGHT/2+230), 35, 'Blue')
    else:

        if not guess_game.game_over():
           canvas.draw_text("The Spelling Game", (250, 70), 60, 'Red')
           canvas.draw_text(guess_game.get_word_so_far(), (50, 500), 25, 'Red')
           canvas.draw_text("[+] Available letters : {} ".format(guess_game.get_available_alphabets()), (0, 140), 23, 'Blue')
           canvas.draw_text("[+] Used letters : {} ".format(guess_game.get_used_letters()), (0, 249), 23, 'Blue')
           canvas.draw_text("[+] You have {} guess remaining".format(guess_game.get_remaining_guesses()), (1, 330), 23, 'Blue')

        if guess_game.game_over():
            Frame.set_canvas_background('Black')
            canvas.draw_text("GAME OVER!!!", (60, SCREEN_HEIGHT/2), 100, 'Red')
            sleep(1)
            canvas.draw_text("Ohh to bad, the correct word was ", (100,  100), 30, 'Red')
            canvas.draw_text("{}".format(guess_game._secret_word), (100, 150), 30, 'Red')
            

        elif guess_game._is_guess_correct():
            canvas.draw_text("Well done", (150, 450), 80, 'Green')
           


guess_game = GuessWordGame()
img_info = ImageInfo("https://dl.dropbox.com/s/wbq66iywhvbvcuw/abc.jpeg?dl=0")

# resigter events
Frame = simplegui.create_frame("Guess Word Game", SCREEN_WIDTH, SCREEN_HEIGHT)
Frame.set_canvas_background('White')
Frame.add_button("New Game", new_game, 150)
Frame.add_button("New random word", random_word, 150)
Frame.add_button("Easy",   easy, 150)
Frame.add_button("Medium", medium, 150)
Frame.add_button("Hard",   diffuculty, 150)
#Frame.add_button("Game Mode", game_mode, 150)


Frame.add_input("\nEnter a character", user_guess, 150)
Frame.set_draw_handler(draw)

# start the frame
Frame.start()

