# -*- coding: utf-8 -*-
"""CIS156_PS5.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wDY87r2g0bywr-BgSdIpD0T5XCrPDozG

please download the [words.txt](https://drive.google.com/file/d/1CTaQ5fhHiakivdaosFuyyVvRhvKW7_m_/view?usp=sharing) and [story.txt](https://drive.google.com/file/d/1Bxnss7vPayxGDHsEjOWAoN3kk3hbke8e/view?usp=sharing) and upload to your /content/words.txt and /content/story.txt to test these code!

Note: all attached files are supposed to be uploaded to /content dir
like /content/story.txt y /content/words.txt

PS1 Prompt:

Encryption is the process of obscuring information to make it unreadable without special knowledge. For centuries, people have devised schemes to encrypt messages - some better than others - but the advent of the computer and the Internet revolutionized the field. These days, it's hard not to encounter some sort of encryption, whether you are buying something online or logging into a shared computer system. Encryption lets you share information with other trusted people, without fear of disclosure.
A cipher is an algorithm for performing encryption (and the reverse, decryption). The original information is called plaintext. After it is encrypted, it is called ciphertext. The ciphertext message contains all the information of the plaintext message, but it is not in a format readable by a human or computer without the proper mechanism to decrypt it; it should resemble random gibberish to those for whom it is not intended.
A cipher usually depends on a piece of auxiliary information, called a key. The key is incorporated into the encryption process; the same plaintext encrypted with two different keys should have two different ciphertexts. Without the key, it should be difficult to decrypt the resulting ciphertext into readable plaintext.
This assignment will deal with a well-known (though not very secure) encryption method called the Caesar cipher. Some vocabulary to get you started on this problem:
Encryption - the process of obscuring or encoding messages to make them unreadable until they are decrypted
Decryption - making encrypted messages readable again by decoding them
Cipher - algorithm for performing encryption and decryption
Plaintext - the original message
Ciphertext - the encrypted message. Note: a ciphertext still contains all of the original message information, even if it looks like gibberish.
The Caesar Cipher
The idea of the Caesar Cipher is to pick an integer and shift every letter of your message by that integer. In other words, suppose the shift is k . Then, all instances of the i-th letter of the alphabet that appear in the plaintext should become the (i+k)-th letter of the alphabet in the ciphertext. You will need to be careful with the case in which i + k > 26 (the length of the alphabet). Here is what the whole alphabet looks like shifted three spots to the right:
Original:  a b c d e f g h i j k l m n o p q r s t u v w x y z
 3-shift:  d e f g h i j k l m n o p q r s t u v w x y z a b c
Using the above key, we can quickly translate the message "happy" to "kdssb" (note how the 3-shifted alphabet wraps around at the end, so x -> a, y -> b, and z -> c).
Note!! We are using the English alphabet for this problem - that is, the following letters in the following order:
>>> import string
>>> print string.ascii_lowercase
abcdefghijklmnopqrstuvwxyz
We will treat uppercase and lowercase letters individually, so that uppercase letters are always mapped to an uppercase letter, and lowercase letters are always mapped to a lowercase letter. If an uppercase letter maps to "A", then the same lowercase letter should map to "a". Punctuation and spaces should be retained and not changed. For example, a plaintext message with a comma should have a corresponding ciphertext with a comma in the same position.
|    plaintext    |  shift    |  ciphertext      |
| ----------------|-----------|------------------|
| 'abcdef'        |    2      |  'cdefgh'        |
| 'Hello, World!' |    5      |  'Mjqqt, Btwqi!' |
| ''              | any value |  ''              |

We implemented for you two helper functions: load_words and is_word. You may use these in your solution and you do not need to understand them completely, but should read the associated comments. You should read and understand the helper code in the rest of the file and use it to guide your solutions.
Getting Started
To get started, download the ps6.zip file. Extract it to your working directory. The files inside are:
ps6.py - a file containing three classes that you will have to implement.
words.txt - a file containing valid English words (should be in the same folder as your ps6..py file).
story.txt - a file containing an encrypted message that you will have to decode (should be in the same folder as your ps6..py file).
This will be your first experience coding with classes! We will have a Message class with two subclasses PlaintextMessage and CiphertextMessage .























Problem 1 - Build the Shift Dictionary and Apply Shift
0.0/20.0 points (graded)
The Message class contains methods that could be used to apply a cipher to a string, either to encrypt or to decrypt a message (since for Caesar codes this is the same action).
In the next two questions, you will fill in the methods of the Message class found in ps6.py according to the specifications in the docstrings. The methods in the Message class already filled in are:
__init__(self, text)
The getter method get_message_text(self)
The getter method get_valid_words(self), notice that this one returns a copy of self.valid_words to prevent someone from mutating the original list.
In this problem, you will fill in two methods:
Fill in the build_shift_dict(self, shift) method of the Message class. Be sure that your dictionary includes both lower and upper case letters, but that the shifted character for a lower case letter and its uppercase version are lower and upper case instances of the same letter. What this means is that if the original letter is "a" and its shifted value is "c", the letter "A" should shift to the letter "C".
If you are unfamiliar with the ordering or characters of the English alphabet, we will be following the letter ordering displayed by string.ascii_lowercase and string.ascii_uppercase:
>>> import string
>>> print(string.ascii_lowercase)
abcdefghijklmnopqrstuvwxyz
>>> print(string.ascii_uppercase)
ABCDEFGHIJKLMNOPQRSTUVWXYZ
A reminder from the introduction page - characters such as the space character, commas, periods, exclamation points, etc will not be encrypted by this cipher - basically, all the characters within string.punctuation, plus the space (' ') and all numerical characters (0 - 9) found in string.digits.
Fill in the apply_shift(self, shift) method of the Message class. You may find it easier to use build_shift_dict(self, shift). Remember that spaces and punctuation should not be changed by the cipher.





























Problem 2 - PlaintextMessage
0.0/15.0 points (graded)
PlaintextMessage is a subclass of Message and has methods to encode a string using a specified shift value. Our class will always create an encoded version of the message, and will have methods for changing the encoding.
Implement the methods in the class PlaintextMessage according to the specifications in ps6.py. The methods you should fill in are:
__init__(self, text, shift): Use the parent class constructor to make your code more concise.
The getter method get_shift(self)
The getter method get_encrypting_dict(self): This should return a COPY of self.encrypting_dict to prevent someone from mutating the original dictionary.
The getter method get_message_text_encrypted(self)
change_shift(self, shift): Think about what other methods you can use to make this easier. It shouldn’t take more than a couple lines of code.
















Problem 3 - CiphertextMessage
0.0/15.0 points (graded)
Given an encrypted message, if you know the shift used to encode the message, decoding it is trivial. If message is the encrypted message, and s is the shift used to encrypt the message, then apply_shift(message, 26-s) gives you the original plaintext message. Do you see why?
The problem, of course, is that you don’t know the shift. But our encryption method only has 26 distinct possible values for the shift! We know English is the main language of these emails, so if we can write a program that tries each shift and maximizes the number of English words in the decoded message, we can decrypt their cipher! A simple indication of whether or not the correct shift has been found is if most of the words obtained after a shift are valid words. Note that this only means that most of the words obtained are actual words. It is possible to have a message that can be decoded by two separate shifts into different sets of words. While there are various strategies for deciding between ambiguous decryptions, for this problem we are only looking for a simple solution.
Fill in the methods in the class CiphertextMessage according to the specifications in ps6.py. The methods you should fill in are:
__init__(self, text): Use the parent class constructor to make your code more concise.
decrypt_message(self): You may find the helper function is_word(wordlist, word) and the string method split() useful. Note that is_word will ignore punctuation and other special characters when considering whether a word is valid.
You may find the function string.split useful for dividing the text up into words.>>> 'Hello world!'.split('o')['Hell', ' w', 'rld!']


Problem 4 - Decrypt a Story
0.0/5.0 points (graded)
Now that you have all the pieces to the puzzle, please use them to decode the file story.txt. The file ps6.py contains a helper function get_story_string() that returns the encrypted version of the story as a string. Create a CiphertextMessage object using the story string and use decrypt_message to return the appropriate shift value and unencrypted story string.
"""

