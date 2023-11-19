import os
import json
import sys
import discord
import requests
import base64
import time
from discord.ext import commands, tasks
import pytz
import logging
import functools
from logging import debug
import calendar
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
dates_check = {}
months_check = {}
days_check = {}
checking = {}
bdayRun = {}
"""Notes: Any json files that use the guild id should be in the form of the raw guild id, not a string of it
The entirety of the webhook function (probably) is fixed
At the moment the bdayRun dictionary is assigned upon running but it may be added to a database in case the bot randomly restarts. However, this should not be a problem with other hosting services

The following files with be moved to a database:
guild_channels.json
guilds.json
role_ids.json
birthdays.json
correct_birthdays.json
guessed_birthdays.json

The setup command should be restricted to server admins and should only be able to used once per server. Use times after the initial setup should overwrite role ids and delete previous roles
"""

# Any errors related to the logging.debug stuff is because I was lazy and selected all the phrases "print" at once and replaced it with logging.debug
debug("Debug working")


months = [
    '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'
]





# The current webhook secret needs to be changed to the webhook you want
"""
Before Running (!)
run "pip install discord pycord py-cord"
"""
intents = discord.Intents.all()
intents.message_content = True

bot = discord.Bot(command_prefix=".", intents=intents)

token = os.environ["token"]

channel = "general"


