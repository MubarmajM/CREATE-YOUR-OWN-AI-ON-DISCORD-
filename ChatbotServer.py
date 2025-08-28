import discord
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import json
from fixer import simple_fixer
import string
bot = ChatBot("Bot")



# bot.storage.drop()
with open("ChatbotData.json") as f:
    d=json.load(f)

trainer = ListTrainer(bot)

data = []
for datas in d:
    data.append(datas.lower())
trainer.train(data)

# Variabel intents menyimpan hak istimewa bot
intents = discord.Intents.default()
# Mengaktifkan hak istimewa message-reading
intents.message_content = True
# Membuat bot di variabel klien dan mentransfernya hak istimewa
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have entered as {client.user}')

@client.event
async def on_message(message):
    print(f"Received message: {message.content} from {message.author}")
    if message.author == client.user:
        return
    # if message.content.startswith('$halo'):
    #     await message.channel.send("HELLO!")
    # else:
    #     await message.channel.send(message.content)

    ask = message.content.lower()
    if ask == "<[clear-memory]>":
        bot.storage.drop()
        trainer.train(data)
        await message.channel.send("MEMORY CLEANED")
    elif ask in data:
        ans = bot.get_response(ask)
        await message.channel.send(ans)
    else:
        ans = bot.get_response(simple_fixer(ask,data))
        await message.channel.send(ans)

client.run("YOUR TOKEN HERE")