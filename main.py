import discord
import random
import time
import asyncio
from decimal import Decimal
from discord.ext import commands

leaderboard = {}
roulette_black = ['2', '4', '6', '8', '10', '11', '13', '15', '17', '20', '22', '24', '26', '28', '29', '31', '33', '35']
roulette_red = ['1', '3', '5', '7', '9', '12', '14', '16', '18', '19', '21', '23', '25', '27', '30', '32', '34', '36']
roulette_green = ['0', '00']
roulette_even = ['2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30', '32', '34', '36']
roulette_onetoeiteen = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18']
roulette_firsttwelve = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
roulette_secondtwelve = ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']
roulette_thirdwelve = ['25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36']
users = {}
statslist = []
statsdic = {}
mods = []
userlist = []
bets = []
messagecode = 0
nmbwin = 0
clrwin = 0
eowin = 0
first12 = 0
second12 = 0
third12 = 0
randomwin = 0
farbe = '0'
zahl = -1
error = 0
bet = 0.0
won = 0.0
accepting_bets = False

tip_of_the_week = '17'
minimumbet = 0.1
maximumbet = 500.0
prefix = '/'


bot = commands.Bot(command_prefix=prefix)
bot.remove_command("help")


try:
    with open("users.txt", "r") as users_file:
        for line in users_file:
            if line.strip():
                user, wealth = line.strip().split(':')
                users[user] = wealth
                userlist.append(user + ':' + users[user])
        users_file.close()

    with open("mods.txt", "r") as mods_file:
        f = mods_file.read()
        mods = f.splitlines()
        users_file.close()

    with open("stats.txt", "r") as stats_file:
        for line in stats_file:
            if line.strip():
                user, won_lost = line.strip().split(':')
                statsdic[user] = won_lost
                won_lost.split('|')
                won = int(won_lost[0])
                lost = int(won_lost[2])
                statslist.append(user + ':' + statsdic[user])
        stats_file.close()

except FileNotFoundError:
    users = {}
    mods = {}
    statsdic = {}


def add_user():
    global messagecode

    with open("users.txt", "r") as users_file:
        for line in users_file:
            if line.strip():
                user, wealth = line.strip().split(':')
                users[user] = wealth
                userlist.append(user + ':' + users[user])
        users_file.close()
    if user in users:
        messagecode = 2
        return
    else:
        users_file.writelines(str(user) + ":0.0" + "\n")
        users_file.flush()
        messagecode = 1
        users_file.close()

    b = open("stats.txt", "a")

    if user in statsdic:
        messagecode = 2
    else:
        b.writelines(str(user) + "0.0|0.0" + "\n")
        b.flush()
        messagecode = 1
        b.close()

    statsdic.clear()

    with open("stats.txt", "r") as stats_file:
        for line in stats_file:
            if line.strip():
                user, won_lost = line.strip().split(':')
                statsdic[user] = won_lost
                won_lost.split('|')
                won = int(won_lost[0])
                lost = int(won_lost[2])
                statslist.append(user + ':' + statsdic[user])
        stats_file.close()

    users.clear()

    with open("users.txt", "r") as users_file:
        for line in users_file:
            if line.strip():
                user, wealth = line.strip().split(':')
                users[user] = wealth
                userlist.append(user + ':' + users[user])
        users_file.close()


def add_mod():
    global mods

    f = open("mods.txt", "a")
    f.write(new_mod + '\n')
    f.flush()
    f.close()

    mods = []

    with open("mods.txt", "r") as mods_file:
        f = mods_file.read()
        mods = f.splitlines()
        users_file.close()


def remove_mod():
    mods.remove(remove_mod())
    with open("mods.txt", "w") as mods_file:
            mods_file.write("\n".join(mods))
    mods_file.close()

def get_playerstats():
    global playerstats
    global won
    global lost
    global username

    statsdic.clear()

    with open("stats.txt", "r") as stats_file:
        for line in stats_file:
            if line.strip():
                user, won_lost = line.strip().split(':')
                statsdic[user] = won_lost
                won_lost.split('|')
                won = int(won_lost[0])
                lost = int(won_lost[2])
                statslist.append(user + ':' + statsdic[user])
        stats_file.close()

    playerstats = statsdic[str(username)].split('|')
    won = playerstats[0]
    lost = playerstats[1]

