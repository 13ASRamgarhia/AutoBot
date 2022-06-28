import discord
import random
import discord.utils
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
autobot = commands.Bot(command_prefix = '.',intents=intents)
autobot.remove_command('help')

#1.AutoBot is Online
@autobot.event
async def on_ready():
    print("="*40)
    print('AutoBot 2.0 is Online...')
    print("-"*40)
    print('Discord username: {}'.format(autobot.user))
    print('Discord ID      : {}'.format(autobot.user.id))
    print("-"*40)
    activity = discord.Game(name="Test", type=3)
    await autobot.change_presence(status=discord.Status.idle, activity=activity)
    print('Status updated')
    print("="*40)


#2.Latency
@autobot.command()
async def ping(ctx):
    await ctx.send(f"It's {round(autobot.latency * 1000)}ms")


#3.Ask (fun command)
@autobot.command(aliases = ['askme'])
async def ask(ctx, *, question):
    responses = ['It is certain.',
                 'It is decidedly so.',
                 'Without a doubt.',
                 'No doubt dear',
                 'Yes, definately',
                 'As I see it, yes',
                 'Most likely',
                 'Yes !',
                 'Signs point to yes',
                 'Ask again later',
                 'Better not tell now',
                 'Cannot predict now',
                 'Ask again !',
                 'My reply is no :)',
                 'My sources say No :)',
                 'Very doubtful']
    await ctx.send(f'Question: {question}\nAnswer  : {random.choice(responses)}')


#4.clear (to clear an amount of messages from a channel)
@autobot.command()
@commands.has_permissions(administrator = True)
async def clear(ctx, amount = 2):
    await ctx.channel.purge(limit = amount)


#5.echo (to announce something or send msg through bot)
@autobot.command()
async def echo(ctx):
    channel = autobot.get_channel(861777235551322135)
    msg = ctx.message.content.split()
    output = ''
    for word in msg[1:]:
        output += word
        output += ' '
    await channel.send(output)


#6.Shutdown command
@autobot.command()
@commands.has_permissions(administrator = True)
async def signoff(ctx):
    await ctx.send(f'Signing off :wave:')
    await autobot.logout()


#7.Message logs in console
@autobot.event
async def on_message(message):
    author = message.author
    content = message.content
    print('{}: {}'.format(author, content))


#8.Message delete logs in msg-del-logs channel
@autobot.event
async def on_message_delete(message):
    author = message.author
    content = message.content
    channel1 = message.channel.id
    channel = autobot.get_channel(861796580151918613)
    embed = discord.Embed(
        colour=discord.Colour.red(),
        description=f"**Message deleted by {author.mention} in <#{channel1}>**\n{message.content}"
    )
    embed.set_author(name=message.author,icon_url=author.avatar_url)
    embed.set_footer(text=f"Author ID: {author.id} | Message ID: {message.id}")
    await channel.send(embed=embed)
    await autobot.process_commands(message)


#9.Autorole
@autobot.event
async def on_member_join(member,message):
    role = discord.utils.get(member.server.roles, id = "861779189913223188")
    channel = autobot.get_channel(861838401178435584)
    await member.add_roles(role)
    await channel.send(f"{role} was given to {member}")
    await autobot.process_commands(message)


#10.Kick member
@autobot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx,member : discord.Member):
    await member.kick()
    await ctx.message.delete()
    await ctx.send(f'{member.display_name} has been kicked')


#11.Ban member
@autobot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx,member : discord.Member):
    await member.ban()
    await ctx.message.delete()
    await ctx.send(f'{member.display_name} has been banned')


#12.Unban member
@autobot.command(brief = "Unban a member. Requires Admin")
@commands.has_permissions(ban_members=True)
async def unban(ctx,*,member):
    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split('#')

    for banned_entry in banned_users:
        user = banned_entry.user

        if(user.name, user.discriminator)==(member_name,member_disc):
            await ctx.guild.unban(user)
            await ctx.send(member_name +" has been unbanned!")
            return

        else:
            await ctx.send(member_name +" was not found!")


