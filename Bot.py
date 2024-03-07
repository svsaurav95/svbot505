# main.py

import discord
import openai
import random
import requests
import json
from discord.ext import commands
import os
from config import TOKEN

openai.api_key = 'OPENAI_KEY'

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='/-', intents=intents)

# generate response using ChatGPT API
async def generate_response(message):
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": message.content,
            },
        ],
    )
    return completion.choices[0].message.content


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # Generate response using ChatGPT API
    response = await generate_response(message)
    # Send the response back to the Discord channel
    await message.channel.send(response)

# Command: hello
@client.command()
async def hello(ctx):
    await ctx.send("whass poppin")

# Command: pj
@client.command()
async def pj(ctx):
    jokeurl = "https://joke3.p.rapidapi.com/v1/joke"
    payload = {"content": "A joke here", "nsfw": "true"}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY",
        "X-RapidAPI-Host": "joke3.p.rapidapi.com"
    }
    response = requests.post(jokeurl, json=payload, headers=headers)
    data = json.loads(response.text)
    await ctx.send(data['content'])

# Command: cut
@client.command()
async def cut(ctx):
    await ctx.send("catch you later homie")

# Command: join
@client.command(pass_context=True)
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("pull up to vc cuh")

# Command: leave
@client.command(pass_context=True)
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("dipped from vc")
    else:
        await ctx.send("not in vc")

# Command: doggo
@client.command()
async def doggo(ctx):
    embed = discord.Embed(title="doggo", url="https://www.google.com/search?q=dog&sxsrf=AOaemvIEUwO7gqX3EbnFLZ0CgRvNF9QCyQ:1638285894412&source=lnms&tbm=isch&sa=X&ved=2ahUKEwip5OP7xb_0AhVnxzgGHSkhBSgQ_AUoAXoECAEQAw&biw=1366&bih=657", description="bro da dawg", color=0x4dff4d)
    embed.set_author(name="aura", url="", icon_url="https://images.app.goo.gl/vgsxAuKpaMEEVQc89")
    embed.set_thumbnail(url="https://www.google.com/search?q=dog&sxsrf=AOaemvIEUwO7gqX3EbnFLZ0CgRvNF9QCyQ:1638285894412&source=lnms&tbm=isch&sa=X&ved=2ahUKEwip5OP7xb_0AhVnxzgGHSkhBSgQ_AUoAXoECAEQAw&biw=1366&bih=657")
    await ctx.send(embed=embed)

# Command: rps
@client.command()
async def rps(ctx, user_choice):
    choices = ["rock", "paper", "scissors"]
    if user_choice.lower() not in choices:
        await ctx.send("Invalid choice! Choose either rock, paper, or scissors.")
        return
    bot_choice = random.choice(choices)
    winner = determine_winner(choices.index(user_choice.lower()), choices.index(bot_choice))
    await ctx.send(f"I chose {bot_choice}. {winner}")

def determine_winner(user_choice_index, bot_choice_index):
    if user_choice_index == bot_choice_index:
        return "It's a tie!"
    elif (user_choice_index - bot_choice_index) % 3 == 1:
        return "You win!"
    else:
        return "I win!"

# Command: ban
@client.command()
async def ban(ctx, member: discord.Member):
    if ctx.author.guild_permissions.administrator:
        await member.ban()
        await ctx.send(f"{member.mention} has been banned.")
    else:
        await ctx.send("You do not have permission to use this command.")

# Command: serverpeeps
@client.command()
async def serverpeeps(ctx):
    member_count = ctx.guild.member_count
    await ctx.send(f"The server has {member_count} members!")

# Command: mute
@client.command()
async def mute(ctx, member: discord.Member):
    if ctx.author.guild_permissions.administrator:
        voice_state = member.voice
        if voice_state:
            await member.edit(mute=True)
            await ctx.send(f"{member.mention} has been muted.")
        else:
            await ctx.send(f"{member.mention} is not in a voice channel.")
    else:
        await ctx.send("This command is for admins only.")

# Command descriptions
command_descriptions = {
    "hello": "Says hello!",
    "pj": "Tells a joke.",
    "cut": "Says goodbye.",
    "join": "Joins the voice channel.",
    "leave": "Leaves the voice channel.",
    "doggo": "Sends a doggo image.",
    "rps": "Plays Rock Paper Scissors.",
    "ban": "Bans a member.",
    "serverpeeps": "Displays the member count of the server.",
    "mute" : "Mutes a member in voice chat."
}

# Command to display help
@client.command()
async def show_help(ctx):
    embed = discord.Embed(title="Command List", description="BOT COMMANDS AVAILABLE!!!!!")
    for command, description in command_descriptions.items():
        embed.add_field(name=f"/-{command}", value=description, inline=False)
    await ctx.send(embed=embed)


class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'

    def print_board(self):
        board_str = '\n'.join([' | '.join(row) for row in self.board])
        return f'```\n{board_str}\n```'

    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return True
        return False

game = None

@client.command()
async def tictac(ctx):
    global game
    if game is None:
        game = TicTacToe()
        await ctx.send("Tic Tac Toe game started!\n" + game.print_board())
    else:
        await ctx.send("A Tic Tac Toe game is already in progress.")

# Command to make a move in Tic Tac Toe game
@client.command()
async def move(ctx, row: int, col: int):
    global game
    if game is None:
        await ctx.send("No Tic Tac Toe game in progress. Use `/-tictac` to start a new game.")
        return
    if row < 0 or row > 2 or col < 0 or col > 2:
        await ctx.send("Invalid move! Please enter row and column indices between 0 and 2.")
        return
    if game.make_move(row, col):
        await ctx.send(f"Move made by player {game.current_player}:\n{game.print_board()}")
        if game.check_winner():
            await ctx.send(f"Player {game.current_player} wins!")
            game = None
    else:
        await ctx.send("Invalid move! That position is already taken.")

# Command to display the current Tic Tac Toe board
@client.command()
async def board(ctx):
    global game
    if game is None:
        await ctx.send("No Tic Tac Toe game in progress. Use `/-tictac` to start a new game.")
        return
    await ctx.send(game.print_board())

client.run(TOKEN)