def get_balance():
    global balance

    balance = users[username]

def addlose(added_lost):
    global won
    global lost
    global player
    global player_id
    global bet
    global added_balance
    global lost_balance


    playerstats = statsdic[str(player_id)].split('|')
    newbalance = Decimal(float(users[str(player_id)]) - lost_balance)
    newbalance = round(newbalance, 2)


    lost = Decimal(float(added_lost) + float(playerstats[1]))
    lost = round(lost,2)
    playerstats[0] = won
    playerstats[1] = lost
    playerstats = str(playerstats[0]) + '|' + str(playerstats[1])

    users[str(player_id)] = newbalance
    with open("users.txt", "w") as users_file:
        for k in users.keys():
            users_file.write("{}:{}\n".format(k, users[k]))
        users_file.close()

    statsdic[player_id] = playerstats
    with open("stats.txt", "w") as stats_file:
        for k in users.keys():
            stats_file.write("{}:{}\n".format(k, statsdic[k]))
    stats_file.close()

def addwin(added_won):
    global won
    global lost
    global player
    global player_id
    global bet
    global added_balance
    global lost_balance

    print(added_balance)
    playerstats = statsdic[str(player_id)].split('|')
    newbalance = Decimal(float(users[str(player_id)]) + added_balance)
    newbalance = round(newbalance,2)

    won = Decimal(float(added_won) + float(playerstats[0]))
    won = round(won,2)
    playerstats[0] = won
    playerstats[1] = lost
    playerstats = str(playerstats[0]) + '|' + str(playerstats[1])

    users[str(player_id)] = newbalance
    with open("users.txt", "w") as users_file:
        for k in users.keys():
            users_file.write("{}:{}\n".format(k, users[k]))
        users_file.close()

    statsdic[player_id] = playerstats
    with open("stats.txt", "w") as stats_file:
        for k in users.keys():
            stats_file.write("{}:{}\n".format(k, statsdic[k]))
    stats_file.close()


async def farbeninput():
    global farbe
    global tip
    global error

    farbe = tip.lower()
    if farbe == 'black' or farbe == 'schwarz':
        farbe = -1
    elif farbe == 'red' or farbe == 'rot':
        farbe = -2
    elif farbe == 'green' or farbe == 'grün':
        farbe = -3
    else:
        error = 1


async def zahlentest(ctx):
    global nmbwin
    global result
    global zahl

    if str(result) == str(zahl):
        nmbwin = 1
        print('Won Zahlentest')
        await resulttest(ctx)
        return
    else:
        nmbwin = -1
        print('Lost Zahlentest')
        await resulttest(ctx)
        return


async def farbentest(ctx):
    global clrwin
    global farbe
    global result

    if farbe == -1 and str(result) in roulette_black:
        clrwin = 1
        print('Won Farbentest')
        await resulttest(ctx)
        return
    elif farbe == -1 and str(result) not in roulette_black:
        clrwin = -1
        print('Lost Farbentest')
        await resulttest(ctx)
        return
    if farbe == -2 and str(result) in roulette_red:
        clrwin = 1
        print('Won Farbentest')
        await resulttest(ctx)
        return
    elif farbe == -2 and str(result) not in roulette_red:
        clrwin = -1
        print('Lost Farbentest')
        await resulttest(ctx)
        return
    elif farbe == -3 and str(result) in roulette_green:
        clrwin = 1
        print('Won Farbentest')
        await resulttest(ctx)
        return
    elif farbe == -3 and str(result) not in roulette_green:
        clrwin = -1
        print('Lost Farbentest')
        await resulttest(ctx)
        return
    else:
        clrwin = -1
        print('No Color')
        await resulttest(ctx)
        return


