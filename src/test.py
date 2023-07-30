import time

def countdown_timer(seconds):
    while seconds > 0:
        print(f"Time remaining: {seconds} seconds")
        time.sleep(1)
        seconds -= 1

    print("Time's up!")

if __name__ == "__main__":
    try:
        user_input = int(input("Enter the countdown time in seconds: "))
        countdown_timer(user_input)
    except ValueError:
        print("Invalid input. Please enter a valid number of seconds.")

