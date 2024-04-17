import discord
from discord.ui import Button, View
from discord import ButtonStyle

win_conditions = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]


class TicTacToeButton(Button):
    def __init__(self, x, y):
        super().__init__(style=ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        game = self.view.game
        player = interaction.user

        if player.id != game.current_player.id:
            await interaction.response.send_message("Сейчас не ваш ход!", ephemeral=True)
            return

        position = self.y * 3 + self.x
        if game.board[position] == '\u200b':
            game.board[position] = game.current_symbol
            self.label = game.current_symbol
            self.disabled = True
            await interaction.response.edit_message(view=self.view)

            if game.check_win():
                for item in self.view.children:
                    item.disabled = True
                content = f'{game.current_player.mention} выиграл!'
                game.game_over = True
            elif not any(spot == '\u200b' for spot in game.board):
                for item in self.view.children:
                    item.disabled = True
                content = 'Игра закончилась вничью!'
                game.game_over = True
            else:
                game.current_player, game.next_player = game.next_player, game.current_player
                game.current_symbol, game.next_symbol = game.next_symbol, game.current_symbol
                content = f"Следующий ход: {game.current_player.mention}"

            await interaction.edit_original_response(content=content, view=self.view if not game.game_over else None)


class TicTacToeView(View):
    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game
        for y in range(3):
            for x in range(3):
                self.add_item(TicTacToeButton(x, y))


class TicTacToeGame:
    def __init__(self, channel, player1, player2):
        self.board = ['\u200b'] * 9
        self.channel = channel
        self.current_player = player1
        self.next_player = player2
        self.current_symbol = '❌'
        self.next_symbol = '⭕'
        self.game_over = False
        self.message = None

    async def start(self):
        view = TicTacToeView(self)
        self.message = await self.channel.send(f"{self.current_player.mention}, ваш ход!", view=view)

    def check_win(self):
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] != '\u200b':
                return True
        return False


async def tictactoe(ctx, opponent: discord.Member):
    game = TicTacToeGame(ctx.channel, ctx.author, opponent)
    await game.start()