async def gerade_ungerade(ctx):
    global result
    global zahl
    global eowin
    global error

    try:
        if tip == 'odd':
            if str(result) not in roulette_even and not '0' and not '00':
                eowin = 1
                error = 0
                print('Won Odd or Even')
                await resulttest(ctx)
                return
            if str(result) in roulette_even and not '0' and not '00':
                eowin = -1
                error = 0
                print('Lost Odd or Even')
                await resulttest(ctx)
                return
        if tip == 'even':
            if str(result) in roulette_even:
                eowin = 1
                error = 0
                print('Won Odd or Even')
                await resulttest(ctx)
                return
            if str(result) not in roulette_even:
                eowin = -1
                error = 0
                print('Lost Odd or Even')
                await resulttest(ctx)
                return
    except:
        error = 1


async def firsttwelve(ctx):
    global first12
    global result

    if str(result) in roulette_firsttwelve:
        first12 = 1
        print('Won First12')
    else:
        first12 = 0
        print('Lost First12')
    await resulttest(ctx)
    return


async def secondtwelve(ctx):
    global second12
    global result

    if str(result) in roulette_secondtwelve:
        second12 = 1
        print('Won Second12')
    else:
        second12 = 0
        print('Lost Second12')
    await resulttest(ctx)
    return


async def thirdtwelve(ctx):
    global third12
    global result

    if str(result) in roulette_thirdwelve:
        third12 = 1
        print('Won Third12')
    else:
        third12 = 0
        print('Lost Third12')
    await resulttest(ctx)
    return


async def random_tip(ctx):
    global tip
    global result
    global randomwin
    global error
    global zahl

    if tip == 'random' or tip == 'zufall':
        tip = str(random.randint(-1, 36))
        if tip == '-1':
            tip = '00'

        print('Tip: ' + tip)
        if tip == str(result):
            randomwin = 1
            error = 0
            print('Won random tip')
            await resulttest(ctx)
            return
        else:
            randomwin = -1
            error = 0
            print('Lost random tip')
            await resulttest(ctx)
            return


async def resulttest(ctx):
    global player
    global player_id
    global nmbwin
    global clrwin
    global win
    global eowin
    global first12
    global second12
    global third12
    global result
    global randomwin
    global tip
    global won
    global lost
    global added_balance
    global lost_balance
    global bet

    if str(result) in roulette_black:
        farbe_result = 'black'
    elif str(result) in roulette_green:
        farbe_result = 'green'
    else:
        farbe_result = 'red'

    if nmbwin == 1:
        await ctx.channel.send(
            'Du hast gewonnen! ' + '(' + str(result) + ' / ' + str(farbe_result) + ')' + ' Dein Tipp: ' + str(
                tip))
        print("----------------------------------------------------------")
        added_won = (bet * 35) - bet
        added_balance = (bet * 35) - bet
        addwin(added_won)
        nmbwin = 0
        return
    elif clrwin == 1:
        await ctx.channel.send(
            'Du hast gewonnen! ' + '(' + str(result) + ' / ' + str(farbe_result) + ')' + ' Dein Tipp: ' + str(
                tip))
        print("----------------------------------------------------------")
        added_won = (bet * 2) - bet
        added_balance = (bet * 2) - bet
        addwin(added_won)
        clrwin = 0
        return
    elif eowin == 1:
        await ctx.channel.send(
            'Du hast gewonnen! ' + '(' + str(result) + ' / ' + str(farbe_result) + ')' + ' Dein Tipp: ' + str(
                tip))
        print("----------------------------------------------------------")
        added_won = (bet * 2) - bet
        added_balance = (bet * 2) - bet
        addwin(added_won)
        eowin = 0
        return
    elif randomwin == 1:
        await ctx.channel.send(
            'Du hast gewonnen! ' + '(' + str(result) + ' / ' + str(farbe_result) + ')' + ' Dein Tipp: ' + str(
                tip))
        print("----------------------------------------------------------")
        added_won = (bet * 35) - bet
        added_balance = (bet * 35) - bet
        addwin(added_won)
        randomwin = 0
        return
    elif first12 == 1:
        await ctx.channel.send(
            'Du hast gewonnen! ' + '(' + str(result) + ' / ' + str(farbe_result) + ')' + ' Dein Tipp: ' + str(
                tip))
        print("----------------------------------------------------------")
        added_won = (bet * 4) - bet
        added_balance = (bet * 4) - bet
        addwin(added_won)
        first12 = 0
        return
    elif second12 == 1:
        await ctx.channel.send(
            'Du hast gewonnen! ' + '(' + str(result) + ' / ' + str(farbe_result) + ')' + ' Dein Tipp: ' + str(
                tip))
        print("----------------------------------------------------------")
        added_won = (bet * 4) - bet
        added_balance = (bet * 4) - bet
        addwin(added_won)
        second12 = 0
        return
    elif third12 == 1:
        await ctx.channel.send(
            'Du hast gewonnen! ' + '(' + str(result) + ' / ' + str(farbe_result) + ')' + ' Dein Tipp: ' + str(
                tip))
        print("----------------------------------------------------------")
        added_won = (bet * 4) - bet
        added_balance = (bet * 4) - bet
        addwin(added_won)
        third12 = 0
        return
    else:
        await ctx.channel.send(
            'Leider verloren ' + '(' + str(result) + ' / ' + str(farbe_result) + ')' + ' Dein Tipp: ' + str(
                tip))
        print("----------------------------------------------------------")
        added_lost = bet
        lost_balance = bet
        addlose(added_lost)
        return


