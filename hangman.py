"""Lógica principal del juego del ahorcado."""

import random
from config import MAX_ATTEMPTS


class Hangman:
    """Gestiona una partida de ahorcado con varias rondas."""

    def __init__(self, words):
        """Inicializa el juego con una lista de palabras.

        Args:
            words (list[str]): Lista de palabras disponibles.
        """
        self.words = words
        self.used_words = []
        self.reset_round()

    def reset_round(self):
        """Reinicia todos los datos de la ronda actual."""
        self.word = ""
        self.guessed_letters = set()
        self.wrong_letters = set()
        self.attempts = 0
        self.display_word = []

    def start_round(self):
        """Selecciona una nueva palabra y prepara la ronda."""
        self.reset_round()

        available_words = list(set(self.words) - set(self.used_words))
        if not available_words:
            raise ValueError("No quedan palabras disponibles")

        self.word = random.choice(available_words)
        self.used_words.append(self.word)
        self.display_word = ["_"] * len(self.word)

    def guess_letter(self, letter):
        """Procesa la letra introducida por el usuario.

        Args:
            letter (str): Letra introducida.

        Returns:
            bool | None:
                - True si la letra es correcta.
                - False si la letra es incorrecta.
                - None si la letra ya se había usado.
        """
        if letter in self.guessed_letters or letter in self.wrong_letters:
            return None

        if letter in self.word:
            self.guessed_letters.add(letter)

            for i, char in enumerate(self.word):
                if char == letter:
                    self.display_word[i] = letter

            return True

        self.wrong_letters.add(letter)
        self.attempts += 1
        return False

    def is_won(self):
        """Devuelve True si la palabra ha sido completada."""
        return "_" not in self.display_word

    def is_lost(self):
        """Devuelve True si se han agotado los intentos."""
        return self.attempts >= MAX_ATTEMPTS

    def get_display_word(self):
        """Devuelve la palabra oculta formateada."""
        return " ".join(self.display_word)
    
    def get_wrong_letters(self):
        """Devuelve las letras incorrectas ordenadas."""
        return sorted(self.wrong_letters)

    def get_attempts_left(self):
        """Devuelve el número de intentos restantes."""
        return MAX_ATTEMPTS - self.attempts

    def get_word(self):
        """Devuelve la palabra actual."""
        return self.word