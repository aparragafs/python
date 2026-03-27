import random

class Hangman:
    MAX_ATTEMPTS = 6

    def __init__(self, words):
        self.words = words
        self.used_words = []
        self.reset_round()

    # Reinicia todo lo relacionado con una ronda
    def reset_round(self):
        self.word = ""
        self.guessed_letters = set()
        self.wrong_letters = set()
        self.attempts = 0
        self.display_word = []

    # Inicia una nueva ronda
    def start_round(self):
        self.reset_round()  

        # selecciona una palabra no usada
        available_words = list(set(self.words) - set(self.used_words))
        if not available_words:
            raise ValueError("No quedan palabras disponibles")

        self.word = random.choice(available_words)
        self.used_words.append(self.word)

        # crea representación oculta de la palabra
        self.display_word = ["_"] * len(self.word)


    # Procesa una letra introducida por el usuario
    def guess_letter(self, letter):
        # evita repetir letras
        if letter in self.guessed_letters or letter in self.wrong_letters:
            return "repeated"

        # letra correcta - actualizar posiciones
        if letter in self.word:
            self.guessed_letters.add(letter)

            for i, char in enumerate(self.word):
                if char == letter:
                    self.display_word[i] = letter

            return "correct"
        # letra incorrecta - suma intento
        else:
            self.wrong_letters.add(letter)
            self.attempts += 1
            return "incorrect"

    # gana si no quedan guiones
    def is_won(self):
        return "_" not in self.display_word

    # pierde si supera intentos máximos
    def is_lost(self):
        return self.attempts >= self.MAX_ATTEMPTS

    # devuelve palabra formateada para mostrar
    def get_display_word(self):
        return " ".join(self.display_word)

    # devuelve letras falladas ordenadas
    def get_wrong_letters(self):
        return sorted(self.wrong_letters)

    # intentos restantes
    def get_attempts_left(self):
        return self.MAX_ATTEMPTS - self.attempts
    
    # palabra actual (para mostrar al perder)
    def get_word(self):
        return self.word