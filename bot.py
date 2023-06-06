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
status = cycle(['Python', 'доту с онлином', 'feel so alone in bedroom', 'Ю Чэгён няшка <3', 'аниме!!!'])


@bot.event
async def on_ready():
    change_status.start()
    print("Бот готов к работе!")


@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


@client.event
async def on_command_error(ctx, err):
    if isinstance(err, discord.ext.commands.errors.CommandNotFound):
        await ctx.send(embed=discord.Embed(title=f"Ошибка!", description=f"Команда не найдена!"))

    elif isinstance(err, discord.ext.commands.errors.BotMissingPermissions):
        await ctx.send(
            embed=discord.Embed(title=f"Ошибка!",
                                description=f"У бота отсутствуют права: {' '.join(err.missing_perms)}\n"
                                            f"Выдайте их ему для полного функционирования бота"))

    elif isinstance(err, discord.ext.commands.errors.MissingPermissions):
        await ctx.send(embed=discord.Embed(title=f"Ошибка!",
                                                  description=f"У вас недостаточно прав для запуска этой команды!"))

    elif isinstance(err, discord.ext.commands.errors.UserInputError):
        await ctx.send(embed=discord.Embed(title=f"Ошибка!",
                                                  description=f"Правильное использование команды {ctx.command}({ctx.command.brief}): `{ctx.command.usage}`"))

    elif isinstance(err, discord.ext.commands.errors.BadArgument):
        await ctx.send(embed=discord.Embed(title=f"Ошибка!",
                                                  description=f"Правильное использование команды {ctx.command}({ctx.command.brief}): `{ctx.command.usage}`"))

    elif isinstance(err, discord.ext.commands.CommandOnCooldown):
        await ctx.send(embed=discord.Embed(title=f"Ошибка!",
                                                  description=f"У вас еще не прошел кулдаун на команду {ctx.command}!\n"
                                                              f"Подождите еще {err.retry_after:.2f}"))

    else:
        await ctx.send(embed=discord.Embed(title=f"Ошибка!",
                                                  description=f"Произошла неизвестная ошибка: `{err}`\n"
                                                              f"Пожалуйста, свяжитесь с разработчиками для "
                                                              f"исправления этой ошибки"))


@bot.command(name="roll", brief="Выдает случайное число в диапазоне", usage="roll <first_num> <second_num>")
async def roll(ctx, a: int, b: int):
    rolled = discord.Embed(title=f"Готово!", description=f"{ctx.author.mention}, ваше число: {random.randrange(a, b)}")
    await ctx.send(embed=rolled)


@bot.command(name="help", brief="Показать список команд", usage="help")
async def help(ctx):
    help = discord.Embed(title=f"Список команд:", description=config.list_of_commands)
    await ctx.send(embed=help)


@bot.command(name="kick", brief="Выгнать пользователя с сервера", usage="kick <@user>")
@commands.has_permissions(manage_messages=True)
async def kick(ctx, user: discord.Member):
    await user.kick()
    kick = discord.Embed(title=f"Готово!", description=f"**Выгнан(а)** {user.name}. **Выгнал:** {ctx.author.mention}")
    await ctx.send(embed=kick)


@bot.command(name="mute", brief="Запретить пользователю писать (настройте роль и канал)", usage="mute <member>")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="muted")
    muted = discord.Embed(title=f"Готово!", description=f"{member.mention} был(а) замьючен(а)!")
    UserRole = discord.utils.get(ctx.guild.roles, name="user")

    if not mutedRole:
        mutedRole = await guild.create_role(name="muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True,
                                          read_messages=False)

    await member.remove_roles(UserRole)
    await ctx.send(embed=muted)


@bot.command(name="unmute", brief="Разрешить пользователю писать", usage="unmute <member>")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="muted")
    await member.remove_roles(mutedRole)
    UserRole = discord.utils.get(ctx.guild.roles, name="user")
    await member.add_roles(UserRole)
    unmuted = discord.Embed(title=f"Готово!", description=f"{member.mention} был(а) размьючен(а)!")
    await ctx.send(embed=unmuted)


@bot.command(name="give_role", brief="Выдать роль пользователю", usage="give_role <member>")
@commands.has_permissions(manage_messages=True)
async def give_role(ctx, member: discord.Member, *, role: discord.Role):
    await member.add_roles(role)
    gived = discord.Embed(title=f"Готово!", description=f"Выдана роль {role} для {member.mention}.")
    await ctx.send(embed=gived)


@bot.command(name="remove_role", brief="Снять роль с пользователя", usage="remove_role <member>")
@commands.has_permissions(manage_messages=True)
async def remove_role(ctx, member: discord.Member, *, role: discord.Role):
    await member.remove_roles(role)
    removed = discord.Embed(title=f"Готово!", description=f"Снята роль {role} с {member.mention}.")
    await ctx.send(embed=removed)


@bot.command(name="clear", brief="Очистить чат от сообщений.", usage="clear <amount>")
async def clear(ctx, amount: int):
    cleared = discord.Embed(title=f"Готово!", description=f"{ctx.author.mention} очистил(а) **{amount}** сообщений.")
    await ctx.channel.purge(limit=amount)
    await ctx.send(embed=cleared)


@bot.command(name="ban", brief="Забанить пользователя на сервере", usage="ban <@user>")
@commands.has_permissions(manage_messages=True)
async def ban(ctx, member: discord.Member):
    await member.ban()
    banned = discord.Embed(title=f"Готово!", description=f"{member} был **забанен** на сервере.")
    await ctx.send(embed=banned)


@bot.command(name="unban", brief="Разбанить пользователя на сервере", usage="ban <user_id>")
@commands.has_permissions(manage_messages=True)
async def unban(ctx, id: int):
    user = await bot.fetch_user(id)
    await ctx.guild.unban(user)
    unbanned = discord.Embed(title=f"Готово!", description=f"{user} был **разбанен** на сервере.")
    await ctx.send(embed=unbanned)


@bot.command(name="profile", brief="Показать профиль пользователя", usage="give_role <member>")
async def profile(ctx):
    member = ctx.author
    embed = discord.Embed(title="Профиль пользователя:")
    embed.add_field(name="Имя", value=member.name, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Статус", value=member.status, inline=True)
    embed.set_thumbnail(url=member.avatar)
    await ctx.send(embed=embed)


@bot.command(name="set_prefix", brief="Сменить префикс бота", usage="set_prefix <new_prefix>")
@commands.has_permissions(manage_messages=True)
async def set_prefix(ctx, *, prefixsetup=None):
    if prefixsetup is None:
        await ctx.send(embed=discord.Embed(title=f"Ошибка!", description=f"Вы не указали префикс!"))

    else:
        openPrefixFile = open("prefix.txt", "w")
        openPrefixFile.write(prefixsetup)
        await ctx.send(embed=discord.Embed(title="Готово!", description=f"Префикс изменён на > ``{prefixsetup}`` "
                                                                        f"< Что бы применить видите {prefixintial}restart"))


def restart_bot():
    subprocess.Popen([sys.executable, 'bot.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
    sys.exit()


@bot.command(name="restart", brief="Перезапустить бота", usage="restart")
async def restart(ctx):
    embed1 = discord.Embed(title="Готово!", description=f"Перезагружаюсь...")
    await ctx.send(embed=embed1)
    restart_bot()


bot.run(TOKEN)
