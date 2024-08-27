import os
import json
import datetime
from dotenv import load_dotenv
from discord import Intents, Client, Message, Poll

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = Intents.default()
intents.members = True
intents.message_content = True
client = Client(intents=intents)

week = datetime.datetime.now().isocalendar()[1]
date = datetime.datetime.now().strftime('%d/%m/%y')
question = f"Uke {week}. Reager på hvilken tier dagens Biltema middag var! ({date})"
poll = Poll(question, datetime.timedelta(hours=24))
active_poll = False

poll.add_answer(text="Baaaaanging!", emoji='🥇')
poll.add_answer(text="Legendarisk", emoji='🟠')
poll.add_answer(text="Utrolig", emoji='🟣')
poll.add_answer(text="Veldig god", emoji='🔵')
poll.add_answer(text="God", emoji='🟢')
poll.add_answer(text="Clas Ohlson", emoji='🟤')

users = {}
with open('app/users.json', 'r') as file:
    users = json.load(file)

async def get_response(user_input):
    if user_is_guru(user_input.author):
        return await cmds(user_input)

async def send_message(message):
    if not message.content:
        print("empty message")
        return

    try:
        response = await get_response(message)
        if not response:
            return 
    
        await message.channel.send(response)
    except Exception as e:
        print(e)

@client.event
async def on_ready():
    print(f'{client.user} is now running')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    print(f'[{message.channel}] {message.author}: "{message.content}"')
    await send_message(message)

def user_is_guru(user):
    for role in user.roles:
        if role.name == "Biltema Guru":
            return True
    return False

async def cmds(message):
    if message.content == '!poll':
        global active_poll, poll
        active_poll = True
        await message.channel.send("", poll=poll)

        if poll.is_finalized() or True:
            active_poll = False
        
        async for i in poll.answers[0].voters():
            print(i)

    if len(message.content.split()) == 2:
        cmd, name = message.content.split()
        
        if not name in users:
            users[name] = {'xp': 0, 'mote': 0}
        
        if cmd == "!xp":
            return f"{name} har {users[name]}xp"

    if len(message.content.split()) == 3:
        cmd, amount, name = message.content.split()
        
        valid = False
        for member in message.guild.members:
            if member.name == name:
                valid = True
        if not valid: 
            print(f"{name} is not a user in the discord")
            return
        if not name in users:
            users[name] = {'xp': 0, 'mote': 0}

        if cmd == "+xp":
            users[name]['xp'] += int(amount)
        
            with open('app/users.json', 'w') as file:
                json.dump(users, file)

            return f"{name} fikk {amount}xp"
        if cmd == "-xp":
            users[name]['xp'] -= int(amount)

            with open('app/users.json', 'w') as file:
                json.dump(users, file)

            return f"{name} mistet {amount}xp"
        if cmd == '+oppmøte':
            users[name]['mote'] += int(amount)

            with open('app/users.json', 'w') as file:
                json.dump(users, file)

            return f"{name} fikk {amount} oppmøte"
        if cmd == '-oppmøte':
            users[name]['mote'] -= int(amount)

            with open('app/users.json', 'w') as file:
                json.dump(users, file)

            return f"{name} mistet {amount} oppmøte"

client.run(token=token)