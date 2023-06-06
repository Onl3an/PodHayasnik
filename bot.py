import random
import subprocess
import sys
from itertools import cycle
import discord
import config
from discord.ext import commands, tasks

prefixintial = open("prefix.txt", "r").readline(1)
prefix = prefixintial
intents = discord.Intents.default()
intents.message_content = True
TOKEN = config.token
bot = commands.Bot(command_prefix=prefixintial, intents=intents)
bot.remove_command("help")
client = discord.Client(intents=intents)
status = cycle(['Python', 'доту с онлином', 'Ю Чэгён няшка <3', 'аниме!!!', 'ожидание новой главы манги'])


@bot.event
async def on_ready():
    change_status.start()
    print("Бот готов к работе!")


@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


@bot.event
async def on_command_error(ctx, err):
    if isinstance(err, discord.ext.commands.errors.CommandNotFound):
        await ctx.send(embed=discord.Embed(title=f"Ошибка!", description=f"Команда **не найден!**", color=0xFF0000))

    elif isinstance(err, discord.ext.commands.errors.MissingPermissions):
        await ctx.send(embed=discord.Embed(title=f"Ошибка!",
                                           description=f"У вас **недостаточно прав** для запуска этой команды!",
                                           color=0xFF0000))

    elif isinstance(err, discord.ext.commands.errors.UserInputError):
        await ctx.send(embed=discord.Embed(title=f"Ошибка!",
                                           description=f"Правильное использование команды **{ctx.command}**"
                                                       f"({ctx.command.brief}): `{ctx.command.usage}`", color=0xFF0000))

    elif isinstance(err, discord.ext.commands.errors.BadArgument):
        await ctx.send(embed=discord.Embed(title=f"Ошибка!",
                                           description=f"Правильное использование команды **{ctx.command}**"
                                                       f"({ctx.command.brief}): `{ctx.command.usage}`", color=0xFF0000))

    elif isinstance(err, discord.ext.commands.CommandOnCooldown):
        await ctx.send(embed=discord.Embed(title=f"Ошибка!",
                                           description=f"У вас еще **не прошел кулдаун** на команду {ctx.command}!\n"
                                                       f"Подождите еще {err.retry_after:.2f}", color=0xFF0000))

    else:
        await ctx.send(embed=discord.Embed(title=f"Ошибка!",
                                           description=f"Произошла **неизвестная ошибка:** `{err}`\n"
                                                       f"Пожалуйста, свяжитесь с разработчиками для "
                                                       f"исправления этой ошибки", color=0xFF0000))


@bot.command(name="roll", brief="Выдает случайное число в диапазоне", usage="roll <first_num> <second_num>")
async def roll(ctx, a: int, b: int):
    rolled = discord.Embed(title=f"Готово!", description=f"{ctx.author.mention}, ваше число: {random.randrange(a, b)}",
                           color=0x008000)
    await ctx.send(embed=rolled)


@bot.command(name="help", brief="Показать список команд", usage="help")
async def help(ctx):
    helped = discord.Embed(title=f"Список команд:", description=config.list_of_commands, color=0x008000)
    await ctx.send(embed=helped)


@bot.command(name="kick", brief="Выгнать пользователя с сервера", usage="kick <@user>")
@commands.has_permissions(administrator=True)
async def kick(ctx, user: discord.Member):
    await user.kick()
    kicked = discord.Embed(title=f"Готово!", description=f"**Выгнан(а)** {user.name}. **Выгнал:** {ctx.author.mention}", color=0x008000)
    await ctx.send(embed=kicked)


@bot.command(name="mute", brief="Запретить пользователю писать.", usage="mute <@user>")
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name='muted')
    await member.add_roles(role)
    muted = discord.Embed(title="Готово!", description=f"{member.mention} был(а) замьючен(а)!", color=0x008000)
    await ctx.send(embed=muted)


@bot.command(name="unmute", brief="Разрешить пользователю писать", usage="unmute <@user>")
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="muted")
    await member.remove_roles(mutedRole)
    unmuted = discord.Embed(title=f"Готово!", description=f"{member.mention} был(а) размьючен(а)!", color=0x008000)
    await ctx.send(embed=unmuted)


@bot.command(name="give_role", brief="Выдать роль пользователю", usage="give_role <@user> <@role>")
@commands.has_permissions(administrator=True)
async def give_role(ctx, member: discord.Member, *, role: discord.Role):
    await member.add_roles(role)
    gived = discord.Embed(title=f"Готово!", description=f"Выдана роль {role} для {member.mention}.", color=0x008000)
    await ctx.send(embed=gived)


@bot.command(name="remove_role", brief="Снять роль с пользователя", usage="remove_role <@user> <@role>")
@commands.has_permissions(administrator=True)
async def remove_role(ctx, member: discord.Member, *, role: discord.Role):
    await member.remove_roles(role)
    removed = discord.Embed(title=f"Готово!", description=f"Снята роль {role} с {member.mention}.", color=0x008000)
    await ctx.send(embed=removed)


@bot.command(name="clear", brief="Очистить чат от сообщений.", usage="clear <amount>")
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: int):
    cleared = discord.Embed(title=f"Готово!", description=f"{ctx.author.mention} очистил(а) **{amount}** сообщений.", color=0x008000)
    await ctx.channel.purge(limit=amount)
    await ctx.send(embed=cleared)


@bot.command(name="ban", brief="Забанить пользователя на сервере", usage="ban <@user>")
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member):
    await member.ban()
    banned = discord.Embed(title=f"Готово!", description=f"{member} был **забанен(а)** на сервере.", color=0x008000)
    await ctx.send(embed=banned)


@bot.command(name="unban", brief="Разбанить пользователя на сервере", usage="ban <user_id>")
@commands.has_permissions(administrator=True)
async def unban(ctx, id: int):
    user = await bot.fetch_user(id)
    await ctx.guild.unban(user)
    unbanned = discord.Embed(title=f"Готово!", description=f"{user} был **разбанен(а)** на сервере.", color=0x008000)
    await ctx.send(embed=unbanned)


@bot.command(name="profile", brief="Показать профиль пользователя", usage="give_role <@user>")
async def profile(ctx):
    member = ctx.author
    embed = discord.Embed(title="Профиль пользователя:", color=0x008000)
    embed.add_field(name="Имя", value=member.name, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Статус", value=member.status, inline=True)
    embed.set_thumbnail(url=member.avatar)
    await ctx.send(embed=embed)


@bot.command(name="set_prefix", brief="Сменить префикс бота", usage="set_prefix <new_prefix>")
@commands.has_permissions(administrator=True)
async def set_prefix(ctx, *, prefixsetup=None):
    if prefixsetup is None:
        await ctx.send(embed=discord.Embed(title=f"Ошибка!", description=f"Вы не указали префикс!", color=0x008000))

    else:
        openPrefixFile = open("prefix.txt", "w")
        openPrefixFile.write(prefixsetup)
        await ctx.send(embed=discord.Embed(title="Готово!", description=f"Префикс изменён на > ``{prefixsetup}`` "
                                                                        f"< Что бы применить видите "
                                                                        f"{prefixintial}restart", color=0x008000))


def restart_bot():
    subprocess.Popen([sys.executable, 'bot.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
    sys.exit()


@bot.command(name="restart", brief="Перезапустить бота", usage="restart")
@commands.has_permissions(administrator=True)
async def restart(ctx):
    embed1 = discord.Embed(title="Готово!", description=f"Перезагружаюсь...", color=0x008000)
    await ctx.send(embed=embed1)
    restart_bot()


bot.run(TOKEN)
