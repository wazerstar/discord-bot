# Work with Python 3.6##########################################################
import random
import asyncio 
import discord
import requests
import json
import steamapi
import youtube_dl
import os
import matplotlib
import matplotlib.pyplot as plt
from imgurpython import ImgurClient
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from os import system

from faceit_data import FaceitData
#comes from laughinglove's faceit API Python wrapper
faceit_data = FaceitData("YOUR_API_KEY_HERE")

# tokens & Secrets #############################################################

steamapi.core.APIConnection(api_key="YOUR_STEAM_API_KEY_HERE", validate_key=True)

TOKEN = ''
botsecret = ''

MASTERS = [''] #define self

IMGUR_ID = ''

IMGUR_SECRET = 'YOUR_IMGUR_SECRET_HERE'

FOXID = 'my_discord_id'
#for testing discord py commands
ATFOX = '<@numbers_that_would_ping_me_in_discord>'

FOXTEXT = 'fox'
#for some old command I forgot about

Steam_api_key = ''

#basic message command template
"""
	if message.content.startswith('hello'):
		msg = 'Hello! {0.author.mention}'.format(message)
		await message.channel.send(msg)
		
"""
##############################################################################
#bot command prefix
client = commands.Bot(command_prefix = '!')

@client.command(pass_context=True, brief="Makes bot join channel")
async def join(ctx):
	channel = ctx.message.author.voice.channel
	if not channel:
		await ctx.send("Get in a channel?")
		return
	voice = get(client.voice_clients, guild=ctx.guild)
	if voice and voice.is_connected():
		await voice.move_to(channel)
	else:
		voice = await channel.connect()
	await voice.disconnect()
	if voice and voice.is_connected():
		await voice.move_to(channel)
	else:
		voice = await channel.connect()
	await ctx.message.add_reaction('❤️')

@client.command(pass_context=True, brief="bot leaves channel", aliases=['stop'])
async def leave(ctx):
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild=ctx.guild)
	if voice and voice.is_connected():
		await voice.disconnect()
		await ctx.message.add_reaction('💔')
		await ctx.send(":c")
	else:
		await ctx.send("??")

