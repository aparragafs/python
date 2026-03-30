"""Punto de entrada del juego del ahorcado."""

import csv
import uuid
from datetime import datetime

from config import GAMES_FILE, HANGMAN_PICS, MAX_ROUNDS, ROUNDS_FILE, WORDS_FILE
from hangman import Hangman


def load_words(filename):
    """Carga las palabras desde un archivo CSV.

    Args:
        filename (str): Ruta del archivo.

    Returns:
        list[str]: Lista de palabras.
    """
    with open(filename, encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def save_game(game_id, username, start_date, end_date, final_score):
    """Guarda los datos de una partida completa."""
    with open(GAMES_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([game_id, username, start_date, end_date, final_score])


def save_round(game_id, word, username, round_id, user_trys, victory):
    """Guarda los datos de una ronda."""
    with open(ROUNDS_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([game_id, word, username, round_id, user_trys, victory])


def play_round(game, player_name, round_number, game_id):
    """Ejecuta una ronda completa del juego."""
    game.start_round()
    round_id = str(uuid.uuid4())

    print(f"\n--- Ronda {round_number} ---")

    while not game.is_won() and not game.is_lost():
        print(HANGMAN_PICS[game.attempts])
        print("\nPalabra:", game.get_display_word())
        print("Fallos:", " ".join(game.get_wrong_letters()))
        print("Intentos restantes:", game.get_attempts_left())

        letter = input("Introduce una letra: ").lower()

        if not letter.isalpha() or len(letter) != 1:
            print("Introduce una letra válida.")
            continue

        result = game.guess_letter(letter)

        if result is True:
            print("¡Correcto!")
        elif result is False:
            print("Incorrecto.")
        else:
            print("Ya la has usado.")

    if game.is_won():
        print("\n¡Has ganado la ronda!")
        victory = True
    else:
        print(HANGMAN_PICS[game.attempts])
        print("\nHas perdido la ronda.")
        print("La palabra era:", game.get_word())
        victory = False

    save_round(
        game_id,
        game.get_word(),
        player_name,
        round_id,
        game.attempts,
        victory
    )

    return victory


def main():
    """Ejecuta una partida completa."""
    words = load_words(WORDS_FILE)

    if len(words) != 30:
        print("Vaya, parece que no encontramos todas las palabras necesarias.")
        return

    print("Palabras listas, ¡adelante!")

    player_name = input("Introduce tu nombre: ")
    game = Hangman(words)

    game_id = str(uuid.uuid4())
    start_date = datetime.now()

    total_wins = 0

    for i in range(1, MAX_ROUNDS + 1):
        if play_round(game, player_name, i, game_id):
            total_wins += 1

    end_date = datetime.now()

    print(
        f"\nPartida finalizada. Tu puntuación es: "
        f"{total_wins}/{MAX_ROUNDS}. Gracias por jugar, {player_name}."
    )

    save_game(game_id, player_name, start_date, end_date, total_wins)

if __name__ == "__main__":
    main()