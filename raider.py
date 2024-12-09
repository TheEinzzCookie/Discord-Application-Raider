import discord
from discord.ext import commands
import os
import json
import time
import asyncio
from colorama import init, Fore, Style
init(autoreset=True)
def status():
    print(Fore.GREEN + "    Status: Running    ")
def logo():
    message = ['''    -... -.-- / . .. -. --.. --.. -.-. --- --- -.- .. . -.-.-. / -.. --- -. - / ... -.- .. -.. ''',
        '''            █████╗ ██████╗ ██████╗     ██████╗  █████╗ ██╗██████╗ ███████╗██████╗ ''',
        '''            ██╔══██╗██╔══██╗██╔══██╗    ██╔══██╗██╔══██╗██║██╔══██╗██╔════╝██╔══██╗''',
        '''            ███████║██████╔╝██████╔╝    ██████╔╝███████║██║██║  ██║█████╗  ██████╔╝''',
        '''            ██╔══██║██╔═══╝ ██╔═══╝     ██╔══██╗██╔══██║██║██║  ██║██╔══╝  ██╔══██╗''',
        '''            ██║  ██║██║     ██║         ██║  ██║██║  ██║██║██████╔╝███████╗██║  ██║''',
        '''            ╚═╝  ╚═╝╚═╝     ╚═╝         ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝''',
        '''    -... -.-- / . .. -. --.. --.. -.-. --- --- -.- .. . -.-.-. / -.. --- -. - / ... -.- .. -.. ''']
    colors = [Fore.BLUE, Fore.BLUE + Style.BRIGHT, Fore.CYAN, Fore.CYAN + Style.BRIGHT, Fore.LIGHTCYAN_EX, Fore.LIGHTCYAN_EX + Style.BRIGHT]
    for i, line in enumerate(message):
        print(colors[i % len(colors)] + line + Style.RESET_ALL)
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
clear()
filename = 'raid_template.json'
def load_template(filename):
    with open(filename, 'r') as file:
        return json.load(file)
def validate_inputs(message_amount):
    if message_amount not in [1, 2, 3, 4, 5]:
        raise ValueError("MESSAGE_AMOUNT must be 1, 2, 3, 4, or 5.")
TOKEN = None
MESSAGE_AMOUNT = None
final_message = None
def get_user_input():
    global TOKEN, MESSAGE_AMOUNT, final_message
    while True:
        TOKEN = input("    Input your bot's token: ")
        try:
            MESSAGE_AMOUNT = int(input("    Input the amount of messages to send per command (1-5): "))  # Convert to int
            validate_inputs(MESSAGE_AMOUNT)
            break  # Exit loop if inputs are valid
        except ValueError as ve:
            print(ve)
    print("    Input your raid message (separate messages with a semicolon ';' and press Enter when done):")
    user_input = input()
    RAID_MESSAGE = [msg.strip() for msg in user_input.split(';')]
    final_message = "\n".join(RAID_MESSAGE)
    print("    New template saved successfully.")
if os.path.exists(filename):
    use_last_template = input(Fore.CYAN + "    A previous template exists. Do you want to use the last template? (yes/no): ")
    if use_last_template.lower() == 'yes':
        template_data = load_template(filename)
        TOKEN = template_data['TOKEN']
        MESSAGE_AMOUNT = int(template_data['MESSAGE_AMOUNT'])
        final_message = template_data['final_message']
        print("    Loaded last template:")
        print(template_data)
    else:
        get_user_input()
else:
    get_user_input()
data_to_save = {
    'TOKEN': TOKEN,
    'MESSAGE_AMOUNT': MESSAGE_AMOUNT,
    'final_message': final_message,}
with open(filename, 'w') as file:
    json.dump(data_to_save, file, indent=4)
intents = discord.Intents.all()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)
time.sleep(1)
clear()
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(Fore.GREEN + "    Synced {len(synced)} command(s)")
        clear()
        logo()
        status()
    except Exception as e:
        print(Fore.RED + "    Failed to sync commands: {e}")
clear()
logo()
print(Fore.GREEN + "Ready to use!")
@bot.tree.command(
    name="spamraid",
    description="This sends out the raid message!")
async def send(interaction: discord.Interaction):
    try:
        if isinstance(interaction.channel, discord.DMChannel) or (
            isinstance(interaction.channel, discord.TextChannel) and
            interaction.channel.permissions_for(interaction.guild.me).send_messages):
            await interaction.response.send_message("Sending message...", ephemeral=True)
            for _ in range(MESSAGE_AMOUNT):
                await interaction.followup.send(final_message)
                await asyncio.sleep(0.02)
        else:
            await interaction.response.send_message(
                "I don't have permission to send messages in this channel!", 
                ephemeral=True
            )
    except Exception as e:
        if not interaction.response.is_done():
            await interaction.response.send_message(f"Error: {str(e)}", ephemeral=True)
        else:
            await interaction.followup.send(f"Error: {str(e)}", ephemeral=True)
bot.run(TOKEN)