def redefine_function():
  global webhook

  # Redefine the function with the new implementation
  async def webhook(message):

    import os
    import random
    import calendar
    import requests


    weekDays = list(calendar.day_name)

    holidays = [
        'New Year', 'Chinese New Year', 'Easter', 'Halloween',
        'Valentine\'s Day', 'Independence Day', 'Thanksgiving', 'Earth Day',
        'St. Patrick\'s Day'
    ]
    holidays.append('Merry Christmas')

    months = list(calendar.month_name[1:])
    # The list only uses indexes 1 and on because the 0 index is blank
    
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    # List of dates in each month
    dates = [d for i, x in enumerate(days, 1) for d in range(1, x + 1)]
    guildid = message.guild.id
    guild = bot.get_guild(int(guildid))
    user_count = len([x for x in guild.members if not x.bot])
    people = int(user_count) + 1
    # Decide if it's a leap year
    if random.randint(1, 4) == 1:
      dates.append(29)

    def formatList(items):
      if len(items) == 0:
        return ''
      elif len(items) == 1:
        return items[0]
      else:
        return f"{', '.join(items[:-1])} & {str(items[-1])}"

    def ordinal(n: int) -> str:
      if 10 < n < 20:
        suffix = "th"
      elif n % 10 == 1:
        suffix = "st"
      elif n % 10 == 2:
        suffix = "nd"
      elif n % 10 == 3:
        suffix = "rd"
      else:
        suffix = "th"

      return f"{n}{suffix}"

    content = ''
    if random.randint(1, len(dates)) == 1:
      numBirthdays = sum(1 for _ in range(people))
    
    selMonths = []
    selDates = []
    selWeekDays = []
    selHolidays = []

    # For a repetition of 12 times, the program randomly selects a number between 1 and 12 inclusive and checks if it is equal to 1
    # If it is equal to 1, then it randomly selects one of the months (defined above) and appends it to list selMonths (defined above)
    for i in range(12):
      if random.randint(1, 12) == 1:
        selMonths.append(random.choice(months))
    """As I did not write the code for the dates definition, I don't actually know how that works.
    However, from what I understand, it generates the number of dates somehow. The code below iterates through that many times and checks if a random number between 1 and the number of dates inclusive is 1. If it is, it randomly selects one of the dates and appends it to the list of dates."""
    for i in dates:
      if random.randint(1, len(dates)) == 1:
        date = random.choice(dates)
        selDates.append(dates)
    # For each of the days of the week (7), if a random number between 1 and 7 inclusive is 1, then the program will randomly select one of the days of the week and append it to the list
    for i in range(7):
      if random.randint(1, 7) == 1:
        selWeekDays.append(random.choice(days))

    # For a repetition of the number of values in the holidays list (as of writing this there are 9 and the appended value of "Merry Christmas for 10"), the program randomly selects a number of 1 and 365, checks if it is equal to 1 and, if so, randomly selects one of 10 holidays and appends it to the list of selHolidays (defined above).
    for i in holidays:
      if random.randint(1, 365) == 1:
        holiday = random.choice(holidays)
        selHolidays.append(holiday)
    selHolidays = [i for i in holidays if randint(1, 365) == 1]
    # From what I understand (again, i didn't write this part of the code), the below is like this for formatting. If there are no months selected, then the program simply states the date, but if not, then it formats it so that it says that it is the month's day (ex. January 1)
    if len(selMonths) == 0:
      if len(selDates) != 0:
        content += f"Today is the {formatList(list(map(ordinal, selDates)))}.\n"
    else:
      if len(selDates) == 0:
        content += f"Today is in {formatList(selMonths)}.\n"
      else:
        content += f"Today is {formatList(selMonths)} {formatList(list(map(ordinal, selDates)))}.\n"

    if len(selWeekDays) > 0:
      content += 'Happy ' + formatList(selWeekDays) + '!\n'

    if numBirthdays > 1:
      content += 'Happy birthday to ' + str(
          numBirthdays) + ' people! No one knows who.\n'
      with open('guessed_birthdays.json', 'r') as file:
        guessed = json.load(file)
      guessed[guild_id] = "True"
    elif numBirthdays > 0:
      content += 'Happy birthday to someone! No one knows who.\n'
      guessed = 'True'
      

    if len(selHolidays) > 0:
      if selHolidays[
          0] == 'Merry Christmas':  # Christmas is always last in the list
        content += 'Merry Christmas!\n'
      else:
        content += 'Happy ' + formatList(selHolidays) + '!\n'


    for i in selMonths:
      logging.debug(f"I: {i}")
      logging.debug(f'Month: {str(time.strftime("%B"))}')
      logging.debug(str(time.strftime('%B')))
      logging.debug("")
      if str(i) == str(time.strftime('%B')):
        
        logging.debug('True')
        
        global months_check
        months_check[message.guild.id] = "True"
        
        

    for i in selWeekDays:
      logging.debug(f"I: {i}")
      logging.debug(f"Day: {str(time.strftime('%A'))}")
      
      
      if str(i) == str(time.strftime('%A')):
        logging.debug('True')
        global days_check
        days_check[message.guild.id] = "True"
        
        

    for i in selDates:
      logging.debug(f"I: {i}")
      logging.debug(f"Date: {str(time.strftime('%d'))}")
      
      if str(i) == str(time.strftime('%d')):
        logging.debug('True')
        global dates_check
        dates_check[message.guild.id] = "True"

        

    # content = ' Happy '
    # if randint() == 0: content += choice(days)
    # if randint() == 0: content +=

    # if randint(0,6) == 0:
    #     content += '\n@birthday cake Happy birthday to someone! No one knows who.'

    # if randint(0,45) == 0:
    #     content += '\nHappy ' + choice(holidays)

    # request = {'content': content}
    
    if content == '':
      content = 'Nothing special happens today, which is actually kinda special in and of itself!'
    logging.debug(content)
    with open("correct_birthdays.json", "r") as file:
      correctBirthdaysAll = json.load(file)
    correctBirthdays = correctBirthdaysAll[str(message.guild.id)]

    bonusCorrectBirthdays = ['David Wang', 'Paige Johnson', 'Liam Ryan']
    cbContent = str(len(correctBirthdays)) + ' birthdays correct so far!\n'
    cbContent += 'Correct birthdays: ' + formatList(correctBirthdays) + '!'
    cbContent += '\nBonus birthdays: ' + formatList(
        bonusCorrectBirthdays) + '!'
    with open("guild_channels.json", "r") as file:
      guild_channels = json.load(file)
    channel_id = guild_channels[message.guild.id]
    channel = await bot.fetch_channel(int(channel_id))
    webhook = await channel.create_webhook(name="Birthday Bot", avatar='https://media.discordapp.net/attachments/914225845260914728/1016591595950321725/birthday-cake-twitter.png', reason="Birthday Bot Was Triggered")

    embed1 = discord.Embed(title=None, content=content, color = 0xF4ABBA)
    embed2 = discord.Embed(title=None, content=cbContent, color= 0xEB566C)
    
    with open("role_ids.json", "r") as file:
      role_ids = json.load(file)
    
    role_id = role_ids[message.guild.id]
    await webhook.send(content="<@&{role_id}>\n", embeds=(embed1, embed2))

    await webhook.delete
    global checking
    checking[message.guild.id] = "True"
    





  logging.debug("Function Redefined")


@bot.event
async def on_ready():
  logging.debug(f'Logged in as {bot.user}')
  activity = discord.Game(name="Happy Birthday")
  await bot.change_presence(status=discord.Status.offline)

