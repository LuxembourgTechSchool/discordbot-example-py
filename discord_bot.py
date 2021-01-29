# Import helpful libraries that you need at the beginning of your program.
import os
import random
import discord
from dotenv import load_dotenv

# Load your environment variables saved in a .env file.
# This "hides" them from others, as long as
# you don't share the file or they are not ignored by 
# the .gitignore file of github.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Don't forget to specify your intents. This allows your bot to subscribe
# to specific buckets of events. In this example we subscribe to the member
# events like, for example, a user joining the server.
intents = discord.Intents.default()
intents.members = True

# We open a client connection which connects us to Discord.
client = discord.Client(intents=intents)

# The following events are treated by our bot. 

# This event is called when the client is done preparing the data received from Discord.
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following Guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild members:\n - {members}')

# On the on_message event this code is run.
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # If the received message is who? the bot will introduce himself to the channel.
    if message.content == 'who?':
        response = "I'm a bot developed by LTS."
        await message.channel.send(response)
        # We can also send pictures. 
        await message.channel.send( file=discord.File('discord_bot.png') )

    # If someone writes an insult, the bot will blame the user and delete his message.
    if 'bla' in message.content:
        await message.channel.send( 
            f'{message.author.mention} don''t use swear words or you''ll be banned!'
         )
        await message.delete()

# If someone joins the server then this code is run.
@client.event
async def on_member_join(member):
    # We DM the user after joining the server.
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord Guild!'
    )


# Run the client with our generated token.
client.run(TOKEN)