async def showhelp(ctx):
    await ctx.channel.send('```'
                               + '\n' + '--------------------------------------------------------------------------'
                               + '\n' + "The Prefix is: '" + prefix + "'"
                               + '\n' + '--------------------------------------------------------------------------'
                               + '\n' + 'Allgemein:'
                               + '\n' + 'help | register | stats <userid> | leaderboard'
                               + '\n' + 'permissions <value> | permissions <userid> | clear <value>'
                               + '\n' + '--------------------------------------------------------------------------'
                               + '\n' + 'Roulette:'
                               + '\n' + 'start r | tip black | tip red | tip green | tip odd | tip even'
                               + '\n' + 'tip first12 | tip second12 | tip third12 | tip x | tip x <bet>'
                               + '\n' + 'tip random | weeklytip'
                               + '\n' + '--------------------------------------------------------------------------'
                               + '\n' + 'Settings:'
                               + '\n' + 'set minimumbet <value> | set maximumbet <value> | set weeklytip <value>'
                               + '\n' + 'set prefix <value>'
                               + '\n' + '--------------------------------------------------------------------------'
                               + '\n' + 'Mods:'
                               + '\n' + 'give <userid> <value> | mod <userid>'
                               + '\n' + '--------------------------------------------------------------------------'
                               + '```')

@bot.event
async def on_ready():
    print("Logged In")
    print("----------------------------------------------------------")

@bot.command()
async def help(ctx):
    await showhelp(ctx)