@client.command(pass_context=True, brief='plays music from youtube')
#plays music from youtube, usses ffmpeg and youtube-dl py 
async def yt(ctx, *args: str):
	channel = ctx.message.author.voice.channel
	if not channel:
		await ctx.send("Get in a channel?")
		return
	voice = get(client.voice_clients, guild=ctx.guild)
	if voice and voice.is_connected():
		await voice.move_to(channel)
	else:
		voice = await channel.connect()
	await voice.disconnect()
	if voice and voice.is_connected():
		await voice.move_to(channel)
	else:
		voice = await channel.connect()


	search_term = " ".join(args[:])
	songname = " ".join(args[:])
	search_term = search_term.replace(" ", "+")
	search_term1 = "'%s'" % search_term
	ytquery = "youtube-dl --no-playlist ytsearch1:" + "'" + search_term + "'" + " -x --audio-format mp3"
	await ctx.send("Now Playing: " + songname )

	song_there = os.path.isfile("song.mp3")
	try:
		if song_there:
			os.remove("song.mp3")
	except Exception:
		await ctx.send("uh.. something went really wrong")
		return

	voice = get(client.voice_clients, guild=ctx.guild)
	ydl_opts = {
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		os.system (ytquery)
	for file in os.listdir("./"):
		if file.endswith(".mp3"):
			os.rename(file, 'song.mp3')
	voice.play(discord.FFmpegPCMAudio("song.mp3"))
	voice.volume = 100
	voice.is_playing()

#plays youtube music from link into a voice channel
@client.command(pass_context=True, brief="bot plays a song !ytlink [url]")
async def ytlink(ctx, url: str):
	#queue? make a list!
	song_there = os.path.isfile("song.mp3")
	try:
		if song_there:
			os.remove("song.mp3")
	except Exception:
		await ctx.send("uh.. something went really wrong")
		return

	songtitle = youtube_dl.main(url +  '--get-title')
	await ctx.send(songtitle)


	voice = get(client.voice_clients, guild=ctx.guild)
	ydl_opts = {
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
	}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([url])
	for file in os.listdir("./"):
		if file.endswith(".mp3"):
			os.rename(file, 'song.mp3')

	voice.play(discord.FFmpegPCMAudio("song.mp3"))
	voice.volume = 100
	voice.is_playing()
#on_message events are basically commands, the line is blurred here but I suppose I should have used commands more than on_message
@client.event
async def on_message(message):
	#this prevents the bot from replying to itself
	if message.author == client.user:
		return

	if 'hello'.lower() in message.content.lower():
		msg = 'Hello! {0.author.mention}'.format(message)
		await message.channel.send(msg)
		
	if 'no u' in message.content.lower():
		await message.channel.send("no u")

	if message.content.lower() == '<@567213611374870528>' or message.content.lower() == 'bot?':
		await message.channel.send('yes?')
	#kills bot remotely
	if message.content == '!kill' :
		await killCommand(message)

	if message.content.startswith('!imgur'):
		await imgurCommand(message)

	if message.content.startswith('!r'):
		await reddit(message)

	if message.content.startswith('!help'):
		await help(message)

	if message.content.startswith('!faceithelp'):
		await faceithelp(message)

	if message.content.startswith('!youtubehelp'):
		await youtubehelp(message)	

	if message.content == '!getid':
		idstore = message.author.id
        await message.channel.send(idstore)

	if message.content.startswith('!lmgtfy'):
		await lmgtfy(message)

	if message.content.startswith('!aww'):
		await aww(message)

	if message.content.startswith('!reddit'):
		await reddit(message)

	if message.content.startswith('!elo'):
		await elo(message)

	if message.content.startswith('!kd'):
		await am_i_cracked(message)

	if message.content.startswith('!steamelo'):
		await steamelo(message)

	if message.content.startswith('!input'):
		await testinput(message)

	if message.content.startswith('!steamid'):
		await steamid(message)

	if message.content.startswith('!faceit64'):
		await faceit64(message)

	if message.content.startswith('!graph'):
		await graph(message)

	if message.content.startswith('!kdgraph'):
		await kdgraph(message)

	if message.content.startswith('!faceitid'):
		await faceit_id(message)

	if message.content.startswith('!trash'):
		await trash(message)

	await client.process_commands(message)

#help stuff
async def help(message):
	await message.channel.send("!faceithelp, !youtubehelp for more info")

async def youtubehelp(message):
	await message.channel.send("!yt plays songs from youtube, !ytlink plays a link from youtube")

async def faceithelp(message):
	await message.channel.send("!elo checks faceit elo using their faceit username")
	await message.channel.send("!faceit64 checks faceit elo using their steamid64 or vanityurl, <https://steamcommunity.com/id/[vanityurl]>")
	await message.channel.send("!steamelo uses their Steam username to get their faceit elo, if there's no answer it means that the name is common and it picked up someone else's account")
	await message.channel.send("!steamelo is a shortcut where specific long names can be used to get faceit elo, but short common names can be hit/miss")
####################################################################################
#faceit api stuff
#returns elo from faceit API from SteamID64 using steamapi
async def faceit64(message):
	vanityid = message.content.split(" ", 1)
	vanityidfiltered = vanityid[1]
	url = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=YOUR_STEAM_API_KEY_HERE&vanityurl=' + vanityid
	r = requests.get(url)
	json_array = r.json()

	if 'steamid' in json_array['response']:
		id64 = json_array['response']['steamid']
		REE = faceit_data.player_details(None, 'csgo', id64)
		resultelo = str((REE['games']['csgo']['faceit_elo']))
		await message.channel.send(resultelo + ' ELO')

	else:
		REE = faceit_data.player_details(None, 'csgo', vanityidfiltered)
		resultelo = str((REE['games']['csgo']['faceit_elo']))
		await message.channel.send(resultelo + ' ELO')
#uses steamapi to find an username's ID64, then returns their elo using faceitapi
#these functions are useful because you cannot get elo from steam, but you cannot get elo from their name, you need their steamid64
async def steamelo(message):
	vanityid = message.content[10:]
	url = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=YOUR_STEAM_API_KEY_HERE&vanityurl=' + vanityid.replace(" ", "")
	#await message.channel.send(url)
	r = requests.get(url)
	json_array = r.json()
	steamidnumber = json_array['response']['steamid']
	await message.channel.send('SteamID64: ' + json_array['response']['steamid'])

	if 'steamid' in json_array['response']:
		id64 = json_array['response']['steamid']
		REE = faceit_data.player_details(None, 'csgo', id64)
		resultelo = str((REE['games']['csgo']['faceit_elo']))

		await message.channel.send(resultelo + ' ELO')

	else:
		REE = faceit_data.player_details(None, 'csgo', vanityid)
		resultelo = str((REE['games']['csgo']['faceit_elo']))
		await message.channel.send(resultelo + ' ELO')
#just returns id64
async def steamid(message):
	vanityid = message.content.split(" ", 1)
	vanityidfiltered = vanityid[1]
	url = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=YOUR_STEAM_API_KEY_HERE&vanityurl=' + vanityidfiltered
	r = requests.get(url)
	json_array = r.json()
	steamidnumber = json_array['response']['steamid']
	await message.channel.send(json_array['response']['steamid'])
#returns current elo from faceit username
async def elo(message):
	nickn = message.content.split(" ", 1)
	name = nickn[1]
	REE = faceit_data.player_details(name, 'csgo')
	results = REE['games']['csgo']['faceit_elo']
	await message.channel.send(str(results)+ ' Elo')
#graphs lifetime elo in faceit using pyplot
async def graph(message):
	nickn = message.content.split(" ", 1)
	name = nickn[1]
	get_player_details = faceit_data.player_details(name, 'csgo')
	get_player_id = get_player_details['player_id']
	api_url = "https://api.faceit.com/stats/api/v1/stats/time/users/{}/games/csgo?size=2000".format(get_player_id)
	res = requests.get(api_url).json()
	i = 0
	elo_history = []
	for match in res:     
	    elo_history.append(res[i].get("elo", None))
	    i += 1

	elo_history = list(filter(None, elo_history)) 
	elo_history.reverse()
	matches = len(elo_history)

	for i in range(0, len(elo_history)): 
	    elo_history[i] = int(elo_history[i]) 
	    
	plt.style.use('dark_background')
	fig, ax = plt.subplots()
	ax.set_title("Faceit Elo Graph", fontsize= 24)
	ax.set_xlabel("Matches", fontsize=14)
	ax.set_ylabel("Elo", fontsize=14)
	ax.plot(elo_history)
	plt.savefig('graph.png')

	await message.channel.send(file=discord.File('graph.png'))
#graphs lifetime kd in faceit using pyplot
async def kdgraph(message):
	nickn = message.content.split(" ", 1)
	name = nickn[1]
	get_player_details = faceit_data.player_details(name, 'csgo')
	get_player_id = get_player_details['player_id']
	api_url = "https://api.faceit.com/stats/api/v1/stats/time/users/{}/games/csgo?size=2000".format(get_player_id)
	res = requests.get(api_url).json()
	i = 0
	elo_history = []
	for match in res:     
	    elo_history.append(res[i]['c2'])
	    i += 1
	elo_history.reverse()
	matches = list(range(1,101))

	for i in range(0, len(elo_history)): 
	    elo_history[i] = float(elo_history[i]) 
	plt.style.use('dark_background')
	fig, ax = plt.subplots()
	ax.set_title("Faceit K/D Graph", fontsize= 24)
	ax.set_xlabel("Matches", fontsize=14)
	ax.set_ylabel("KD", fontsize=14)
	ax.plot(elo_history)
	plt.savefig('graph.png')

	await message.channel.send(file=discord.File('graph.png'))
#just returns faceitid for testing
async def faceit_id(message):
	nickn = message.content.split(" ", 1)
	name = nickn[1]
	get_player_details = faceit_data.player_details(name, 'csgo')
	get_player_id = get_player_details['player_id']
	await message.channel.send(get_player_id)

#joke command to compare KD from api request to float and returns compliments/snide remarks
async def am_i_cracked(message):
	nickn = message.content.split(" ", 1)
	name = nickn[1]
	REE = faceit_data.player_details(name, 'csgo')
	get_player_id = REE['player_id']
	statistics = faceit_data.player_stats(get_player_id, 'csgo')
	kill_death = statistics['lifetime']['Average K/D Ratio']
	bad_kd = ['You really should DM', 'Please load a map and click on bots', 'Try !trash instead']
	good_kd = ['there is a high chance you actually deathmatched', 'Some may say you click on heads']
	insane_kd = ['This is probably what 500 hours on practice looks like']
	if float(kill_death) < 1.3:
		await message.channel.send(bad_kd[random.randint(0,4)])
	elif float(kill_death) < 1.7: 
		await message.channel.send(good_kd[random.randint(0,2)])
	else:
		await message.channel.send(insane_kd[random.randint(0,2)])
	
####################################################################################
#uses IMGUR Api to find an image from a subreddit gallery in reddit, in this case "aww"
async def aww(message):
	imgr = ImgurClient(IMGUR_ID, IMGUR_SECRET)
	cmd = message.content.split(" ", 1)
	searche2 = imgr.subreddit_gallery('aww')
	i = random.randint(0,len(searche2)-1)
	await message.channel.send(searche2[i].link)

#returns image query from imgur 
async def imgurCommand(message):
	imgr = ImgurClient(IMGUR_ID, IMGUR_SECRET)
	cmd = message.content.split(" ", 1)
	if len(cmd) <= 1:
		items = imgr.gallery(section='user', sort='time', page=1, window='day', show_viral=False)
	else:
		items = imgr.gallery_search(cmd[1], advanced=None, sort='time', window='all', page=0)
	if len(items) < 1:
		await message.channel.send("No reults")
	i = random.randint(0,len(items)-1) # Added -1 to prevent list index out of range exceptions
	await message.channel.send(items[i].link)
# creates a "let me google that for you" link
async def lmgtfy(message):
	lmgtfys = message.content[8:]
	searchstr = lmgtfys.replace(" ", "+")
	await message.channel.send('http://lmgtfy.com/?q='+searchstr)
####################################################################################
#for testing
async def testinput(message):
	filtr = message.content.split(" ", 1)
	inputtedtext = filtr[1]
	alphaonly = list(filter(str.isalpha, inputtedtext))
	await message.channel.send(alphaonly)
#kills bot
async def killCommand(message):
	if str(message.author.id) in MASTERS:
		await message.channel.send("goodbye cruel world")
		exit()
	else:
		await message.channel.send("kys")
#joke command for counterstrike 
async def trash(message):
	reasons = ["the lag", "you're not trying" ,"you only had like 2 hours of sleep", 
    "your cat is on your keyboard", "you're too greasy", "of brain lag", "you were looking at chat", 
	"you got cookie dust on your mousepad", 
	"it's too hot", "you swallowed your GUM", "of your itchy arm",  "there's cat hair on your mousepad",
	"your hair got in your eyes", "crumbs on your mousepad from PB&J", "you are hungry"]
	trashplayer = '{0.author.mention}'.format(message)
	await message.channel.send(trashplayer + ', you are trash because ' + reasons[(random.randint(0,24))])

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	await client.change_presence(status=discord.Status.idle, activity=discord.Game("Videogame bot is playing"))

client.run(TOKEN)