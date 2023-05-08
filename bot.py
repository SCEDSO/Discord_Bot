from discord.ext import commands, tasks
import discord
from dataclasses import dataclass
import datetime
from hidden import TOKEN

BOT_TOKEN = TOKEN
# CHANNEL_ID = 1101796035392704592
CHANNEL_ID = 1104934474715775082
MAX_SESSION_TIME_MINUTES = 45

@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0

bot = commands.Bot(command_prefix = '!', intents = discord.Intents.all())
session = Session()

@bot.event
async def on_ready():
    print("Hello! Study bot is ready!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello! Study bot is ready!")

@tasks.loop(minutes = MAX_SESSION_TIME_MINUTES, count = 2)
async def break_reminder():

    # Ignore the first execution of this command
    if break_reminder.current_loop == 0:
        return

    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"**Take a break!** You've been studying for {MAX_SESSION_TIME_MINUTES} minutes.")

@bot.command()
async def add(ctx, *arr) :
    result = 0
    for i in arr:
        result += int(i)
    
    await ctx.send(f"Result: {result}")

@bot.command()
async def start(ctx):
    if session.is_active:
        await ctx.send("A session is already active!")
        return

    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()
    readable_time = ctx.message.created_at.strftime("%H:%M:%S")
    break_reminder.start()
    await ctx.send(f"New session started at {readable_time}.")

@bot.command()
async def end(ctx):
    if not session.is_active:
        await ctx.send("No session is active!")
        return

    session.is_active = False
    end_time = ctx.message.created_at.timestamp()
    duration = end_time - session.start_time
    readable_duration = str(datetime.timedelta(seconds = duration))
    break_reminder.stop()
    await ctx.send(f"Session ended after {readable_duration}.")


bot.run(BOT_TOKEN)