@bot.command()
async def set(ctx):
    global prefix
    global minimumbet
    global maximumbet

    requested_set = ctx.message.content.split(' ')[1]
    if requested_set == 'prefix':
        temp = str(ctx.message.content.split(' ')[2])
        if str(ctx.author.id) in mods:
            prefix = str(ctx.message.content.split(' ')[2])
            await ctx.channel.send("Der Prefix wurde erfolgreich zu '" + str(prefix) + "' geändert.")
            print(str(ctx.author) + " set the Prefix to '" + prefix + "'")
            print("----------------------------------------------------------")
        else:
            await ctx.channel.send('Fehlende Berechtigungen: Der befehl konnte nicht ausgeführt werden.')
            print(str(ctx.author) + ' tried to set the Prefix to ' + str(temp) + "'")
            print('Error: Missing permissions')
            print("----------------------------------------------------------")#

    elif requested_set == 'weeklytip':
        temp = str(ctx.message.content.split(' ')[2])
        if str(ctx.author.id) in mods:
            tip_of_the_week = str(ctx.message.content.split(' ')[2])
            await ctx.channel.send("Der Tip der Woche wurde erfolgreich zu '" + str(tip_of_the_week) + "' geändert.")
            print(str(ctx.author) + " set the weeklytip to '" + str(tip_of_the_week) + "'")
            print("----------------------------------------------------------")
        else:
            await ctx.channel.send('Fehlende Berechtigungen: Der befehl konnte nicht ausgeführt werden.')
            print(str(ctx.author) + " tried to set the weekly to '" + str(temp) + "'")
            print('Error: Missing permissions')
            print("----------------------------------------------------------")

    elif requested_set == 'maximumbet':
        temp = str(ctx.message.content.split(' ')[2])
        if str(ctx.author.id) in mods:
            maximumbet = str(ctx.message.content.split(' ')[2])
            maximumbet = float(str(maximumbet).replace('€', ''))
            maximumbet = float(str(maximumbet).replace('$', ''))
            await ctx.channel.send("Der Maximaleinsatz wurde erfolgreich zu " + str(maximumbet) + "€ geändert.")
            print(str(ctx.author) + " set maximum bet to " + str(maximumbet) + "€")
            print("----------------------------------------------------------")
        else:
            await ctx.channel.send('Fehlende Berechtigungen: Der befehl konnte nicht ausgeführt werden.')
            print(str(ctx.author) + " tried to set the maximum bet to " + str(temp) + '€')
            print('Error: Missing permissions')
            print("----------------------------------------------------------")

    elif requested_set == 'minimumbet':
        temp = str(ctx.message.content.split(' ')[2])
        if str(ctx.author.id) in mods:
            minimumbet = str(ctx.message.content.split(' ')[2])
            minimumbet = float(str(minimumbet).replace('€', ''))
            minimumbet = float(str(minimumbet).replace('$', ''))
            await ctx.channel.send("Der Minimaleinsatz wurde erfolgreich zu " + str(minimumbet) + "€ geändert.")
            print(str(ctx.author) + " set minimum bet to " + str(minimumbet) + "€")
            print("----------------------------------------------------------")
        else:
            await ctx.channel.send('Fehlende Berechtigungen: Der befehl konnte nicht ausgeführt werden.')
            print(str(ctx.author) + " tried to set the minimum bet to " + str(temp) + '€')
            print('Error: Missing permissions')
            print("----------------------------------------------------------")

@bot.command(name='clearevidence', aliases=['purge', 'clean', 'delete', 'c', 'clear'])
async def clear(ctx):
    if str(ctx.channel.type) == 'private':
        return
    else:
        try:
            msg_to_delete = int(ctx.message.content.split(' ')[1])
            if msg_to_delete == 1:
                await ctx.channel.send('Clearing ' + str(msg_to_delete) + ' message')
                await ctx.channel.purge(limit=3)
            elif msg_to_delete < 1:
                await ctx.channel.send('Fehler, bitte gebe eine positive Zahl ein')
            else:
                await ctx.channel.send('Clearing ' + str(msg_to_delete) + ' messages')
                await ctx.channel.purge(limit=msg_to_delete + 2)
        except:
            await ctx.channel.send('Nachrichten konnten nicht gelöscht werden')

@bot.command()
async def backup(ctx):
    requested_file = ctx.message.content.split(' ')[1]
    print(str(ctx.author) + " requested " + str(requested_file))
    if str(ctx.author.id) in mods:
        if requested_file == 'users.txt':
            if str(ctx.channel.type) == 'private':
                with open("users.txt", "rb") as file:
                    await ctx.channel.send("Your requested file is:", file=discord.File(file, "users.txt"))
        elif requested_file == 'stats.txt':
            if str(ctx.channel.type) == 'private':
                with open("stats.txt", "rb") as file:
                    await ctx.channel.send("Your requested file is:", file=discord.File(file, "stats.txt"))
        elif requested_file == 'mods.txt':
            if str(ctx.channel.type) == 'private':
                with open("stats.txt", "rb") as file:
                    await ctx.channel.send("Your requested file is:", file=discord.File(file, "mods.txt"))
    else:
        await ctx.channel.send('Fehlende Berechtigungen, bitte kontaktiere einen Moderator.')
        print(str(ctx.author) + ' tried to get ' + str(requested_file))
        print("----------------------------------------------------------")

