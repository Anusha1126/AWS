import random
import string

def generate_random_text(length):
    """Generate a string of random text of a given length."""
    letters = string.ascii_letters + string.digits + string.punctuation + ' '
    return ''.join(random.choice(letters) for i in range(length))

def create_random_txt_file(file_path, length):
    """Create a .txt file with random text content."""
    random_text = generate_random_text(length)
    with open(file_path, 'w') as file:
        file.write(random_text)
    print(f"Random text file '{file_path}' created successfully.")

if __name__ == "__main__":
    file_path = "random_text.txt"  # Path to the .txt file to be created
    text_length = 1000  # Length of the random text to be generated

    create_random_txt_file(file_path, text_length)