@bot.command()
async def role(ctx):
    with open("role_ids.json", "r") as file:
      roleids = json.load(file)
    role_id = roleids[str(message.guild.id)]
    role = message.guild.get_role(role_id)
    if role is not None:
      await ctx.author.add_roles(role)
      await ctx.respond('Added Role!')

    else:
      await ctx.respond("Role not found.")
@bot.command()
async def setup(ctx, channel : discord.TextChannel):
  channel = channel.id
  with open("guild_channels.json", "r") as file:
    channels = json.load(file)
  channels[ctx.guild.id] = channel
  guild = ctx.guild
  role = await guild.create_role(name="Birthday Cake")
  roleid = role.id
  with open('role_ids.json', "r") as file:
    role_ids = json.load(file)
  role_ids[int(guild.id)] = roleid
  with open("role_ids.json", "w") as file:
    json.dump(role_ids, file)
  await ctx.respond(f"Channel ID has been set and <@&{roleid}> has been created")
birthday = bot.create_group("birthday")
@birthday.command(name='set')
async def set_birthday(ctx, month, date):
  months = list(calendar.month_name)
  if str(month) in months:
    month_index = months.index(str(month))
    monthrange = calendar.monthrange(2000, month_index)
    if int(date) > len(monthrange):
      await ctx.respond("Invalid Day for Month Provided")
      raise Exception("Invalid Day for Month Given")
    else:
      pass
  else:
    await ctx.respond("Invalid Month Provided")
    raise Exception("Invalid Month Provided")
  logging.debug(f"Month: {month}")
  logging.debug(f"Day: {date}")

  birthday = (f"{month}/{date}")
  with open("birthdays.json", "r") as file:
    birthdaysAll = json.load(file)
  user_id = ctx.author.id
  found = False
  birthdays = birthdaysAll[str(guild_id)]
  for key in birthdays:
    if key == str(user_id):
      await ctx.respond(
          "You have already set your birthday! Please use /birthday change to change your birthday"
      )
      found = True
  if not found:
    birthdays[user_id] = birthday
    await ct.xrespond("Successfully Assigned Birthday")

  with open("birthdays.json", "w") as file:
    json.dump(birthdays, file)
  logging.debug(time.strftime("%m/%d"))
