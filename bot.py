import random
from itertools import cycle
from discord.ext import tasks
import discord
from discord.ext import commands
import config
from flask import Flask

intents = discord.Intents.default()
intents.message_content = True
TOKEN = config.token
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command("help")
client = discord.Client(intents=intents)
status = cycle(['Python', 'доту с онлином ', 'Feel so alone in bedroom'])
app = Flask('')


@bot.event
async def on_ready():
    change_status.start()
    print("Your bot is ready")


@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


@bot.command(pass_context=True)
async def repeat(ctx, arg):
    await ctx.reply(arg)


@bot.command()
async def bio(ctx):
    await ctx.reply(config.bio_text)


@bot.command()
async def roll(ctx, a: int, b: int):
    await ctx.reply(random.randrange(a, b))


@bot.command()
async def help(ctx):
    help = discord.Embed(title=f"Список команд:", description=config.list_of_commands)
    await ctx.reply(embed=help)


@bot.command()
async def kick(ctx, user: discord.Member):
    await user.kick()
    kick = discord.Embed(title=f"Готово!", description=f"Выгнан {user.name}. Выгнал: {ctx.author.mention}")
    await ctx.reply(embed=kick)


@bot.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="muted")
    muted = discord.Embed(title=f"Готово!", description=f"{member.mention} был замьючен!")
    UserRole = discord.utils.get(ctx.guild.roles, name="user")

    if not mutedRole:
        mutedRole = await guild.create_role(name="muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True,
                                          read_messages=False)

    await member.remove_roles(UserRole)
    await member.add_roles(mutedRole, reason=reason)
    await ctx.reply(embed=muted)


@bot.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="muted")
    await member.remove_roles(mutedRole)
    UserRole = discord.utils.get(ctx.guild.roles, name="user")
    await member.add_roles(UserRole)
    unmuted = discord.Embed(title=f"Готово!", description=f"{member.mention} был размьючен!")
    await ctx.reply(embed=unmuted)


@bot.command()
async def give_role(ctx, member: discord.Member, *, role: discord.Role):
    await member.add_roles(role)
    gived = discord.Embed(title=f"Готово!", description=f"Выдана роль {role} для {member.mention}.")
    await ctx.reply(embed=gived)


@bot.command()
async def remove_role(ctx, member: discord.Member, *, role: discord.Role):
    await member.remove_roles(role)
    removed = discord.Embed(title=f"Готово!", description=f"Снята роль {role} с {member.mention}.")
    await ctx.reply(embed=removed)


@bot.command()
async def clear(ctx, amount: int):
    cleared = discord.Embed(title=f"Готово!", description=f"{ctx.author.mention} очистил(а) **{amount}** сообщений.")
    await ctx.channel.purge(limit=amount)
    await ctx.send(embed=cleared)


@bot.command()
async def ban(ctx, member: discord.Member):
    await member.ban()
    banned = discord.Embed(title=f"Готово!", description=f"{member} был забанен на сервере.")
    await ctx.send(embed=banned)


@bot.command()
async def unban(ctx, *, member):
    banned_users = ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user} был разбанен с сервера.')
            return
    unbanned = discord.Embed(title=f"Готово!", description=f"{member} был разбанен на сервере.")
    await ctx.send(embed=unbanned)


@bot.command()
async def profile(ctx):
    member = ctx.author
    embed = discord.Embed(title="Профиль пользователя", description=member.mention)
    embed.add_field(name="Имя", value=member.name, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Статус", value=member.status, inline=True)
    embed.set_thumbnail(url=member.avatar)
    await ctx.reply(embed=embed)


bot.run(TOKEN)