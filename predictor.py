import re

# pattern that find all symbols that are not 1 or 0
pattern = r"[^01]"
triads = dict()


def add_to_dict(user_input):
    # iterates through all characters except last 3
    # this is done because you can't gain any prediction from the last 3
    for n in range(len(user_input) - 3):
        triads.setdefault(user_input[n:n + 3], [0, 0])
        if user_input[n + 3] == "0":
            triads[user_input[n:n + 3]][0] += 1
        else:
            triads[user_input[n:n + 3]][1] += 1


# Creating the initial string to gather data
def gather_string_data():
    print("Please provide AI some data to learn...")
    initial_string = ""
    while len(initial_string) < 100:
        print(f"The current data length is {len(initial_string)}, {100 - len(initial_string)} symbols left")
        print("Print a random string containing 0 or 1: ")
        user_input = input()
        # Uses pattern to remove all non 1 or 0 characters
        initial_string += re.sub(pattern, "", user_input)

    print("Final data string:")
    print(initial_string)
    add_to_dict(initial_string)


def get_new_input():
    game_inputs = ""
    # iterates through all characters except last 3
    # this is done because you can't gain any prediction from the last 3
    while len(game_inputs) < 4:
        print("Print a random string containing 0 or 1:")
        game_inputs = input()
        # if string is "enough", it breaks to return string unchanged
        if game_inputs == "enough":
            break
        game_inputs = re.sub(pattern, "", game_inputs)

    return game_inputs


def guess_following_value(new_input):
    guess_string = ""
    correct_guesses = 0
    # iterates through all characters except last 3
    # this is done because you can't gain any prediction from the last 3
    for x in range(len(new_input) - 3):
        current_triad = new_input[x:x + 3]
        prob_next_1 = (triads[current_triad][1]) / (triads[current_triad][0] + triads[current_triad][0])
        if prob_next_1 > 0.5:
            guess_string += "1"
        elif prob_next_1 < 0.5:
            guess_string += "0"
        else:
            # Hard coded 0 due to Hyperskill needing a 0 to be correct
            guess_string += "0"
        if guess_string[x] == new_input[x + 3]:
            correct_guesses += 1
    return correct_guesses, guess_string


def lets_play_game():
    # These 4 lines need to be written exactly as follows
    # in order to pass HyperSkill check
    print()
    print("You have $1000. Every time the system successfully predicts your next press, you lose $1.")
    print("Otherwise, you earn $1. Print \"enough\" to leave the game. Let's go!")
    print()

    game_guess = get_new_input()
    balance = 1000

    # "enough" is used to end game
    while game_guess != "enough":
        correct_guesses, guess_string = guess_following_value(game_guess)
        accuracy = 100 * (round(correct_guesses / len(guess_string), 4))
        balance = balance - correct_guesses + (len(guess_string) - correct_guesses)

        print("predictions:")
        print(guess_string)
        print()
        print(f"Computer guessed {correct_guesses} out of {len(guess_string)} symbols({accuracy}%)")
        print(f"Your balance is now ${balance}")
        print()

        # analyzes latest input to increase accuracy
        add_to_dict(game_guess)
        game_guess = get_new_input()

    print("Game Over!")


def main():
    gather_string_data()
    lets_play_game()


if __name__ == "__main__":
    main()
