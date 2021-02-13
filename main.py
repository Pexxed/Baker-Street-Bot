import discord
import random
import time

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
stats = {}
mods = []
userlist = []
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

tip_of_the_week = '17'
minimumbet = 0.1
maximumbet = 500.0
prefix = '/'

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
                stats[user] = won_lost
                won_lost.split('|')
                won = int(won_lost[0])
                lost = int(won_lost[2])
                statslist.append(user + ':' + stats[user])
        stats_file.close()

except FileNotFoundError:
    users = {}
    mods = {}
    stats = {}


def add_user():
    global messagecode

    f = open("users.txt", "a")
    if user in users:
        messagecode = 2
    else:
        f.writelines(str(user) + ":0" + "\n")
        f.flush()
        messagecode = 1
        f.close()
    b = open("stats.txt", "a")

    if user in stats:
        messagecode = 2
    else:
        b.writelines(str(user) + "0|0" + "\n")
        b.flush()
        messagecode = 1
        b.close()


def add_mod():
    f = open("mods.txt", "a")
    f.write(new_mod + '\n')
    f.flush()
    f.close()
    mods.append(new_mod)

def remove_mod():
    mods.remove(remove_mod())
    with open("mods.txt", "w") as mods_file:
            mods_file.write("\n".join(mods))
    mods_file.close()

def addlose(added_lost):
    global won
    global lost
    global player
    global player_id
    global bet

    playerstats = stats[str(player_id)].split('|')
    newbalance = float(users[str(player_id)]) - added_lost

    lost = 0.0
    lost += float(added_lost)
    playerstats[0] = won
    playerstats[1] = lost

    playerstats = str(won) + '|' + str(lost)

    with open("users.txt", "w") as users_file:
        users[str(player_id)] = newbalance
        for k in users.keys():
            users_file.write("{}:{}\n".format(k, users[k]))
        users_file.close()

    stats[player_id] = playerstats
    with open("stats.txt", "w") as stats_file:
        for k in users.keys():
            stats_file.write("{}:{}\n".format(k, stats[k]))
    stats_file.close()

def addwin(added_won):
    global won
    global looses
    global player
    global player_id
    global bet

    playerstats = stats[str(player_id)].split('|')
    newbalance = float(users[str(player_id)]) + added_won
    won = playerstats[0]
    won += float(added_won)
    playerstats[0] = won
    playerstats[1] = lost
    playerstats = str(won) + '|' + str(lost)

    with open("users.txt", "w") as users_file:
        users[str(player_id)] = newbalance
        for k in users.keys():
            users_file.write("{}:{}\n".format(k, users[k]))
        users_file.close()

    stats[player_id] = playerstats
    with open("stats.txt", "w") as stats_file:
        for k in users.keys():
            stats_file.write("{}:{}\n".format(k, stats[k]))
    stats_file.close()