@bot.command()
async def leaderboard(ctx):
    for x in users:
        users[x] = float(users[x])
    ranking = sorted(users, key=users.get, reverse=True)
    await ctx.channel.send('```'
                                       + '\n' + "Baker Street's Top Ten:"
                                       + '\n' + '1st Place:  @' + str(await bot.fetch_user(ranking[0])) + '  |   '
                                       + '[Account Balance: ' + str(users[ranking[0]]) + '€' + ']'
                                       + '\n' + '2nd Place:  @' + str(await bot.fetch_user(ranking[1])) + '  |   '
                                       + '[Account Balance: ' + str(users[ranking[1]]) + '€' + ']'
                                       + '\n' + '3rd Place:  @' + str(await bot.fetch_user(ranking[2])) + '  |   '
                                       + '[Account Balance: ' + str(users[ranking[2]]) + '€' + ']'
                                       + '\n' + '4th Place:  @' + str(await bot.fetch_user(ranking[3])) + '  |   '
                                       + '[Account Balance: ' + str(users[ranking[3]]) + '€' + ']'
                                       + '\n' + '5th Place:  @' + str(await bot.fetch_user(ranking[4])) + '  |   '
                                       + '[Account Balance: ' + str(users[ranking[4]]) + '€' + ']'
                                       + '\n' + '6th Place:  @' + str(await bot.fetch_user(ranking[5])) + '  |   '
                                       + '[Account Balance: ' + str(users[ranking[5]]) + '€' + ']'
                                       + '\n' + '7th Place:  @' + str(await bot.fetch_user(ranking[6])) + '  |   '
                                       + '[Account Balance: ' + str(users[ranking[6]]) + '€' + ']'
                                       + '\n' + '8th Place:  @' + str(await bot.fetch_user(ranking[7])) + '  |   '
                                       + '[Account Balance: ' + str(users[ranking[7]]) + '€' + ']'
                                       + '\n' + '9th Place:  @' + str(await bot.fetch_user(ranking[8])) + '  |   '
                                       + '[Account Balance: ' + str(users[ranking[8]]) + '€' + ']'
                                       + '\n' + '10th Place: @' + str(await bot.fetch_user(ranking[9])) + '  |   '
                                       + '[Account Balance: ' + str(users[ranking[9]]) + '€' + ']'
                                       + '\n' + '```')

@bot.command()
async def permissions(ctx):
    try:
        requested_user_rank = ctx.message.content.split(' ')[1]
    except IndexError:
        requested_user_rank = str(ctx.author.id)

    if requested_user_rank in users:
        if str(requested_user_rank) in mods:
            await ctx.channel.send('```'
                                               + '\n' + 'Showing Permissions for: ' + str(
                await bot.fetch_user(requested_user_rank))
                                               + '\n \n' + 'Ranks: Moderator, Player'
                                               + '\n' + '```')
        else:
            await ctx.channel.send('```'
                                               + '\n' + 'Showing Permissions for: ' + str(
                await bot.fetch_user(requested_user_rank))
                                               + '\n \n' + 'Rank: Player'
                                               + '\n' + '```')
    else:
        await ctx.channel.send("User konnte nicht in der Datenbank gefunden werden")

@bot.command()
async def stats(ctx):
    global won
    global lost
    global balance
    global username

    try:
        username = str(ctx.message.content.split(' ')[1])
    except IndexError:
        username = str(ctx.author.id)
    get_playerstats()

    if username in statsdic:
        get_balance()

        await ctx.channel.send('```'
                                    + '\n' + 'Showing Statistics for: ' + str(
            await bot.fetch_user(int(username)))
                                    + '\n \n' + 'Won: ' + str(won) + '€' + ' Lost: ' + str(
            lost) + '€' + ' Balance: ' + str(balance) + '€'
                                    + '\n' + '```')
    else:
        await ctx.channel.send("User konnte nicht in der Datenbank gefunden werden")

