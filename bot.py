import random
from itertools import cycle
import discord
import config
import os
from discord.ext import commands
from discord.ext import commands, tasks
import sys
import asyncio

prefixintial = open("prefix.txt", "r").readline(1)
prefix = prefixintial
intents = discord.Intents.default()
intents.message_content = True
TOKEN = config.token
bot = commands.Bot(command_prefix=prefixintial, intents=intents)
bot.remove_command("help")
client = discord.Client(intents=intents)
status = cycle(['Python', 'доту с онлином', 'feel so alone in bedroom', 'Ю Чэгён няшка <3', 'аниме!!!'])


@bot.event
async def on_ready():
    change_status.start()
    print("Your bot is ready")


@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


@bot.event
async def on_command_error(ctx, err):
    if isinstance(err, discord.ext.commands.errors.CommandNotFound):
        await ctx.send(embed=discord.Embed(title=f"Ошибка!", description=f"Команда не найдена!"))


    elif isinstance(err, discord.ext.commands.errors.BotMissingPermissions):
        await ctx.send(
            embed=discord.Embed(title=f"Ошибка!",
                                description=f"У бота отсутствуют права: {' '.join(err.missing_perms)}\nВыдайте их ему для полного функционирования бота"))


    elif isinstance(err, discord.ext.commands.errors.MissingPermissions):
        await ctx.send(embed=discord.Embed(title=f"Ошибка!", description=f"У вас недостаточно прав для запуска "
                                                                         f"этой команды!"))


    elif isinstance(err, discord.ext.commands.errors.UserInputError):
        await ctx.send(embed=discord.Embed(title=f"Ошибка!",
                                           description=f"Правильное использование команды {ctx.command}({ctx.command.brief}): {ctx.command.usage}"))


    elif isinstance(err, commands.CommandOnCooldown):
        await ctx.send(embed=discord.Embed(
            description=f"У вас еще не прошел кулдаун на команду {ctx.command}!\nПодождите еще {err.retry_after:.2f}"))


    else:
        await ctx.send(embed=discord.Embed(title=f"Ошибка!",
                                           description=f"Произошла неизвестная ошибка: {err}\nПожалуйста, "
                                                       f"свяжитесь с разработчиками для исправления этой "
                                                       f"ошибки"))


@bot.command()
async def bio(ctx):
    bio = discord.Embed(title=f"Привет!", description=f"Я Хаясе Нагаторо, меня написал один "
                                                      f"уебок и теперь издевается надо мной.")
    await ctx.send(embed=bio)


@bot.command()
async def roll(ctx, a: int, b: int):
    rolled = discord.Embed(title=f"Готово!", description=f"{ctx.author.mention}, ваше число: {random.randrange(a, b)}")
    await ctx.send(embed=rolled)


@bot.command()
async def help(ctx):
    help = discord.Embed(title=f"Список команд:", description=config.list_of_commands)
    await ctx.send(embed=help)


@bot.command()
async def kick(ctx, user: discord.Member):
    await user.kick()
    kick = discord.Embed(title=f"Готово!", description=f"Выгнан {user.name}. Выгнал: {ctx.author.mention}")
    await ctx.send(embed=kick)


@bot.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member):
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
    await ctx.send(embed=muted)


@bot.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="muted")
    await member.remove_roles(mutedRole)
    UserRole = discord.utils.get(ctx.guild.roles, name="user")
    await member.add_roles(UserRole)
    unmuted = discord.Embed(title=f"Готово!", description=f"{member.mention} был размьючен!")
    await ctx.send(embed=unmuted)


@bot.command()
async def give_role(ctx, member: discord.Member, *, role: discord.Role):
    await member.add_roles(role)
    gived = discord.Embed(title=f"Готово!", description=f"Выдана роль {role} для {member.mention}.")
    await ctx.send(embed=gived)


@bot.command()
async def remove_role(ctx, member: discord.Member, *, role: discord.Role):
    await member.remove_roles(role)
    removed = discord.Embed(title=f"Готово!", description=f"Снята роль {role} с {member.mention}.")
    await ctx.send(embed=removed)


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
async def unban(ctx, id: int):
    user = await bot.fetch_user(id)
    await ctx.guild.unban(user)
    unbanned = discord.Embed(title=f"Готово!", description=f"{user} был разбанен на сервере.")
    await ctx.send(embed=unbanned)


@bot.command()
async def profile(ctx):
    member = ctx.author
    embed = discord.Embed(title="Профиль пользователя:")
    embed.add_field(name="Имя", value=member.name, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Статус", value=member.status, inline=True)
    embed.set_thumbnail(url=member.avatar)
    await ctx.send(embed=embed)


@bot.command(aliases=["prefix"])
async def set_prefix(ctx, *, prefixsetup=None):
    if prefixsetup is None:
        massnoprefix = await ctx.send(embed=discord.Embed(title=f"Ошибка!", description=f"Вы не указали префикс!"))

    else:
        openPrefixFile = open("prefix.txt", "w")
        writingprefix = openPrefixFile.write(prefixsetup)
        await ctx.send(f"Префикс изменён на > {prefixsetup} < Что бы применить видите {prefixintial}reload")


@bot.command()
async def reload(ctx):
    embed = discord.Embed(title="Перезагрузка", description=f"Начинаю перезагрузку...")
    await ctx.send(embed=embed)
    await bot.close()
    await asyncio.sleep(3)
    await bot.connect()
    embed = discord.Embed(title="Готово!", description=f"Бот успешно перезагружен")
    await ctx.send(embed=embed)


bot.run(TOKEN)
