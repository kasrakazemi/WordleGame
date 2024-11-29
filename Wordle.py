# %%
import nltk
from termcolor import colored
import time

# %%
# Ensure the NLTK word corpus is downloaded
nltk.download('words')

# %%
# Load all valid English words
from nltk.corpus import words
all_words = words.words()
five_letter_words = set([word.lower() for word in all_words if len(word) == 5])

# %%
# Helper function to clean up user input
def clean_input(input_list):
    return [item.strip() for item in input_list if item.strip()]

# %%
# Function to filter words based on criteria
def filter_words(positional_correct, positional_incorrect, present_letters, absent_letters):
    filtered_words = []
    for word in five_letter_words:
        # Check if all letters in `present_letters` exist in the word
        if not all(letter in word for letter in present_letters):
            continue
        
        # Check if no letter in `absent_letters` exists in the word
        if any(letter in word for letter in absent_letters):
            continue
        
        # Check if letters in `positional_correct` match the exact positions
        if not all(word[i] == letter for i, letter in enumerate(positional_correct) if letter != '0'):
            continue
        
        # Check if letters in `positional_incorrect` are not in those positions
        if any(word[i] == letter for i, letter in enumerate(positional_incorrect) if letter != '0'):
            continue
        
        filtered_words.append(word)
    
    return filtered_words

# %%
# Display instructions to the user
instructions = colored(
    "Instructions:\n"
    "1. Start with one of the suggested words.\n"
    "2. After each attempt, enter the feedback:\n"
    "   - Exact matches (correct letters in correct positions).\n"
    "   - Letters in the word but in wrong positions.\n"
    "   - Letters not in the word.\n"
    "3. Repeat until you find the answer.\n", 
    'blue', attrs=['bold']
)
print(instructions)

start_message = colored(
    "Start with one of these words:\n\nanise\nagile\naisle\naides\nabide", 
    'green', attrs=['bold']
)
print(start_message)

# %%
# Initialize lists for game logic
exact_positions = ['0', '0', '0', '0', '0']  # Correct letters in the correct positions
incorrect_positions = ['0', '0', '0', '0', '0']  # Letters in the wrong positions
present_letters = []  # Letters that are in the word
absent_letters = []  # Letters that are not in the word

# %%
# Game loop
for attempt in range(6):
    print(colored(f"Attempt {attempt + 1}:", 'yellow', attrs=['bold']))

    # Get feedback from the user
    exact_positions = list(input(colored(
        "Enter the correct positions (e.g., 'a00le' for 'a' at position 1, 'l' at position 4):\n", 
        'blue', attrs=['bold']
    )))
    incorrect_positions = list(input(colored(
        "Enter the wrong positions (e.g., '0g00e' where 'g' and 'e' are not in these positions):\n", 
        'blue', attrs=['bold']
    )))
    
    present_input = input(colored(
        "Enter letters that are in the word, separated by spaces (press Enter if none):\n", 
        'blue', attrs=['bold']
    ))
    absent_input = input(colored(
        "Enter letters that are NOT in the word, separated by spaces (press Enter if none):\n", 
        'blue', attrs=['bold']
    ))
    
    # Update letter lists
    present_letters += clean_input(present_input.split())
    absent_letters += clean_input(absent_input.split())

    # Filter words based on user feedback
    suggestions = filter_words(exact_positions, incorrect_positions, present_letters, absent_letters)
    
    # Display suggestions
    if suggestions:
        print(colored("Try one of these words:", 'green', attrs=['bold']))
        for i in range(0, len(suggestions), 5):
            print("  ".join(f"{word:<10}" for word in suggestions[i:i + 5]))
    else:
        print(colored("No valid words found. Check your inputs!", 'red', attrs=['bold']))

    # Check if the game is complete
    stop_game = input(colored("Did you find the correct word? (y/n):\n", 'red', attrs=['bold']))
    if stop_game.lower() == 'y':
        print(colored("Congratulations! Have a great day!", 'green', attrs=['bold']))
        break
else:
    print(colored("Game over. Better luck next time!", 'red', attrs=['bold']))
