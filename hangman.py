import random

import discord
from discord import ButtonStyle
from discord.ui import Button, View

WORDS = [
    "mystery", "whisper", "harvest", "journey", "feather", "captain", "diamond", "brother",
    "fantasy", "liberty", "justice", "balloon", "element", "silence", "monarch", "trouble",
    "college", "freedom", "picture", "blanket", "justice", "octagon", "marathon", "network",
    "january", "visible", "kingdom", "quantum", "traverse", "vaccine", "eclipse", "organic",
    "article", "measure", "theater", "sapphire", "aviation", "corridor", "crusader", "dinosaur",
    "emerald", "festival", "glacier", "heritage", "illusion", "juncture", "kangaroo", "lantern",
    "magnetic", "nebula", "obelisk", "pacifier", "quarrel", "republic", "skeleton", "tropical",
    "umbrella", "vacation", "warranty", "xenolith", "yielding", "zodiac", "ancestor", "bachelor",
    "cemetery", "diligent", "elephant", "flamenco", "gorgeous", "hierarchy", "insomnia", "jasmine",
    "kerosene", "leverage", "minstrel", "nautical", "opposite", "pendulum", "question", "reformer",
    "scarcity", "turbine", "universe", "variable", "wrestler", "exchange", "yearling", "zeppelin",
    "adequate", "blueprint", "chemical", "doctrine", "ensemble", "flotilla", "guidance", "handbook",
    "infinity", "jovially"
]


class HangmanButton(Button):
    def __init__(self, letter, row):
        super().__init__(style=ButtonStyle.secondary, label=letter, row=row)
        self.letter = letter

    async def callback(self, interaction: discord.Interaction):
        game = self.view.game
        player = interaction.user

        if player.id != game.current_player.id:
            return

        if self.letter in game.word:
            game.reveal_letters(self.letter)
        elif len(self.letter) == 2:
            if 'Y' in game.word:
                game.reveal_letters('Y')
            if 'Z' in game.word:
                game.reveal_letters('Z')
        else:
            game.wrong_guesses += 1

        self.disabled = True
        await interaction.response.edit_message(view=self.view)

        if game.check_win():
            content = f"{game.current_player.mention} wins! The word was '{game.word}'."
            for item in self.view.children:
                item.disabled = True
            game.game_over = True
        elif game.wrong_guesses == game.max_guesses:
            content = f"Game over! The word was '{game.word}'."
            for item in self.view.children:
                item.disabled = True
            game.game_over = True
        else:
            content = game.display_word()

        await interaction.edit_original_response(content=content, view=self.view if not game.game_over else None)


class HangmanView(View):
    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWX"
        row = 0
        i = 0
        for letter in alphabet:
            if i == 5:
                row += 1
                i = 0
            self.add_item(HangmanButton(letter, row=row))
            i += 1
        self.add_item(HangmanButton('YZ', row=row))


class HangmanGame:
    def __init__(self, channel, player):
        self.channel = channel
        self.current_player = player
        self.word = random.choice(WORDS).upper()
        self.displayed_word = ["\\*" for char in self.word]
        self.wrong_guesses = 0
        self.max_guesses = 6
        self.game_over = False
        self.message = None

    def reveal_letters(self, letter):
        for i, char in enumerate(self.word):
            if char == letter:
                self.displayed_word[i] = letter
        print(f"After revealing letters: {' '.join(self.displayed_word)}")

    def display_word(self):
        lives = self.max_guesses - self.wrong_guesses
        return f"Word: {' '.join(self.displayed_word)}\n Wrong guesses left: {lives}"

    def check_win(self):
        return '\*' not in self.displayed_word

    async def start(self):
        view = HangmanView(self)
        content = self.display_word()
        print(f"Initial display content: {content}")
        self.message = await self.channel.send(content, view=view)


async def hangman(ctx):
    game = HangmanGame(ctx.channel, ctx.author)
    await game.start()
