import discord
import settings

from events.buttons import button_handler
from events.message import message_handler
from events.reaction import reaction_change_handler
from events.voice import voice_handler
from events.channel_archive import ArchEventsLoop

from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def setup_hook():
    extensions = [
        "cogs.seen_settings",
        "cogs.zamowieniegrafik",
        "cogs.role",
        "cogs.embedy",
        "cogs.channelarchive_settings"
    ]
    
    for ext in extensions:
        try:
            await bot.load_extension(ext)
        except Exception as e:
            print(f"Failed to load extension {ext}: {e}")

    try:
        guild = discord.Object(id=settings.main_guild_id)
        await bot.tree.sync(guild=guild)
        print("Application commands synchronized.")
        commands_list = [command.name for command in bot.tree.get_commands(guild=guild)]
        print(f"Registered commands in guild: {settings.main_guild_id}: {commands_list}")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

bot.setup_hook = setup_hook

@bot.command()
@commands.is_owner()
async def clear_all_commands(ctx):
    guild = discord.Object(id=settings.main_guild_id)
    bot.tree.clear_commands(guild=guild)
    await bot.tree.sync(guild=guild)
    print("All commands cleared and synced.")

@bot.event
async def on_message(message):
    await message_handler(bot, message)
    await bot.process_commands(message)

@bot.event
async def on_interaction(interaction):
    await button_handler(bot, interaction)

@bot.event
async def on_raw_reaction_add(payload):
    await reaction_change_handler(bot, payload)

@bot.event
async def on_raw_reaction_remove(payload):
    await reaction_change_handler(bot, payload)

@bot.event
async def on_voice_state_update(member, before, after):
    await voice_handler(bot, member, before, after)

@bot.event
async def on_ready():
    print("Commands loaded.")
    print(f"Logged in as {bot.user.name} in guild: {settings.main_guild_id}")
    
    if not hasattr(bot, 'arch_loop_started'):
        try:
            ArchEventsLoop(bot).archive_events.start()
            bot.arch_loop_started = True
        except Exception as e:
            print(f"Failed to start ArchEventsLoop: {e}")

bot.run(settings.client_token)