@bot.command()
async def mod(ctx):
    global new_mod
    global removed_mod

    new_mod = ctx.message.content.split(' ')[1]
    removed_mod = new_mod
    if str(ctx.author.id) in mods:
        if new_mod not in mods:
            add_mod()
            await ctx.channel.send('`Added new mod: ' + str(await bot.fetch_user(new_mod)) + '`')
            print(ctx.author + ' added ' + new_mod + ' to mods')
            print("----------------------------------------------------------")
        else:
            remove_mod()
            await ctx.channel.send('`Removed mod: ' + str(await bot.fetch_user(removed_mod)) + '`')
            print(ctx.author + ' removed ' + removed_mod + ' from mods')
            print("----------------------------------------------------------")
    else:
        await ctx.channel.send('Fehlende Berechtigungen: Der befehl konnte nicht ausgeführt werden.')
        print(ctx.author + ' tried to add ' + new_mod + ' to mods')
        print('Error: Missing permissions')
        print("----------------------------------------------------------")

@bot.command()
async def give(ctx):
    global newbalance
    global user_id
    global user_balance

    user_balance = ctx.message.content.split(' ')[1:]
    userid = user_balance[0]
    try:
        newbalance = str(user_balance[1])
        newbalance = float(str(newbalance).replace('€', ''))
    except IndexError:
        await ctx.channel.send('Geld konnte nicht hinzugefügt werden')
    old_balance = users[userid]
    if str(ctx.author.id) in mods:
        if str(userid) in users:
            with open("users.txt", "w") as users_file:
                users[str(userid)] = newbalance
                for k in users.keys():
                    users_file.write("{}:{}\n".format(k, users[k]))
                users_file.close()
            print('Old Balance: ' + str(old_balance) + '€')
            print('New Balance: ' + str(users[str(userid)]) + '€')
            print("----------------------------------------------------------")
            await ctx.channel.send("Changed Account Balance of " + str(await bot.fetch_user(userid))
                                               + " to " + str(newbalance) + '€')
        else:
            print('Error: Userid not found')
    else:
        await ctx.channel.send(
                    'Fehlende Berechtigungen: Die Account balance konnte nicht verändert werden.')
        print(str(ctx.author) + ' tried to change the account balance of '
                      + str(await bot.fetch_user(userid)) + ' from ' + users[userid] + ' to: ' + str(newbalance) + '€')
        print("----------------------------------------------------------")

@bot.command()
async def weeklytip(ctx):
    await ctx.channel.send('`' + 'The weekly tip is: ' + tip_of_the_week + '`')

@bot.command()
async def register(ctx):
    global user

    user = str(ctx.author.id)
    username = str(ctx.author)
    add_user()
    if messagecode == 1:
        print("User registered: " + username)
        print("----------------------------------------------------------")
        await ctx.channel.send('`' + username + '`' + ', du hast dich erfolgreich registriert')
    else:
        print(username)
        print("Error: User already exists")
        print("----------------------------------------------------------")
        await ctx.channel.send('`' + username + '`' + ', du bist schon registriert')

@bot.command()
async def start(ctx):
    game_to_start = ctx.message.content.split(' ')[1]
    if game_to_start == 'r':
        global accepting_bets
        time.sleep(0.5)
        await ctx.channel.send("Das Spiel beginnt, um dich zu registrieren schreibe " + '`' + prefix + 'register' + '`, Platziere deine Wette')
        accepting_bets = True
        await asyncio.sleep(57)
        accepting_bets = False
        await asyncio.sleep(3)

        await ctx.channel.purge(limit=100)

    print(bets)
    i = 0
    while i < len(bets):
        player_tip = bets[i]
        player_tip.split(':')
        print(player_tip)
        player = int(player_tip[0])
        tip = int(player_tip[1])
        bet = int(player_tip[2])
        i += 1
        print(str(player) + str(tip) + str(bet))



    await showhelp(ctx)
    f = open('bets.txt', 'r+')
    f.truncate(0)
    f.close()