#13.Music Player
@autobot.command()
async def music(ctx):
    await ctx.send("Hey! What do wanna listen buddy :slight_smile:")
    channel = autobot.get_channel(862393702378242098)
    await channel.connect()


@autobot.command(aliases=['p'])
async def play(ctx):
    await ctx.send('Still not ready to play music mate :no_mouth:')

@autobot.command(aliases=['dc'])
async def disconnect(ctx):
    await ctx.send("See ya :wave:")
    await ctx.voice_client.disconnect()


#14.Blacklisted system
with open('bl.txt') as file:
    file = file.read().split()

@autobot.event
async def on_message(message):
    channel = autobot.get_channel(861777235551322135)
    mybot = autobot.get_user(862032740563943514)
    if not message.author == mybot:
        for badword in file:
            if badword in message.content.lower():
                await message.delete()
                await channel.send(f'Mind your language {message.author.mention} :angry:')
    await autobot.process_commands(message)


#15.Custom help command
@autobot.command()
async def help(ctx):
    author = ctx.message.author
    channel = ctx.channel
    embed1 = discord.Embed(
        colour = discord.Colour.orange(),
        title = "Help Center",
        description = "Following are General commands for AutoBot"
    )
    embed1.set_thumbnail(url = "https://cdn.discordapp.com/attachments/725901296929865748/862520467385483264/x65L0xe.jpg")
    embed1.add_field(name = "\n.ping", value = "Tells Latency of AutoBot", inline = True)
    embed1.add_field(name = "\n.ask", value = "Ask anything to AutoBot for fun", inline = True)
    embed1.add_field(name = "\n.clear", value = "Used to mass delete messages", inline = True)
    embed1.add_field(name = "\n.echo", value = "Used to announce something through AutoBot", inline = True)
    embed1.add_field(name = "\n.developer", value = "Know more about developers", inline = True)
    embed1.add_field(name = "\n.Console Logs", value = "Console will have logs for member join/leave", inline = True)
    embed1.add_field(name="\n.kick", value=".kick <@user>\nKicks user from Server", inline=True)
    embed1.add_field(name="\n.ban", value=".ban <@user>\nBans user from Server", inline=True)
    embed1.add_field(name="\n.signoff", value="Used to shutdown the AutoBot", inline=True)

    await author.send(embed = embed1)
    await channel.send(f'{ctx.author.mention} Check your DM')


#16.Developer Info
@autobot.command(aliases = ['d'])
async def developer(ctx):
    author = ctx.message.author
    channel = ctx.channel
    embed1 = discord.Embed(
        colour=discord.Colour.orange(),
        title="Developer Info",
        description="There are three developers for AutoBot 2.0"
    )
    embed1.set_thumbnail(url="https://cdn.discordapp.com/attachments/725901296929865748/862612725757902858/aa.png")
    embed1.add_field(name = "Amandeep Singh", value = "\n**Branch:** BTech CSE\n**Sem.:** 8th Sem\n**Roll no.:** 183005", inline = True)
    embed1.add_field(name = "Sarthak Rawal", value = "\n**Branch:** BTech CSE\n**Sem.:** 8th Sem\n**Roll no.:** 183046", inline = True)
    embed1.add_field(name = "Sanjay Rao", value = "\n**Branch:** BTech CSE\n**Sem.:** 8th Sem\n**Roll no.:** 183044", inline = True)


    await author.send(embed = embed1)
    await channel.send(f'{ctx.author.mention} Check your DM')


#17.Member join
@autobot.event
async def on_member_join(member):
    channel = autobot.get_channel(863379917080100925)
    logs_channel = autobot.get_channel(862034648673419294)
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        title="Welcome",
        description="Hy {}, Welcome to AutoBot Test Server".format(member.mention)
    )
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_image(url="https://media.discordapp.net/attachments/556465274036158484/710907565206274048/ezgif-1-a2a2e7173d80-1.gif?width=500&height=3")

    await channel.send(embed=embed)
    await logs_channel.send(f"{member.mention} just joined AutoBot Test")


#18.Member left
@autobot.event
async def on_member_remove(member):
    channel = autobot.get_channel(863386368100007936)
    await channel.send(f'{member} has left the server')


autobot.run("")

