# Template for cipher exercise
import random
import os
from language_dict import *

letters = "abcdefghijklmnopqrstuvwxyz"


# Helper functions:
# Create a dictionary from letters to letters based on Ceaser's code with a shift
def ceaser_code(shift):
    return {letters[i]: letters[(i + shift) % len(letters)] for i in range(len(letters))}


# Invert substition code
def inverse_code(code):
    return {code[c]:c for c in code}


# Generate random code
def random_code():
    code = list(letters)
    random.shuffle(code)
    return { letters[i]:code[i] for i in range(len(letters)) }


# Translate the plain text message into an encrypted one using the code dictionary
def encrypt(plaintext, code):
    return "".join([(code[c] if c in code else c) for c in plaintext])


# Translate the encrypted message into plain text using the code dictionary
def decrypt(cipher, code):
    return encrypt(cipher, inverse_code(code))


# Encrypt file
def encrypt_file(plain_filename, cipher_filename, code):
    f = open(plain_filename, 'r')
    plaintext = f.readlines()
    f.close()
    print(len(plaintext))
    cipher = [None]*len(plaintext)
    for i in range(len(plaintext)):
        cipher[i] = encrypt(plaintext[i].lower(), code)

    f = open(cipher_filename, 'w')  # save
    f.writelines(cipher)
    f.close()


# Decrypt file3
def decrypt_file(cipher_filename, plain_filename, code):
    encrypt_file(cipher_filename, plain_filename, inverse_code(code))
# End of Helper functions


# 7. Build language model from file
def build_language_dict(language_filename, words=False):
    if not os.path.isfile(language_filename):
        return None
    with open(language_filename, "r") as file:            # open file in read mode.
        text = file.read()
        if words:                                         # 2 dictionaries defined by the requested boolean variable.
            return compute_words_frequencies(text)
        else:
            return compute_letters_frequencies(text)


# 8. Break ceaser code by trying all different shifts and matching words to language
def break_ceaser_code(cipher, language_words):
    best_guess = ["", 0]                               # the expected outcome of the decrypt code and shift.
    max_count = 0
    for shift in range(26):
        guess = decrypt(cipher, ceaser_code(shift))
        count = count_words_in_language(guess, language_words)  # using helper function.
        if count >= max_count:
            max_count = count
            best_guess = [guess, shift]         # get the guess,shift that contains the most words in the language.
    return best_guess


# 9. Break general code: Find the best permutation substitution code by sorting letter frequencies for decrypted text
def break_code(cipher, language_letters):
    cipher_letters = compute_letters_frequencies(cipher)
    sorted_cipher_letters = sort_dict_keys_by_value(cipher_letters)       # using helper function.
    sorted_language_letters = sort_dict_keys_by_value(language_letters)   # using helper function.
    code = dict(zip(sorted_language_letters, sorted_cipher_letters))      # the guideline for the encryption.
    return [decrypt(cipher, code), code]


# 10. Break general code: Find the best permutation substitution code by sorting letter frequencies for decrypt text and modifying the code to match the language words
def break_code_with_words(cipher, language_letters, language_words):
    best_guess, best_code = break_code(cipher, language_letters)                # best option from language letters.
    best_guess_count = count_words_in_language(best_guess, language_words)      # using helper function.
    continue_swap = True                                    # flag- to begin the while loop.
    while continue_swap:
        continue_swap = False                               # flag- assume that the swap is over after the for loop.
        for i in range(len(letters) - 1):                   # run on indexes - i: 0 - 25 -> a - y
            for j in range(i+1, len(letters)):              # run on indexes - j: i+1 - 26 -> i+1 - z
                code = best_code.copy()                     # saves the original guideline in a copy form.
                key1, key2 = letters[i], letters[j]         # switch the values.
                code[key1], code[key2] = code[key2], code[key1]
                guess = decrypt(cipher, code)
                guess_count = count_words_in_language(guess, language_words)    # using helper function.
                if guess_count > best_guess_count:          # check if the new guess is better repeatedly.
                    best_code = code
                    best_guess = guess
                    best_guess_count = guess_count
                    continue_swap = True                    # flag- if their has been a change,we will keep swapping.
    return [best_guess, best_code]


# my_helper_methods


def sort_dict_keys_by_value(dictionary):             # helper function for question 9.
    sorted_keys = []
    while dictionary:                                # condition for a not empty dictionary.
        max_key, max_value = "", 0
        for key, value in dictionary.items():
            if value >= max_value:
                max_key, max_value = key, value      # finding the max key by value.
        sorted_keys.append(max_key)                  # save the max key.
        dictionary.pop(max_key)                      # remove the previous max key to create the order from max to min.
    return sorted_keys


def count_words_in_language(guess, language_words):  # helper function for questions 8  and 10
    count = 0
    guess_words = guess.split(" ")                   # get a list of strings from guess.
    for guess_word in guess_words:
        if guess_word in language_words:
            count += 1                               # count how many word from guess are in language words.
    return count