class MyClient(discord.Client):
    global prefix
    # Einloggen
    async def on_ready(self):
        print("Logged In")
        print("----------------------------------------------------------")

    # Wenn Nachricht gepostet(im Server oder Privat)
    async def on_message(self, message):
        if message.author == client.user:
            return

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

        async def zahlentest():
            global nmbwin
            global result
            global zahl

            if str(result) == str(zahl):
                nmbwin = 1
                print('Won Zahlentest')
                await resulttest()
                return
            else:
                nmbwin = -1
                print('Lost Zahlentest')
                await resulttest()
                return

        async def farbentest():
            global clrwin
            global farbe
            global result

            if farbe == -1 and str(result) in roulette_black:
                clrwin = 1
                print('Won Farbentest')
                await resulttest()
                return
            elif farbe == -1 and str(result) not in roulette_black:
                clrwin = -1
                print('Lost Farbentest')
                await resulttest()
                return
            if farbe == -2 and str(result) in roulette_red:
                clrwin = 1
                print('Won Farbentest')
                await resulttest()
                return
            elif farbe == -2 and str(result) not in roulette_red:
                clrwin = -1
                print('Lost Farbentest')
                await resulttest()
                return
            elif farbe == -3 and str(result) in roulette_green:
                clrwin = 1
                print('Won Farbentest')
                await resulttest()
                return
            elif farbe == -3 and str(result) not in roulette_green:
                clrwin = -1
                print('Lost Farbentest')
                await resulttest()
                return
            else:
                clrwin = -1
                print('No Color')
                await resulttest()
                return

        async def gerade_ungerade():
            global result
            global zahl
            global eowin
            global error

            try:
                if tip == 'odd':
                    if str(result) not in roulette_even:
                        eowin = 1
                        error = 0
                        print('Won Odd or Even')
                        await resulttest()
                        return
                    if str(result) in roulette_even:
                        eowin = -1
                        error = 0
                        print('Lost Odd or Even')
                        await resulttest()
                        return
                if tip == 'even':
                    if str(result) in roulette_even:
                        eowin = 1
                        error = 0
                        print('Won Odd or Even')
                        await resulttest()
                        return
                    if str(result) not in roulette_even:
                        eowin = -1
                        error = 0
                        print('Lost Odd or Even')
                        await resulttest()
                        return
            except:
                error = 1

        async def firsttwelve():
            global first12
            global result

            if str(result) in roulette_firsttwelve:
                first12 = 1
                print('Won First12')
            else:
                first12 = 0
                print('Lost First12')
            await resulttest()
            return

        async def secondtwelve():
            global second12
            global result

            if str(result) in roulette_secondtwelve:
                second12 = 1
                print('Won Second12')
            else:
                second12 = 0
                print('Lost Second12')
            await resulttest()
            return

        async def thirdtwelve():
            global third12
            global result

            if str(result) in roulette_thirdwelve:
                third12 = 1
                print('Won Third12')
            else:
                third12 = 0
                print('Lost Third12')
            await resulttest()
            return

        async def random_tip():
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
                    await resulttest()
                    return
                else:
                    randomwin = -1
                    error = 0
                    print('Lost random tip')
                    await resulttest()
                    return

        async def resulttest():
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
            global looses

            if str(result) in roulette_black:
                farbe_result = 'black'
            elif str(result) in roulette_green:
                farbe_result = 'green'
            else:
                farbe_result = 'red'

            if nmbwin == 1:
                await message.channel.send(
                    'Du hast gewonnen! ' + '(' + str(result) + ' / ' + str(farbe_result) + ')' + ' Dein Tipp: ' + str(
                        tip))
                print("----------------------------------------------------------")
                added_won = bet * 35
                addwin(added_won)
                nmbwin = 0
                return
            elif clrwin == 1:
                await message.channel.send(
                    'Du hast gewonnen! ' + '(' + str(result) + ' / ' + str(farbe_result) + ')' + ' Dein Tipp: ' + str(
                        tip))
                print("----------------------------------------------------------")
                added_won = bet * 2
                addwin(added_won)
                clrwin = 0
                return
            elif eowin == 1:
                await message.channel.send(
                    'Du hast gewonnen! ' + '(' + str(result) + ' / ' + str(farbe_result) + ')' + ' Dein Tipp: ' + str(
                        tip))
                print("----------------------------------------------------------")
                added_won = bet * 2
                addwin(added_won)
                eowin = 0
                return
            elif randomwin == 1:
                await message.channel.send(
                    'Du hast gewonnen! ' + '(' + str(result) + ' / ' + str(farbe_result) + ')' + ' Dein Tipp: ' + str(
                        tip))
                print("----------------------------------------------------------")
                added_won = bet * 35
                addwin(added_won)
                randomwin = 0
                return
            elif first12 == 1:
                await message.channel.send(
                    'Du hast gewonnen! ' + '(' + str(result) + ' / ' + str(farbe_result) + ')' + ' Dein Tipp: ' + str(
                        tip))
                print("----------------------------------------------------------")
                added_won = bet * 4
                addwin(added_won)
                first12 = 0
                return
            elif second12 == 1:
                await message.channel.send(
                    'Du hast gewonnen! ' + '(' + str(result) + ' / ' + str(farbe_result) + ')' + ' Dein Tipp: ' + str(
                        tip))
                print("----------------------------------------------------------")
                added_won = bet * 4
                addwin(added_won)
                second12 = 0
                return
            elif third12 == 1:
                await message.channel.send(
                    'Du hast gewonnen! ' + '(' + str(result) + ' / ' + str(farbe_result) + ')' + ' Dein Tipp: ' + str(
                        tip))
                print("----------------------------------------------------------")
                added_won = bet * 4
                addwin(added_won)
                third12 = 0
                return
            else:
                await message.channel.send(
                    'Leider verloren ' + '(' + str(result) + ' / ' + str(farbe_result) + ')' + ' Dein Tipp: ' + str(
                        tip))
                print("----------------------------------------------------------")
                added_looses = bet
                addlose(added_looses)
                return

        global prefix
        global tip_of_the_week
        global minimumbet
        global maximumbet

        if message.content == prefix + 'help':
            await message.channel.send('```'
                                       + '\n' + '--------------------------------------------------------------------------'
                                       + '\n' + "The Prefix is: '" + prefix + "'"
                                       + '\n' + '--------------------------------------------------------------------------'
                                       + '\n' + 'Allgemein:'
                                       + '\n' + 'help | register | stats <userid> | leaderboard'
                                       + '\n' + 'permissions permissions <userid>'
                                       + '\n' + '--------------------------------------------------------------------------'
                                       + '\n' + 'Roulette:'
                                       + '\n' + 'start r | tip black | tip red | tip green | tip odd | tip even'
                                       + '\n' + 'tip first12 | tip second12 | tip third12 | tip x | tip x <bet>'
                                       + '\n' + 'tip random | weeklytip'
                                       + '\n' + '--------------------------------------------------------------------------'
                                       + '\n' + 'Mods:'
                                       + '\n' + 'give <userid> | mod <userid> | backup <file.txt>'
                                       + '\n' + '--------------------------------------------------------------------------'
                                       + '\n' + 'Settings:'
                                       + '\n' + 'set minimumbet | set maximumbet | set weeklytip | set prefix'
                                       + '\n' + '--------------------------------------------------------------------------'
                                       + '```')

        if message.content.startswith(prefix + 'set minimumbet'):
            global minimumbet

            temp = str(message.content.split(' ')[2])
            if str(message.author.id) in mods:
                minimumbet = str(message.content.split(' ')[2])
                minimumbet = float(str(minimumbet).replace('€', ''))
                minimumbet = float(str(minimumbet).replace('$', ''))
                await message.channel.send("Der Minimaleinsatz wurde erfolgreich zu " + str(minimumbet) + "€ geändert.")
                print(str(message.author) + " set minimum bet to " + str(minimumbet) + "€")
                print("----------------------------------------------------------")
            else:
                await message.channel.send('Fehlende Berechtigungen: Der befehl konnte nicht ausgeführt werden.')
                print(str(message.author) + " tried to set the minimum bet to " + str(temp) + '€')
                print('Error: Missing permissions')
                print("----------------------------------------------------------")

        if message.content.startswith(prefix + 'set maximumbet'):
            global maximumbet

            temp = str(message.content.split(' ')[2])
            if str(message.author.id) in mods:
                maximumbet = str(message.content.split(' ')[2])
                maximumbet = float(str(maximumbet).replace('€', ''))
                maximumbet = float(str(maximumbet).replace('$', ''))
                await message.channel.send("Der Maximaleinsatz wurde erfolgreich zu " + str(maximumbet) + "€ geändert.")
                print(str(message.author) + " set maximum bet to " + str(maximumbet) + "€")
                print("----------------------------------------------------------")
            else:
                await message.channel.send('Fehlende Berechtigungen: Der befehl konnte nicht ausgeführt werden.')
                print(str(message.author) + " tried to set the maximum bet to " + str(temp) + '€')
                print('Error: Missing permissions')
                print("----------------------------------------------------------")

        if message.content.startswith(prefix + 'set weeklytip'):
            global tip_of_the_week

            temp = str(message.content.split(' ')[2])
            if str(message.author.id) in mods:
                tip_of_the_week = str(message.content.split(' ')[2])
                await message.channel.send("Der Tip der Woche wurde erfolgreich zu '" + str(tip_of_the_week) + "' geändert.")
                print(str(message.author) + " set the weeklytip to '" + str(tip_of_the_week) + "'")
                print("----------------------------------------------------------")
            else:
                await message.channel.send('Fehlende Berechtigungen: Der befehl konnte nicht ausgeführt werden.')
                print(str(message.author) + " tried to set the weekly to '" + str(temp) + "'")
                print('Error: Missing permissions')
                print("----------------------------------------------------------")

        if message.content.startswith(prefix + 'set prefix'):
            temp = str(message.content.split(' ')[2])
            if str(message.author.id) in mods:
                prefix = str(message.content.split(' ')[2])
                await message.channel.send("Der Prefix wurde erfolgreich zu '" + str(prefix) + "' geändert.")
                print(str(message.author) + " set the Prefix to '" + prefix + "'")
                print("----------------------------------------------------------")
            else:
                await message.channel.send('Fehlende Berechtigungen: Der befehl konnte nicht ausgeführt werden.')
                print(str(message.author) + ' tried to set the Prefix to ' + str(temp) + "'")
                print('Error: Missing permissions')
                print("----------------------------------------------------------")

        if message.content == prefix + 'backup users.txt':
            if str(message.author.id) in mods:
                if str(message.channel.type) == 'private':
                    with open("users.txt", "rb") as file:
                        await message.channel.send("Your requested file is:", file=discord.File(file, "users.txt"))

        if message.content == prefix + 'backup stats.txt':
            if str(message.author.id) in mods:
                if str(message.channel.type) == 'private':
                    with open("stats.txt", "rb") as file:
                        await message.channel.send("Your requested file is:", file=discord.File(file, "stats.txt"))

        if message.content == prefix + 'backup mods.txt':
            if str(message.author.id) in mods:
                if str(message.channel.type) == 'private':
                    with open("stats.txt", "rb") as file:
                        await message.channel.send("Your requested file is:", file=discord.File(file, "mods.txt"))

        if message.content == prefix + 'leaderboard':
            for x in users:
                users[x] = float(users[x])
            ranking = sorted(users, key=users.get, reverse=True)
            await message.channel.send('```'
                                       + '\n' + "Baker Street's Top Ten:"
                                       + '\n' + '1st Place:  @' + str(await client.fetch_user(ranking[0])) + '  |   '
                                       + '[Account Balance: ' + str(users[ranking[0]]) + '€' + ']'
                                       + '\n' + '2nd Place:  @' + str(await client.fetch_user(ranking[1])) + '  |   '
                                       + '[Account Balance: ' + str(users[ranking[1]]) + '€' + ']'
                                       + '\n' + '3rd Place:  @' + str(await client.fetch_user(ranking[2])) + '  |   '
                                       + '[Account Balance: ' + str(users[ranking[2]]) + '€' + ']'
                                       + '\n' + '4th Place:  @' + str(await client.fetch_user(ranking[3])) + '  |   '
                                       + '[Account Balance: ' + str(users[ranking[3]]) + '€' + ']'
                                       + '\n' + '5th Place:  @' + str(await client.fetch_user(ranking[4])) + '  |   '
                                       + '[Account Balance: ' + str(users[ranking[4]]) + '€' + ']'
                                       + '\n' + '6th Place:  @' + str(await client.fetch_user(ranking[5])) + '  |   '
                                       + '[Account Balance: ' + str(users[ranking[5]]) + '€' + ']'
                                       + '\n' + '7th Place:  @' + str(await client.fetch_user(ranking[6])) + '  |   '
                                       + '[Account Balance: ' + str(users[ranking[6]]) + '€' + ']'
                                       + '\n' + '8th Place:  @' + str(await client.fetch_user(ranking[7])) + '  |   '
                                       + '[Account Balance: ' + str(users[ranking[7]]) + '€' + ']'
                                       + '\n' + '9th Place:  @' + str(await client.fetch_user(ranking[8])) + '  |   '
                                       + '[Account Balance: ' + str(users[ranking[8]]) + '€' + ']'
                                       + '\n' + '10th Place: @' + str(await client.fetch_user(ranking[9])) + '  |   '
                                       + '[Account Balance: ' + str(users[ranking[9]]) + '€' + ']'
                                       + '\n' + '```')

        if message.content.startswith(prefix + 'permissions'):
            try:
                requested_user_rank = message.content.split(' ')[1]
            except IndexError:
                requested_user_rank = str(message.author.id)

            if requested_user_rank in users:
                if str(requested_user_rank) in mods:
                    await message.channel.send('```'
                                               + '\n' + 'Showing Permissions for: ' + str(
                        await client.fetch_user(requested_user_rank))
                                               + '\n \n' + 'Ranks: Moderator, Player'
                                               + '\n' + '```')
                else:
                    await message.channel.send('```'
                                               + '\n' + 'Showing Permissions for: ' + str(
                        await client.fetch_user(requested_user_rank))
                                               + '\n \n' + 'Rank: Player'
                                               + '\n' + '```')
            else:
                await message.channel.send("User konnte nicht in der Datenbank gefunden werden")

        if message.content.startswith(prefix + 'stats'):
            global won
            global lost
            global balance

            try:
                username = str(message.content.split(' ')[1])
            except IndexError:
                username = str(message.author.id)

            playerstats = stats[str(username)].split('|')

            won = playerstats[0]
            lost = playerstats[1]

            if username in stats:
                balance = users[username]
                await message.channel.send('```'
                                           + '\n' + 'Showing Statistics for: ' + str(
                    await client.fetch_user(int(username)))
                                           + '\n \n' + 'Won: ' + str(won) + '€' + ' Lost: ' + str(
                    lost) + '€' + ' Balance: ' + str(balance) + '€'
                                           + '\n' + '```')
            else:
                await message.channel.send("User konnte nicht in der Datenbank gefunden werden")

        if message.content.startswith(prefix + 'mod'):
            global new_mod
            global removed_mod

            new_mod = message.content.split(' ')[1]
            removed_mod = new_mod
            if str(message.author.id) in mods:
                if new_mod not in mods:
                    add_mod()
                    await message.channel.send('`Added new mod: ' + str(await client.fetch_user(new_mod)) + '`')
                    print(message.author + ' added ' + new_mod + ' to mods')
                    print("----------------------------------------------------------")
                else:
                    remove_mod()
                    await message.channel.send('`Removed mod: ' + str(await client.fetch_user(removed_mod)) + '`')
                    print(message.author + ' removed ' + removed_mod + ' from mods')
                    print("----------------------------------------------------------")
            else:
                await message.channel.send('Fehlende Berechtigungen: Der befehl konnte nicht ausgeführt werden.')
                print(message.author + ' tried to add ' + new_mod + ' to mods')
                print('Error: Missing permissions')
                print("----------------------------------------------------------")

        if message.content.startswith(prefix + 'give'):
            global newbalance
            global user_id
            global user_balance

            user_balance = message.content.split(' ')[1:]
            userid = user_balance[0]
            try:
                newbalance = str(user_balance[1])
                newbalance = float(str(newbalance).replace('€', ''))
                newbalance = float(str(newbalance).replace('$', ''))
            except IndexError:
                await message.channel.send('Geld konnte nicht hinzugefügt werden')
            old_balance = users[userid]
            if str(message.author.id) in mods:
                if str(userid) in users:
                    with open("users.txt", "w") as users_file:
                        users[str(userid)] = newbalance
                        for k in users.keys():
                            users_file.write("{}:{}\n".format(k, users[k]))
                        users_file.close()
                    print('Old Balance: ' + str(old_balance) + '€')
                    print('New Balance: ' + str(users[str(userid)]) + '€')
                    print("----------------------------------------------------------")
                    await message.channel.send("Changed Account Balance of " + str(await client.fetch_user(userid))
                                               + " to " + str(newbalance) + '€')
                else:
                    print('Error: Userid not found')
            else:
                await message.channel.send(
                    'Fehlende Berechtigungen: Die Account balance konnte nicht verändert werden.')
                print(str(message.author) + ' tried to change the account balance of '
                      + str(await client.fetch_user(userid)) + ' from ' + users[userid] + ' to: ' + str(newbalance) + '€')
                print("----------------------------------------------------------")

        if message.content == prefix + 'weeklytip':
            await message.channel.send('`' + 'The weekly tip is: ' + tip_of_the_week + '`')

        if message.content == prefix + 'register':
            global user

            user = str(message.author.id)
            username = str(message.author)
            add_user()
            if messagecode == 1:
                print("User registered: " + username)
                print("----------------------------------------------------------")
                await message.channel.send('`' + username + ', du hast dich erfolgreich registriert`')
            else:
                print(username)
                print("Error: User already exists")
                print("----------------------------------------------------------")
                await message.channel.send('`' + username + ', du bist schon registriert`')

        if message.content == prefix + 'start r':
            time.sleep(0.5)
            await message.channel.send(
                "`Das Spiel beginnt in 45 Sekunden, um dich zu registrieren schreibe '/register'`")

        if message.content.startswith(prefix + "tip"):
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

            try:
                tip_bet = message.content.split(' ')[1:]
                tip_bet = ' '.join(tip_bet)
                tip,bet = tip_bet.split(' ')
            except IndexError:
                await message.channel.send('Dein Einsatz konnte nicht hinterlegt werden, bitte versuche es nochmal.')
                print(str(message.author))
                print('Error: Invalid Input')
                print("----------------------------------------------------------")
                return
            except ValueError:
                tip = message.content.split(' ')[1]
                bet = 0.0

            player = message.author
            player_id = str(message.author.id)
            print(str(player))
            print('Tip: ' + str(tip))

            bet = float(str(bet).replace('€', ''))
            bet = float(str(bet).replace('$', ''))

            if bet == 0.0:
                pass
            elif bet > float(users[player_id]):
                await message.channel.send('Dein Einsatz konnte nicht hinterlegt werden, dein Guthaben reicht nicht aus.')
                print('Error: Account balance not sufficient ' + '(' + str(users[player_id]) + '<' + str(bet) + ')')
                print("----------------------------------------------------------")
                return
            elif bet < float(minimumbet) and bet != 0:
                await message.channel.send("Dein Einsatz konnte nicht hinterlegt werden, der Mindesteinsatz beträgt " + str(minimumbet) + "€.")
                print('Error: Requested bet smaller than minimumbet ' + '(' + str(minimumbet) + ')')
                print("----------------------------------------------------------")
                return
            elif bet > float(maximumbet) and bet != 0:
                await message.channel.send(
                    "Dein Einsatz konnte nicht hinterlegt werden, der Maximaleinsatz beträgt " + str(maximumbet) + "€.")
                print('Error: Requested bet bigger than maximumbet ' + '(' + str(maximumbet) + ')')
                print("----------------------------------------------------------")
                return
            else:
                pass

            print('Bet: ' + str(bet) + '€')
            if str(tip) == 'x':
                await message.channel.send(
                    "Dein Einsatz konnte nicht hinterlegt werden, gebe eine Zahl zwischen 00 und 36 ein.")

            result = random.randint(-1, 36)
            if result == -1:
                result = '00'
            print('Correct Number: ' + str(result))

            try:
                if int(tip) > 36:
                    print("Error: invalid tip")
                    print("----------------------------------------------------------")
                    await message.channel.send(
                        'Dein Einsatz konnte nicht hinterlegt werden, bitte versuche es nochmal.')
                    return
                else:
                    clrwin = -1
                    zahl = int(tip)
                    print("No Color input")
                    await zahlentest()
            except ValueError:
                nmbwin = -1
                if tip == 'random' or tip == 'zufall':
                    await random_tip()
                    return
                print("No Number input")
                if tip == 'black' or tip == 'schwarz' or tip == 'red' or tip == 'rot' or tip == 'green' or tip == 'grün':
                    await farbeninput()
                    await farbentest()
                    return
                if tip == 'odd' or tip == 'even':
                    await gerade_ungerade()
                    return
                if tip == 'first12':
                    await firsttwelve()
                    return
                if tip == 'second12':
                    await secondtwelve()
                    return
                if tip == 'third12':
                    await thirdtwelve()
                    return
                # error = 1 == no color detected
                if error == 1:
                    await message.channel.send(
                        'Dein Einsatz konnte nicht hinterlegt werden, bitte versuche es nochmal.')
                    print('Error: invalid color')
                    print("----------------------------------------------------------")
                    return


client = MyClient()
client.run("NDY4NzM5NzY3ODQwODAwNzY5.W03R7Q.jfybjYfxEhCcBtfeY3ukx793AFs")