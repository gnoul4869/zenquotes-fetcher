import os
import json
import requests
from time import sleep

ZENQUOTES_URL = "https://zenquotes.io/api/quotes/"
MAX_TRIES = 20  # Maximum number of times to fetch the quotes
DELAY = 60 * 5  # Seconds


def get_new_quotes():
    """
    Get new quotes from Zenquotes API

    Returns:
        list: List of new quotes
    """

    print("Getting new quotes...")

    raw_quotes = requests.get(ZENQUOTES_URL).json()

    quotes = [
        {
            "author": q["a"],
            "quote": q["q"],
        }
        for q in raw_quotes
    ]

    print(f"Got {len(quotes)} new quotes")

    return quotes


def load_quotes():
    """
    Load saved quotes from file

    Returns:
        list: List of saved quotes
    """

    print("Loading quotes...")

    with open("quotes.json", "r") as f:
        quotes = json.load(f)

    print(f"Loaded {len(quotes)} quotes.")

    return quotes


def update_quotes():
    "Update saved quotes from file with new quotes from Zenquotes API"

    new_quotes = get_new_quotes()
    quotes = load_quotes()

    num_old_quotes = len(quotes)

    for nq in new_quotes:
        if all(nq["quote"] != q["quote"] for q in quotes):
            quotes.append(nq)

    with open("quotes.json", "w") as f:
        json.dump(quotes, f, indent=4)

    num_new_quotes = len(quotes)
    print(f"Added {num_new_quotes - num_old_quotes} new quotes. Total: {num_new_quotes}")


if __name__ == "__main__":
    os.system("cls")

    print(f"{' BEGINNING UPDATE ':=^50}")

    i = 0
    while i < MAX_TRIES:
        i += 1
        print(f"{f' {i} ':-^50}")

        update_quotes()

        print(f"Sleeping for {DELAY} seconds...")
        print("--------------------------------------------------")

        if i < MAX_TRIES:
            sleep(DELAY)

    print(f"{' UPDATE COMPLETE ':=^50}")