@bot.event
async def on_message(message):
  logging.debug(message.author)
  guild_id = int(message.guild.id)
  debug(guild_id)
  with open("guilds.json", "r") as file:
    guilds = json.load(file)
  if message.guild.id not in guilds:
    guilds.append(guild_id)
    with open('guilds.json', "w") as file:
      json.dump(guilds, file)
    with open('birthdays.json', "r") as file:
      birthdays = json.load(file)
    birthdays[int(guild_id)] = {}
    with open('birthdays.json', "w") as file:
      birthdays = json.dump(birthdays, file)
    checking[int(guild_id)] = "False"
    with open('correct_birthdays.json', "r") as file:
      correct_birthdays = json.load(file)
    correct_birthdays[guild_id] = {}
    with open('correct_birthdays.json', "w") as file:
      correct_birthdays = json.dump(correct_birthdays, file)

        
  else:
    pass
  
  debug("Continue")
  guild_id = message.guild.id
  redefine_function()
  if not guild_id in checking:
    checking[guild_id] = "False"
  if checking[guild_id] == "True":
    if message.author == "Birthday Bot#0000":
      if months_check[guild_id] == 'True':
        await message.add_reaction('🇲')
        logging.debug('Added or Attempted to Add Reaction')

        months_check[guild_id] = "False"
        
      if days_check[guild_id] == 'True':
        days_check[guild_id] = "False"
        await message.add_reaction('📆')

      if dates_check[guild_id] == 'True':
        dates_check[guild_id] = "False"
        await message.add_reaction('🇩')

  
      elif str(imonth) == 'False' and str(idate) == 'False' and str(
          iday) == 'False':
        logging.debug('Nothing')
        await message.add_reaction('❌')
        message_id = message.id

      with open("guessed_birthdays.json", "r") as file:
        guessed_birthday_all = json.load(file)
      guessed_birthday_guild = guessed_birthday_all[guild_id]
      if guessed_birthday_guild == "True":
        day = time.strftime("%M/%d")
        for key in birthdays:
          if birthdays[key] == day:
            message = f"Happy Birthday to <@{key}>!"
            embed = discord.Embed(title="Birthday Guessed", content=message)
            embed.set_footer("User automatically added to server's list")
            message = await message.channel.send(embed=embed)
            await message.add_reaction('🎂')
            with open("correct_birthdays.json", "r") as file:
              birthdaysAll = json.load(file)
            
            birthdays = birthdaysAll[str(guild_id)]
            birthdays.append(f"<@{key}>")
            birthdaysAll[guild_id] = birthdays
            with open('correct_birthdays.json', "w") as file:
              json.dump(file, birthdaysAll)
            
          else:
            return
        with open("guessed_birthdays.json", "r") as file:
          guessed_birthday_all = json.load(file)
        guessed_birthday_all[guild_id] = "False"
        with open('guessed_birthdays.json', "w") as file:
          json.dump(file, guessed_birthday_all)
      
      if guessed_birthday_guild == "False":
        day = time.strftime("%M/%d")
        for key in birthdays:
          if birthdays[key] == day:
            message = f"Happy Birthday to <@{key}>!"
            embed = discord.Embed(title="Missed Birthday", content=message)
            embed.set_footer("User automatically added to server's list")
            message = await message.channel.send(embed=embed)
            await messsage.add_reaction('🎂')
            with open("correct_birthdays.json", "r") as file:
              birthdaysAll = json.load(file)
            birthdays = birthdaysAll[guild_id]
            birthdays.append(f"<@{key}>")
            birthdaysAll[guild_id] = birthdays
            with open('correct_birthdays.json', "w") as file:
              json.dump(file, birthdaysAll)
          else:
            return
          
            

  elif message.author == bot.user:
    return
  
  if message.content.lower() == 'setup start':
    await message.channel.send("Please send the following message: '.setup <channel you would like to use i.e. #birthdays>' and the channel will be set. Additionally, a 'birthday cake' role will be created. Please send 'birthday help' for more info on how the bot works. Yes, you do need the . before setup")
  
  elif message.content.lower().startswith('birthday?'):
    guild_ids = []
    guild_id = message.guild.id
    with open('guild_channels.json', 'r') as file:
      guildChannels = json.load(file)
    for key in guildChannels:
      guild_ids.append(key)
    if not guild_id in channels:
      await message.channel.send("Your server has not yet set a channel for birthday bot to be run in. Please set one before proceeding. Please send 'setup start' to proceed")
    channel = guildChannels[guild_id]
    if message.channel.id == channel:
      if not guild_id in bdayRun:
        bdayRun[guild_id] = "False"
      if bdayRun[guild_id] == "True":
        confirm = await message.channel.send("It appears Birthday Bot was already run in this server. Please react with ✅ to confirm you would like to run Birthday Bot. Or react with ❌ to cancel")
        author = message.author
        confirm = '✅'
        cancel = '❌'
        valid_reactions = ['✅', '❌']
        def check(reaction, user):
          return user == author and str(reaction.emoji) in valid_reactions
        await bot.wait_for('reaction_add', timeout=60.0, check=check)
        if str(reaction.emoji) == confirm:
          await message.channel.send("Confirmed")
          webhook = functools.partial(webhook, message)
          webhook()
        await message.channel.send("Cancelled")
        await message.delete

        confirm.add_reaction("✅")
        confirm.add_reaction("❌")
      else:
        webhook = functools.partial(webhook, message)
        webhook()
        
        bdayRun[guild_id] = "True"

    

  elif message.content.lower() == 'test':
    await message.channel.send('Test')
    debug("Test Successful")
  elif message.content.lower() == 'status':
    await message.channel.send('Bot functional')
    now = time.strftime("%H:%M:%S")
    await message.channel.send(now)
    await message.channel.send('** **')


  elif message.content.lower() == 'remove':
    role_id = int(roleid)  # replace with your role ID
    role = message.guild.get_role(role_id)
    if role is not None:
      await message.author.remove_roles(role)
      await message.channel.send('Removed role')
    else:
      await message.channel.send("Role not found.")
  elif message.content.lower() == 'test redefine':
    await message.channel.send("Testing Redefinition of ```webhook()```")
    redefine_function()

  elif message.content.lower() == 'triggers' or message.content.lower(
  ) == 'birthday help':
    with open("role_ids.json", "r") as file:
      role_ids = json.load(file)
    try:
      roleid = role_ids[str(message.guild.id)]
      embed = discord.Embed(title="Bot Message Triggers",
        description=f"""
      ```Remove```  Remove <@&{int(roleid)}>
      ```Role```  Assign <@&{int(roleid)}>
      ```Triggers```  Receive this embed
      ```Birthday help```  Receive this embed
      ```Test redefine```  Test a redefinition of the **webhook** function
      ```Birthday?```  Run the webhook (Once per day)
      ```Birthday: MM/DD```  Set your birthday
      ```Change birthday: MM/DD```  Change Your Birthday""")
      embed.set_footer(
          text=
          "Note that triggers are not case sensitive. Additionally, support can be sent to the bot's direct messages"
      )
    except Exception as e:
      debug(f"Error: {e}")
      debug("")
      embed = discord.Embed(title="Bot Message Triggers",
        description=f"""
      ```Remove```  Remove `role not setup`
      ```Role```  Assign `role not setup`
      ```Triggers```  Receive this embed
      ```Birthday help```  Receive this embed
      ```Test redefine```  Test a redefinition of the **webhook** function
      ```Birthday?```  Run the webhook (Once per day)
      ```Birthday: MM/DD```  Set your birthday
      ```Change birthday: MM/DD```  Change Your Birthday""")
      embed.set_footer(
          text=
          """Note that triggers are not case sensitive. Additionally, support can be sent to the bot's direct messages
          `Bot has not been fully setup in this server`"""
      )
    
    await message.channel.send(embed=embed)

  

  elif message.content.lower().startswith("change birthday: "):

    content = message.content.lower()
    content = list(content)
    for i in range(17):
      content.remove(content[0])
    content.remove('/')
    logging.debug(content)
    logging.debug(len(content))
    month = (content[0] + content[1])
    day = (content[2] + content[3])
    logging.debug(month)
    logging.debug(day)
    if len(content) != 4:
      await message.channel.send("Invalid Date Provided")
      raise Exception("Invalid Date")
    if month not in months:
      await message.channel.send("Invalid Month")
      raise Exception("Invalid Month")
    else:
      if int(day) <= 0:
        await message.channel.send("Invalid Day")
        raise Exception("Invalid Day")
      if str(month) in ('01', '03', '05', '07', '08', '10', '12'):
        if int(day) > 31:
          await message.channel.send("Invalid Day for Month Provided")
          raise Exception("Invalid Day for Month Given")
        else:
          pass
      elif str(month) == '02':
        if int(day) > 29:
          await message.channel.send("Invalid Day for Month Provided")
          raise Exception("Invalid Day for Month Given")
        else:
          logging.debug("Valid Date")

      elif str(month) in ("04", '06', '09', '11'):
        if int(day) > 30:
          await message.channel.send("Invalid Day for Month Provided")
          raise Exception("Invalid Day for Month Given")
        else:
          logging.debug("Valid Date")

      else:
        logging.debug("No Error")
    logging.debug(f"Month: {month}")
    logging.debug(f"Day: {day}")

    birthday = (f"{month}/{day}")
    with open("birthdays.json", "r") as file:
      birthdays = json.load(file)
    user_id = message.author.id
    birthdays[guild_id][user_id] = birthday
    with open("birthdays.json", "w") as file:
      json.dump(birthdays, file)
    logging.debug(time.strftime("%m/%d"))
    await message.channel.send(f"Changed Birthday to {birthday}")
  else:
    for key in months_check:
      month[key] = "False"
    for key in days_check:
      day[key] = "False"
    for key in dates_check:
      date[key] = "False"
    
    logging.debug(message.channel)
    


@bot.event
async def on_member_join(member):
  redefine_function()
  embed = discord.Embed(
      title=None,
      description=
      """We need to know your birthday so that we can add more features to the bot. Please use the following format to provide us your birthday:
      Birthday: MM/DD

      Example:
      Birthday: 06/09
    
      ```Months:
      January: 01
      February: 02
      March: 03
      April: 04
      May: 05
      June: 06
      July: 07
      August: 08
      September: 09
      October: 10
      November: 11
      December: 12```

      You should receive a message in response confirming that your birthday was assigned.
      """)

  await member.send(embed=embed)

@tasks.loop(seconds=60)
async def check_time():
  if str(time.strftime("%h")) == "0" or str(time.strftime("%h")) == "00":
    
    for key in bdayRun:
      bdayRun[key] = False
  else:
    pass
  


logging.debug('Ran Webserver')
logging.debug(f"Current Time: {time}")

bot.run(token)
