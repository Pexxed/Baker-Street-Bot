import discord
import random
import time
import fileinput

mods = ['Chris♚#4498']
leaderboard = {}
roulette_black = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
roulette_green = ['0', '00']
roulette_even = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35]
roulette_onetoeiteen = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
roulette_firsttwelve = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
roulette_secondtwelve = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
roulette_thirtwelve = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
users = {}
userlist = []
messagecode = 0

try:
    with open("users.txt", "r") as users_file:
        for line in users_file:
            if line.strip():
                user, wealth = line.strip().split(':')
                users[user] = wealth
                userlist.append(user + ':' + users[user])
        users_file.close()
except FileNotFoundError:
    users = {}

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
                                       + '\n' + '/help | /leaderboard | /stats | /register'
                                       + '\n' + '--------------------------------------------------------------------------'
                                       + '\n' + 'Roulette:'
                                       + '\n' + '/start r | /tip black | /tip red | /tip green | /tip x' + '```')

        if message.content == '/leaderboard':
            ranking = sorted(users, key=users.get, reverse=True)
            await message.channel.send("```Baker Street's Top Ten:"
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
                                       + '[Account Balance: ' + users[ranking[9]] + '€' + ']' + '```')

        if message.content.startswith('/set.balance'):
            global newbalance
            global username
            global user_id
            global user_bal

            user_balance = message.content.split(' ')[1]
            user_balance = user_balance.split(':')
            userid = user_balance[0]
            user_bal = user_balance[1]

            if str(message.author) in mods:
                print(str(message.author) + ' changed the Account balance of ' + str(
                    await client.fetch_user(userid)) + ':')
                print('Old Balance: ' + users[userid] + '€')
                for line in fileinput.input('users.txt', inplace = 1):
                    line.replace(str(userid) + ':' + users[userid], str(userid) + ':' + user_bal),
                print('New Balance: ' + users[userid] + '€')
                print("----------------------------------------------------------")


            else:
                await message.channel.send('Fehlende Berechtigungen: Die Account balance konnte nicht verändert werden.')
                print(str(message.author) + ' tried to change the account balance of '
                      + str(await client.fetch_user(userid)) + ' from ' + users[userid] + 'to: ' + user_bal + '€')
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

            nmbwin = 0
            clrwin = 0
            eowin = 0
            first12 = 0
            second12 = 0
            third12 = 0
            farbe = '0'
            zahl = -1
            error = 0

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
                else:
                    nmbwin = -1
                    print('Lost Zahlentest')

            async def farbentest():
                global clrwin
                global farbe
                global result

                if farbe == -1 and result in roulette_black:
                    clrwin = 1
                    print('Won Farbentest')
                    return
                elif farbe == -1 and result not in roulette_black:
                    clrwin = -1
                    print('Lost Farbentest')
                    return
                if farbe == -2 and result not in roulette_black:
                    clrwin = 1
                    print('Won Farbentest')
                    return
                elif farbe == -2 and result in roulette_black:
                    clrwin = -1
                    print ('Lost Farbentest')
                    return
                elif farbe == -3 and str(result) in roulette_green:
                    clrwin = 1
                elif farbe == -3 and str(result) not in roulette_green:
                    clrwin = -1
                    return
                else:
                    clrwin = -1
                    print('No Color')
                    return

            async def gerade_ungerade():
                global result
                global zahl
                global eowin
                global error

                try:
                    if tip == 'odd' or tip == 'ungleich':
                        if int(tip) not in roulette_even:
                            eowin = 1
                            error = 0
                        if int(tip) in roulette_even:
                            eowin = -1
                            error = 0
                    if tip == 'even' or tip == 'gleich':
                        if int(tip) in roulette_even:
                            eowin = 1
                            error = 0
                        if int(tip) not in roulette_even:
                            eowin = -1
                            error = 0
                except:
                    error = 1

            async def resulttest():
                global nmbwin
                global clrwin
                global win
                global eowin
                global first12
                global second12
                global third12
                global result

                if result in roulette_black:
                    farbe_result = 'black'
                elif result in roulette_green:
                    farbe_result = 'green'
                else:
                    farbe_result = 'red'

                if nmbwin == 1 or clrwin == 1 or eowin == 1 or first12 == 1 or second12 == 1 or third12 == 1:
                    await message.channel.send('Du hast gewonnen! ' + '(' + str(result) + ' / ' + str(farbe_result) + ')')
                    print("----------------------------------------------------------")
                    return
                else:
                    await message.channel.send('Leider verloren ' + '(' + str(result) + ' / ' + str(farbe_result) + ')')
                    print("----------------------------------------------------------")
                    return

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
                    zahl = str(tip)

            except ValueError:
                await farbeninput()
                await gerade_ungerade()
                # error = 1 == no color detected
                if error == 1:
                    await message.channel.send(
                        'Dein Einsatz konnte nicht hinterlegt werden, bitte versuche es nochmal.')
                    print('Error: invalid color')
                    print("----------------------------------------------------------")
                    return

            if farbe != '0':
                nmbwin = -1
                print("No Number input")
                await farbentest()
            else:
                clrwin = -1
                print("No Color input")

                await zahlentest()

            await resulttest()



client = MyClient()
client.run("NDY4NzM5NzY3ODQwODAwNzY5.W03R7Q.jfybjYfxEhCcBtfeY3ukx793AFs")