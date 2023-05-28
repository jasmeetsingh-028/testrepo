import discord
from discord.ext import commands
import random

class Player:
    def __init__(self, user):
        self.user = user
        self.number = None

class NumberGuessingGame:
    def __init__(self):
        self.players = []
        self.target_number = None
        self.game_started = False

    def add_player(self, user):
        if not self.game_started:
            player = Player(user)
            self.players.append(player)

    def start_game(self):
        if not self.game_started and len(self.players) >= 2:
            self.target_number = random.randint(1, 100)
            self.game_started = True

    def guess_number(self, user, number):
        if self.game_started:
            for player in self.players:
                if player.user == user:
                    player.number = number
                    break

    def all_players_guessed(self):
        return all(player.number is not None for player in self.players)

    def get_game_status(self):
        return self.game_started

    def get_winner(self):
        closest_distance = float('inf')
        winner = None

        for player in self.players:
            if player.number is not None:
                distance = abs(player.number - self.target_number)
                if distance < closest_distance:
                    closest_distance = distance
                    winner = player

        return winner


class MyClient(discord.Client):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.game = NumberGuessingGame()

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.channel.id != 1112025912712642650:
            return

        if message.author == self.user:
            return
        
        
        content = message.content.lower()

        print(content)

        if content.startswith('!join'):
            if self.game.get_game_status():
                await message.channel.send('The game has already started or ended. Try again later.')
            else:
                self.game.add_player(message.author)
                await message.channel.send(f'{message.author.mention} has joined the game!')

        elif content.startswith('!start'):
            if self.game.get_game_status():
                await message.channel.send('The game has already started or ended. Try again later.')
            elif len(self.game.players) < 2:
                await message.channel.send('Not enough players to start the game. Need at least 2 players.')
            else:
                self.game.start_game()
                await message.channel.send('The game has started! Guess a number between 1 and 100.')

        elif content.startswith('!guess'):
            if not self.game.get_game_status():
                await message.channel.send('The game has not started yet. Use the `!start` command to start the game.')
            else:
                try:
                    number = int(content.split(' ')[1])
                    self.game.guess_number(message.author, number)

                    if self.game.all_players_guessed():
                        winner = self.game.get_winner()
                        if winner is not None:
                            await message.channel.send(f'{winner.user.mention} has won the game with the closest guess of {winner.number} which was close to {self.game.target_number}!')
                        else:
                            await message.channel.send('No winner this time! The game has ended.')
                        self.game.game_started = False
                        self.game.players = []
                    else:
                        await message.channel.send(f'{message.author.mention} has guessed the number {number}.')
                   
                except IndexError:
                    await message.channel.send('Please provide a valid number to guess.')


def run_game():
    # Discord bot token
    TOKEN = 'YOUR_DISCORD_TOKEN'

    intents = discord.Intents.default()
    intents.message_content = True

    # Create the bot
    bot = MyClient(command_prefix='!', intents=intents)

    # Run the bot
    bot.run('MTA4MDE1NzQ0NjI4ODQ1MzY2NA.GRRFkc.o0A_Mw9PWkEBkVmfoBYCn6wkdoPBv5GddZjgqE')


if __name__ == '__main__':
    run_game()
