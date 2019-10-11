import discord
from discord.ext.commands import Bot
import asyncio
import json
import requests
import time
from discord.ext import commands
from PIL import Image
import sys, os
import random
import hashlib


#Define write to json
def file_read(folder, fname):
    catched = open(path + "/" + folder + "/" + fname, "r")
    lines = catched.readlines()
    catched.close()
    return lines
def clear_file(folder, fname):
    open(path + "/" + folder + "/" + fname, 'w').close()
def file_append(folder, fname, append):
    p = (path + "/" + folder + "/" + fname)
    f = open(p, "a")
    f.write(append + " ")
    f.close()
def add_pokemon(name):
    try:
        with open(path + "/User/customs.json") as cs:
            jsdecoded = json.load(cs)
            jsdecoded[str(name)] = ""
        with open(path + "/User/customs.json", 'w') as jfil:
            json.dump(jsdecoded, jfil)
    except Exception as e: print(e)
def write_json(wrtline, wrt):
    try:
        with open(path + "/preferences.json") as pr:
            jsdecoded = json.load(pr)
            jsdecoded[str(wrtline)] = str(wrt)
        with open(path + "/preferences.json", 'w') as jfil:
            json.dump(jsdecoded, jfil)
    except Exception as e: print(e)
#Path
path = os.path.dirname(os.path.abspath(sys.argv[0])).replace("/WebServer", "")
#Presets
with open (path + "/preferences.json") as p:
    prefs = json.load(p)
with open (path + "/User/guilds.json") as g:
    guild_list = json.load(g)
    g.close()
#Start
#Pref
client = commands.Bot(command_prefix='_')

#Defines
def gethash(img):
    with open (img, "rb") as h:
        md = hashlib.md5(h.read()).hexdigest()
        h.close()
    return md
##########

#Lists
with open (path + '/Lists/hashes.json') as h:
    hashdata = json.load(h)

#End

#Ready
@client.event
async def on_ready():
    user_guilds = client.guilds
    for guild in user_guilds:
        try:
            if(guild_list[str(guild.id)]):
                guild_list[str(guild.id)] = [guild_list[str(guild.id)][0], guild.name, guild.icon]
        except:
            guild_list[str(guild.id)] = ["True", guild.name, guild.icon]
    try:
        with open (path + "/User/guilds.json", 'w') as clr_guilds:
            clr_guilds.write("{}")
            clr_guilds.close()
        with open(path + "/User/guilds.json", 'w') as jfil:
            json.dump(guild_list, jfil)
    except Exception as e: print(e)
    print("JokerCord is connected and running. Version : BETA 0.0.4b")
    try:
        if(prefs["auto_spam"] == "True"):
            while(1):
                #try:
                if(prefs["auto_spam_interval"] == "R"):
                    channel = client.get_channel(int(prefs["auto_spam_channel"]))
                    await channel.send(prefs["auto_spam_text"])
                    rand = random.randrange(1, 20)
                    await asyncio.sleep(rand)
                else:
                    channel = client.get_channel(int(prefs["auto_spam_channel"]))
                    await channel.send(prefs["auto_spam_text"])
                    await asyncio.sleep(int(prefs["auto_spam_interval"]))
    except:
        print("Something went wrong with the channel id.")
    
@client.event
async def on_message(message):
    ev = 1
    #Get the embed message
    try:
        embed = message.embeds[0]
    except IndexError:
        ev = 0
    #Check if message is from Pokecord Spawn
    if (message.author.id != client.user.id and ev == 1 and (guild_list[str(message.guild.id)][0] == "True")): #and "A wild" in message.content):
        
        try:
            url = embed.image.url
            try:
                    if 'discordapp' not in url:
                        return
            except TypeError:
                    return
            #print(url)
            #Open image and save it to JPG
            openimg = open(path + '/Assets/pokemon.jpg','wb')
            openimg.write(requests.get(url).content)
            openimg.close()
            await asyncio.sleep(1)
            

                #Get hashes

            mdhash = gethash(path + '/Assets/pokemon.jpg')
            #Compare hashes with the lists
            save_line = None
            
            for i in hashdata:
                
                if (hashdata[i] == mdhash):
                    save_line = i
                    break
            
            
            if(prefs["custom_list"] == "True"):
                if(save_line in custom_list):
                    await message.channel.send("p!catch " + save_line.lower())
                    if (save_line not in file_read("User", "caught.txt")):
                        file_append("User","caught.txt",save_line)
            else:
                await message.channel.send("p!catch " + save_line.lower())
                if (save_line not in file_read("User", "caught.txt")):
                    file_append("User","caught.txt",save_line)      
                    
                else:
                    return
        except AttributeError:
            return
    


 