@bot.command()
async def tip(ctx):
    global nmbwin
    global clrwin
    global eowin
    global result
    global zahl
    global farbe
    global tip
    global error
    global first12
    global second12
    global third12
    global player
    global player_id
    global bet

    if accepting_bets == True:
        pass
    else:
        await ctx.channel.send('Deine Wette konnte nicht hinterlegt werden, starte das Spiel, indem du ' + '`' + prefix
                                           + 'start r' + '`' + ' eingibst')
        return
    try:
        tip_bet = ctx.message.content.split(' ')[1:]
        tip_bet = ' '.join(tip_bet)
        tip,bet = tip_bet.split(' ')
    except IndexError:
        await ctx.channel.send('Dein Einsatz konnte nicht hinterlegt werden, bitte versuche es nochmal.')
        print(str(ctx.author))
        print('Error: Invalid Input')
        print("----------------------------------------------------------")
        return
    except ValueError:
        tip = ctx.message.content.split(' ')[1]
        bet = 0.0

    player = ctx.author
    player_id = str(ctx.author.id)
    print(str(player))
    print('Tip: ' + str(tip))

    try:
        bet = float(str(bet).replace('€', ''))
        bet = float(str(bet).replace('$', ''))
    except:
        await ctx.channel.send('Dein Einsatz konnte nicht hinterlegt werden, bitte versuche es nocheinmal.')
        return

    if bet == 0.0:
        pass
    elif bet > float(users[player_id]):
        await ctx.channel.send('Dein Einsatz konnte nicht hinterlegt werden, dein Guthaben reicht nicht aus.')
        print('Error: Account balance not sufficient ' + '(' + str(users[player_id]) + '<' + str(bet) + ')')
        print("----------------------------------------------------------")
        return
    elif bet < float(minimumbet) and bet != 0:
        await ctx.channel.send("Dein Einsatz konnte nicht hinterlegt werden, der Mindesteinsatz beträgt " + str(minimumbet) + "€.")
        print('Error: Requested bet smaller than minimumbet ' + '(' + str(minimumbet) + ')')
        print("----------------------------------------------------------")
        return
    elif bet > float(maximumbet) and bet != 0:
        await ctx.channel.send(
                    "Dein Einsatz konnte nicht hinterlegt werden, der Maximaleinsatz beträgt " + str(maximumbet) + "€.")
        print('Error: Requested bet bigger than maximumbet ' + '(' + str(maximumbet) + ')')
        print("----------------------------------------------------------")
        return
    else:
        pass

    print('Bet: ' + str(bet) + '€')
    if str(tip) == 'x':
        await ctx.channel.send(
                    "Dein Einsatz konnte nicht hinterlegt werden, gebe eine Zahl zwischen 00 und 36 ein.")

    requested_append = str(player_id) + ':' + str(tip) + ':' + str(bet)
    bets.append(requested_append)
    with open("bets.txt", "a") as bets_file:
        bets_file.write(requested_append + '\n')
    bets_file.close()

    result = random.randint(-1, 36)
    if result == -1:
        result = '00'
    print('Correct Number: ' + str(result))

    try:
        if int(tip) > 36:
            print("Error: invalid tip")
            print("----------------------------------------------------------")
            await ctx.channel.send(
                        'Dein Einsatz konnte nicht hinterlegt werden, bitte versuche es nochmal.')
            return
        else:
            clrwin = -1
            zahl = int(tip)
            print("No Color input")
            await zahlentest(ctx)
    except ValueError:
        nmbwin = -1
        if tip == 'random' or tip == 'zufall':
            await random_tip(ctx)
            return
        print("No Number input")
        if tip == 'black' or tip == 'schwarz' or tip == 'red' or tip == 'rot' or tip == 'green' or tip == 'grün':
            await farbeninput()
            await farbentest(ctx)
            return
        if tip == 'odd' or tip == 'even':
            await gerade_ungerade(ctx)
            return
        if tip == 'first12':
            await firsttwelve(ctx)
            return
        if tip == 'second12':
            await secondtwelve(ctx)
            return
        if tip == 'third12':
            await thirdtwelve(ctx)
            return
        await ctx.channel.send('Dein Einsatz konnte nicht hinterlegt werden, bitte versuche es nochmal.')
        print("----------------------------------------------------------")
        # error = 1 == no color detected
        if error == 1:
            await ctx.channel.send(
                        'Dein Einsatz konnte nicht hinterlegt werden, bitte versuche es nochmal.')
            print('Error: invalid color')
            print("----------------------------------------------------------")
            return



bot.run("NDY4NzM5NzY3ODQwODAwNzY5.W03R7Q.jfybjYfxEhCcBtfeY3ukx793AFs")