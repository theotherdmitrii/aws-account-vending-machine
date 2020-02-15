import random
import string


def generate(length: int) -> str:
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


if __name__ == "__main__":
    print(generate(16))