import string

### DO NOT MODIFY THIS FUNCTION ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print('Loading word list from file...')
    # inFile: file
    in_file = open(file_name, 'r')
    # line: string
    line = in_file.readline()
    # word_list: list of strings
    word_list = line.split()
    print('  ', len(word_list), 'words loaded.')
    in_file.close()
    return word_list

### DO NOT MODIFY THIS FUNCTION ###
def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

### DO NOT MODIFY THIS FUNCTION ###
def get_story_string():
    """
    Returns: a joke in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    ### DO NOT MODIFY THIS METHOD ###
    def __init__(self, text):
        '''
        Initializes a Message object

        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    ### DO NOT MODIFY THIS METHOD ###
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class

        Returns: self.message_text
        '''
        return self.message_text

    ### DO NOT MODIFY THIS METHOD ###
    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class

        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.

        shift (integer): the amount by which to shift every letter of the
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        '''
        #TODO
        pass #delete this line and replace with your code here

def apply_shift(self, shift):
    '''
    Applies the Caesar Cipher to self.message_text with the input shift.
    Creates a new string that is self.message_text shifted down the
    alphabet by some number of characters determined by the input shift

    shift (integer): the shift with which to encrypt the message.
    0 <= shift < 26

    Returns: the message text (string) in which every character is shifted
         down the alphabet by the input shift
    '''
    shifted_message = []

    # Go through each character in the message
    for char in self.message_text:
        if char.islower():  # If it's a lowercase letter
            new_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            shifted_message.append(new_char)
        elif char.isupper():  # If it's an uppercase letter
            new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            shifted_message.append(new_char)
        else:  # Non-alphabetical characters remain unchanged
            shifted_message.append(char)

    # Join the list of characters into a single string and return it
    return ''.join(shifted_message)


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object

        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encrypting_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)
        '''
        # Initialize the parent class with the text
class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object

        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encrypting_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        # Initialize the parent class with the text
        super().__init__(text)  # Calls Message.__init__(self, text)

        # Initialize the shift value specific to PlaintextMessage
        self.shift = shift

        # Create the encrypting dictionary using the shift value
        self.encrypting_dict = self.build_shift_dict(shift)

        # Encrypt the message text using the shift value
        self.message_text_encrypted = self.apply_shift(shift)


        #TODO
        pass #delete this line and replace with your code here

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object

        text (string): the message's text
        shift (integer): the shift associated with this message
        '''
        super().__init__(text)  # Calls Message.__init__(self, text)
        self.shift = shift
        self.encrypting_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class

        Returns: self.shift
        '''
        return self.shift

    def get_encrypting_dict(self):
        '''
        Used to safely access a copy of self.encrypting_dict outside of the class

        Returns: a COPY of self.encrypting_dict
        '''
        return self.encrypting_dict.copy()

        #TODO
        pass #delete this line and replace with your code here

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object

        text (string): the message's text
        shift (integer): the shift associated with this message
        '''
        super().__init__(text)  # Calls Message.__init__(self, text)
        self.shift = shift
        self.encrypting_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class

        Returns: self.shift
        '''
        return self.shift

    def get_encrypting_dict(self):
        '''
        Used to safely access a copy of self.encrypting_dict outside of the class

        Returns: a COPY of self.encrypting_dict
        '''
        return self.encrypting_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class

        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

        #TODO
        pass #delete this line and replace with your code here

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other
        attributes determined by shift (ie. self.encrypting_dict and
        message_text_encrypted).

        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        #TODO
        pass #delete this line and replace with your code here


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object

        text (string): the encrypted message's text
        '''
        super().__init__(text)  # Calls Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create
        the maximum number of valid words, you may choose any of those shifts
        (and their corresponding decrypted messages) to return.

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        best_shift = None
        max_valid_words = 0
        best_decrypted_message = ""

        # Loop through all possible shifts (0 to 25)
        for shift in range(26):
            # Decrypt the message with the current shift
            decrypted_message = self.apply_shift(26 - shift)

            # Split the decrypted message into words and count valid words
            words = decrypted_message.split()
            valid_word_count = sum([is_word(self.valid_words, word) for word in words])

            # If this shift gives more valid words, update the best shift
            if valid_word_count > max_valid_words:
                max_valid_words = valid_word_count
                best_shift = shift
                best_decrypted_message = decrypted_message

        return (best_shift, best_decrypted_message)

        #TODO
        pass #delete this line and replace with your code here

if __name__ == "__main__":
    # Example test case (PlaintextMessage)
    import os
    print("Current Working Directory:", os.getcwd())  # Get the current working directory

    # Create a PlaintextMessage object and encrypt it with shift 2
    plaintext = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')  # Expected encrypted text
    print('Actual Output:', plaintext.get_message_text_encrypted())  # Encrypted text from the object

    # Example test case (CiphertextMessage)
    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))  # Expected best shift and decrypted message
    print('Actual Output:', ciphertext.decrypt_message())  # Output from decrypting the ciphertext

    # Example test case (CiphertextMessage with story string)
    # Assuming get_story_string() returns the encrypted story text
    ciphertext = CiphertextMessage(get_story_string())
    print('Actual Output:', ciphertext.decrypt_message())  # Decrypt the story and print the result