import discord
import random
import time
import os

leaderboard = {}
roulette_black = ['2', '4', '6', '8', '10', '11', '13', '15', '17', '20', '22', '24', '26', '28', '29', '31', '33', '35']
roulette_red = ['1', '3', '5', '7', '9', '12', '14', '16', '18', '19', '21', '23', '25', '27', '30', '32', '34', '36']
roulette_green = ['0', '00']
roulette_even = ['2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30', '32', '34', '36']
roulette_onetoeiteen = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18']
roulette_firsttwelve = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
roulette_secondtwelve = ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']
roulette_thirtwelve = ['25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36']
users = {}
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
except FileNotFoundError:
    users = {}
    mods = {}

def add_user():
    f = open("users.txt", "a")
    global messagecode
    if user in users:
        messagecode = 2
    else:
        f.writelines(str(user) + ":0" + "\n")
        f.flush()
        messagecode = 1
        f.close()

def add_mod():
    mods.append(new_mod)
    f = open("mods.txt", "a")
    f.write(new_mod + '\n')
    f.flush()
    f.close()

class MyClient(discord.Client):
    # Einloggen
    async def on_ready(self):
        print("Logged In")
        print("----------------------------------------------------------")

    # Wenn Nachricht gepostet(im Server oder Privat)
    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content == '/help':
            await message.channel.send('```'
                                       + '\n' + '--------------------------------------------------------------------------'
                                       + '\n' + 'Allgemein:'
                                       + '\n' + '/help | /register | /stats | /leaderboard | /permissions | /permissions <userid>'
                                       + '\n' + '--------------------------------------------------------------------------'
                                       + '\n' + 'Roulette:'
                                       + '\n' + '/start r | /tip black | /tip red | /tip green | /tip odd | /tip even | /tip x'
                                       + '\n' + '/tip random'
                                       + '\n' + '--------------------------------------------------------------------------'
                                       + '\n' + 'Mods:'
                                       + '\n' + '/give <userid> | /mod <username>' + '```')

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

            if str(result) in roulette_black:
                farbe_result = 'black'
            elif str(result) in roulette_green:
                farbe_result = 'green'
            else:
                farbe_result = 'red'

            if tip == 'odd':
                tip = 'ungerade'
            if tip == 'even':
                tip = 'gerade'

            if nmbwin == 1 or clrwin == 1 or eowin == 1 or randomwin == 1 or first12 == 1 or second12 == 1 or third12 == 1:
                await message.channel.send('Du hast gewonnen! ' + '(' + str(result) + ' / ' + str(farbe_result) + ')' + ' Dein Tipp: ' + str(tip))
                print("----------------------------------------------------------")
                return
            else:
                await message.channel.send('Leider verloren ' + '(' + str(result) + ' / ' + str(farbe_result) + ')' + ' Dein Tipp: ' + str(tip))
                print("----------------------------------------------------------")
                return

        if message.content == '/leaderboard':
            ranking = sorted(users, key=users.get, reverse=True)
            await message.channel.send('```'
                                       + '\n' + "Baker Street's Top Ten:"
                                       + '\n' + '1st Place:  @' + str(await client.fetch_user(ranking[0])) + '  |   '
                                       + '[Account Balance: ' + users[ranking[0]] + '€' + ']'
                                       + '\n' + '2nd Place:  @' + str(await client.fetch_user(ranking[1])) + '  |   '
                                       + '[Account Balance: ' + users[ranking[1]] + '€' + ']'
                                       + '\n' + '3rd Place:  @' + str(await client.fetch_user(ranking[2])) + '  |   '
                                       + '[Account Balance: ' + users[ranking[2]] + '€' + ']'
                                       + '\n' + '4th Place:  @' + str(await client.fetch_user(ranking[3])) + '  |   '
                                       + '[Account Balance: ' + users[ranking[3]] + '€' + ']'
                                       + '\n' + '5th Place:  @' + str(await client.fetch_user(ranking[4])) + '  |   '
                                       + '[Account Balance: ' + users[ranking[4]] + '€' + ']'

                                       + '\n' + '6th Place:  @' + str(await client.fetch_user(ranking[5])) + '  |   '
                                       + '[Account Balance: ' + users[ranking[5]] + '€' + ']'
                                       + '\n' + '7th Place:  @' + str(await client.fetch_user(ranking[6])) + '  |   '
                                       + '[Account Balance: ' + users[ranking[6]] + '€' + ']'
                                       + '\n' + '8th Place:  @' + str(await client.fetch_user(ranking[7])) + '  |   '
                                       + '[Account Balance: ' + users[ranking[7]] + '€' + ']'
                                       + '\n' + '9th Place:  @' + str(await client.fetch_user(ranking[8])) + '  |   '
                                       + '[Account Balance: ' + users[ranking[8]] + '€' + ']'
                                       + '\n' + '10th Place: @' + str(await client.fetch_user(ranking[9])) + '  |   '
                                       + '[Account Balance: ' + users[ranking[9]] + '€' + ']'
                                       + '\n' + '```')

        if message.content.startswith('/permissions'):
            global new_mod
            try:
                requested_user_rank = message.content.split(' ')[1]
            except IndexError:
                requested_user_rank = str(message.author.id)

            if requested_user_rank in users:
                if str(requested_user_rank) in mods:
                    await message.channel.send('```'
                                                + '\n' + 'Showing Permissions for: ' + str(await client.fetch_user(requested_user_rank))
                                                + '\n \n' + 'Ranks: Moderator, Player'
                                                + '\n' + '```')
                else:
                    await message.channel.send('```'
                                                + '\n' + 'Showing Permissions for: ' + str(await client.fetch_user(requested_user_rank))
                                                + '\n \n' + 'Rank: Player'
                                                + '\n' + '```')
            else:
                await message.channel.send("User konnte nicht in der Datenbank gefunden werden")

        if message.content.startswith('/mod'):
            global new_mod

            new_mod = message.content.split(' ')[1]
            if str(message.author.id) in mods:
                if new_mod not in mods:
                    add_mod()
                    await message.channel.send('`Added new mod: ' + str(await client.fetch_user(new_mod)) + '`')
                    print(message.author + ' added ' + new_mod + ' to mods')
                    print("----------------------------------------------------------")
                else:
                    await message.channel.send('`' + str(await client.fetch_user(new_mod)) + ' is already a mod`')
                    print(message.author + ' tried to add ' + new_mod + ' to mods')
                    print('Error: User is already a mod')
                    print("----------------------------------------------------------")
            else:
                await message.channel.send('Fehlende Berechtigungen: Der befehl konnte nicht ausgeführt werden.')
                print(message.author + ' tried to add ' + new_mod + ' to mods')
                print('Error: User is already a mod')
                print("----------------------------------------------------------")

        if message.content.startswith('/give'):
            global newbalance
            global username
            global user_id
            global user_balance

            user_balance = message.content.split(' ')[1]
            user_balance = user_balance.split(':')
            userid = user_balance[0]
            try:
                newbalance = str(user_balance[1])
            except IndexError:
                await message.channel.send('Geld konnte nicht hinzugefügt werden')
            old_balance = users[userid]
            if str(message.author.id) in mods:
                if str(userid) in users:
                    os.remove('users.txt')
                    open("users.txt", "x")
                    with open("users.txt", "r+") as users_file:
                        users[str(userid)] = newbalance
                        for k in users.keys():
                            users_file.write("{}:{}\n".format(k, users[k]))

                        users_file.close()
                    print('Old Balance: ' + str(old_balance) + '€')
                    print('New Balance: ' + str(users[str(userid)]) + '€')
                    print("----------------------------------------------------------")
                    await message.channel.send("Changed Account Balance of " + str(await client.fetch_user(userid))
                                               + " to " + newbalance + '€')
                else:
                    print('Error: Userid not found')
            else:
                await message.channel.send('Fehlende Berechtigungen: Die Account balance konnte nicht verändert werden.')
                print(str(message.author) + ' tried to change the account balance of '
                      + str(await client.fetch_user(userid)) + ' from ' + users[userid] + ' to: ' + newbalance + '€')
                print("----------------------------------------------------------")


        if message.content == '/register':
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

        if message.content == '/start r':
            time.sleep(0.5)
            await message.channel.send(
                "`Das Spiel beginnt in 45 Sekunden, um dich zu registrieren schreibe '/register'`")

        if message.content.startswith("/tip"):
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

            try:
                tip = message.content.split(' ')[1]
            except IndexError:
                await message.channel.send('Dein Einsatz konnte nicht hinterlegt werden, bitte versuche es nochmal.')
                print(str(message.author))
                print('Error: Invalid Input')
                print("----------------------------------------------------------")
                return

            print(str(message.author))
            print('Tip: ' + tip)

            if str(tip) == 'x':
                await message.channel.send(" Dein Einsatz konnte nicht hinterlegt werden, gebe anstatt 'x' eine Zahl von 00 bis 36 ein.")

            result = random.randint(-1, 36)
            if result == -1:
                result = '00'
            print('Correct Number: ' + str(result))

            try:
                if int(tip) > 36:
                    print("Error: invalid tip")
                    print("----------------------------------------------------------")
                    await message.channel.send('Dein Einsatz konnte nicht hinterlegt werden, bitte versuche es nochmal.')
                    return
                else:
                        clrwin = -1
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
                # error = 1 == no color detected
                if error == 1:
                    await message.channel.send(
                        'Dein Einsatz konnte nicht hinterlegt werden, bitte versuche es nochmal.')
                    print('Error: invalid color')
                    print("----------------------------------------------------------")
                    return







client = MyClient()
client.run("NDY4NzM5NzY3ODQwODAwNzY5.W03R7Q.jfybjYfxEhCcBtfeY3ukx793AFs")