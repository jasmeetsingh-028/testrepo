import discord
from discord.ext import commands
import random

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.channel.id != 1112020200175456367:
            return

        if message.author == self.user:
            return

        content = message.content.lower()

        if content.startswith('!play'):
            choices = ['rock', 'paper', 'scissors']
            try:
                player_choice = content.split(' ')[1]
            except IndexError:
                response = 'Invalid command format! Please use `!play` followed by your choice: rock, paper, or scissors.'
                await message.channel.send(response)
                return

            if player_choice not in choices:
                response = 'Invalid choice! Please choose either rock, paper, or scissors.'
            else:
                bot_choice = random.choice(choices)
                result = self.get_game_result(player_choice, bot_choice)
                response = f'You chose {player_choice}, and the bot chose {bot_choice}. {result}'

            await message.channel.send(response)

        elif content.startswith('!rules'):
            rules = "Welcome to Rock, Paper, Scissors game!\n\n" \
                    "To play, use the command `!play` followed by your choice: rock, paper, or scissors.\n" \
                    "For example, `!play rock` to choose rock.\n\n" \
                    "Remember the rules:\n" \
                    "- Rock beats scissors\n" \
                    "- Scissors beat paper\n" \
                    "- Paper beats rock\n\n" \
                    "Let's start playing! Have fun!"

            await message.channel.send(rules)

    def get_game_result(self, player_choice, bot_choice):
        if player_choice == bot_choice:
            return "It's a tie!"
        elif (player_choice == 'rock' and bot_choice == 'scissors') or \
             (player_choice == 'paper' and bot_choice == 'rock') or \
             (player_choice == 'scissors' and bot_choice == 'paper'):
            return 'You win!'
        else:
            return 'Bot wins!'

def main():
    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)
    client.run('MTA4MDE1NzQ0NjI4ODQ1MzY2NA.GRRFkc.o0A_Mw9PWkEBkVmfoBYCn6wkdoPBv5GddZjgqE')

if __name__ == "__main__":
    main()
