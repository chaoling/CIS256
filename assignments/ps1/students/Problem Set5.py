import string

# Helper functions
def load_words():
    """
    Returns a list of valid words from the words.txt file.
    """
    with open('words.txt', 'r') as file:
        return file.read().splitlines()

def is_word(wordlist, word):
    """
    Returns True if the word is a valid word (in the wordlist),
    ignoring punctuation and capitalization.
    """
    word = word.lower().strip(string.punctuation)
    return word in wordlist

def get_story_string():
    """
    Helper function to get the encrypted story text from 'story.txt'
    """
    with open('story.txt', 'r') as file:
        return file.read()


# Message Class (Base class)
class Message:
    def __init__(self, text):
        self.text = text
        self.valid_words = load_words()

    def get_message_text(self):
        return self.text

    def get_valid_words(self):
        return self.valid_words[:]

    def build_shift_dict(self, shift):
        shift_dict = {}
        lower_alphabet = string.ascii_lowercase
        upper_alphabet = string.ascii_uppercase

        for i in range(26):
            # Create the shifted dictionary for lowercase letters
            shift_dict[lower_alphabet[i]] = lower_alphabet[(i + shift) % 26]
            # Create the shifted dictionary for uppercase letters
            shift_dict[upper_alphabet[i]] = upper_alphabet[(i + shift) % 26]

        return shift_dict

    def apply_shift(self, shift):
        shift_dict = self.build_shift_dict(shift)
        shifted_text = []

        for char in self.text:
            if char in shift_dict:
                shifted_text.append(shift_dict[char])
            else:
                shifted_text.append(char)  # Non-alphabetic characters remain unchanged

        return ''.join(shifted_text)


# PlaintextMessage Class (Subclass of Message)
class PlaintextMessage(Message):
    def __init__(self, text, shift):
        super().__init__(text)
        self.shift = shift
        self.encrypting_dict = self.build_shift_dict(shift)
        self.encrypted_text = self.apply_shift(shift)

    def get_shift(self):
        return self.shift

    def get_encrypting_dict(self):
        return self.encrypting_dict.copy()

    def get_message_text_encrypted(self):
        return self.encrypted_text

    def change_shift(self, shift):
        self.shift = shift
        self.encrypting_dict = self.build_shift_dict(shift)
        self.encrypted_text = self.apply_shift(shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        super().__init__(text)

    def decrypt_message(self):
        best_shift = 0
        max_valid_words = 0
        decrypted_message = ""

        # Try all 26 shifts and count valid words
        for shift in range(26):
            decrypted_text = self.apply_shift(26 - shift)  # Decrypt by shifting back
            words = decrypted_text.split()
            valid_word_count = sum([1 for word in words if is_word(self.valid_words, word)])  # Check if word is valid
            print(f"Shift {shift}: {decrypted_text} (valid words: {valid_word_count})")  # Print the shift result

            if valid_word_count > max_valid_words:
                max_valid_words = valid_word_count
                best_shift = shift
                decrypted_message = decrypted_text

        return decrypted_message  # Returns the best shift decrypted message


# Decrypt the Encrypted Story (Problem 4)
def decrypt_story():
    encrypted_story = get_story_string()  # Get the encrypted story
    ciphertext = CiphertextMessage(encrypted_story)
    decrypted_story = ciphertext.decrypt_message()
    print(decrypted_story)  # Print or process the decrypted story


# Example of how to encrypt and decrypt a message:
if __name__ == '__main__':
    # Encrypting a message
    plaintext = PlaintextMessage('Hello, World!', 5)
    print("Encrypted Message:", plaintext.get_message_text_encrypted())

    # Decrypting a message
    encrypted_message = CiphertextMessage(plaintext.get_message_text_encrypted())
    print("Decrypted Message:", encrypted_message.decrypt_message())

    # Decrypting the story from 'story.txt'
    decrypt_story()