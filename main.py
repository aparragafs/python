from hangman import Hangman
import csv
import uuid
from datetime import datetime

# Dibujos del ahorcado según número de fallos
HANGMAN_PICS = [
    """
       -----
       |   |
           |
           |
           |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
           |
           |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
       |   |
           |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
      /|   |
           |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
      /|\\  |
           |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    =========
    """
]

# Lee las palabras del CSV y devuelve una lista 
def load_words(filename):
    with open(filename, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


# Guarda una partida completa (una fila en games.csv)
def save_game(game_id, username, start_date, end_date, final_score):
    with open("games.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([game_id, username, start_date, end_date, final_score])


# Guarda cada ronda jugada
def save_round(game_id, word, username, round_id, user_trys, victory):
    with open("rounds_in_games.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([game_id, word, username, round_id, user_trys, victory])


# Ejecuta una ronda completa del juego
def play_round(game, player_name, round_number, game_id):
    game.start_round()
    round_id = str(uuid.uuid4())

    print(f"\n--- Ronda {round_number} ---")

    # Bucle principal: se repite hasta ganar o perder
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

        if result == "correct":
            print("¡Correcto!")
        elif result == "incorrect":
            print("Incorrecto.")
        else:
            print("Ya la has usado.")

    # Resultado
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
    words = load_words("words.csv")

    if len(words) != 30:
        print("Vaya, parece que no encontramos todas las palabras necesarias.")
        return

    print("Palabras listas, ¡adelante!")

    player_name = input("Introduce tu nombre: ")
    game = Hangman(words)

    game_id = str(uuid.uuid4())
    start_date = datetime.now()

    total_wins = 0

    for i in range(1, 4):
        if play_round(game, player_name, i, game_id):
            total_wins += 1

    end_date = datetime.now()

    print(f"\nPartida finalizada. Tu puntuación es: {total_wins}/3 Gracias por jugar, {player_name}.")

    save_game(game_id, player_name, start_date, end_date, total_wins)


# Punto de entrada del programa
if __name__ == "__main__":
    main()