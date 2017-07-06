import asyncio
import discord
import aiohttp
import json
import time
from textblob import TextBlob
import sys
import os
import random

tokens = {}
with open("/root/Bots/SweetieBot/SweetieBot/token.json",'r') as fp:
    tokens = json.load(fp)

token = tokens['token']

class SweetieBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.GamePlaying = discord.Game()
        self.GamePlaying.name = "@mention me!"
        self.ownid = tokens['ownid']
        self.ownerid = tokens['ownerid']
        self.isowner = False
        self.commandlist = ["blob","spellcheck", "translate","woof","meow","youtube","wiki","commands","me_irl"]
        self.responselist = [":3",">:]","*boop*","zzz",";3","<3",":P",":D",":v","^w^","!!","me_irl","-w-","o.o","https://derpicdn.net/img/view/2012/1/31/2708__safe_animated_sweetie+belle_wat_scrunchy+face_what+has+science+done_dumb+running+ponies_caterpillar_centipede_artist-colon-3dapple.gif"]
        self.requestssession = aiohttp.ClientSession()
        self.googlekey = tokens['youtube']

    async def on_ready(self):
    	await self.change_presence(game = self.GamePlaying)

    async def on_message(self, message):
    	if message.author.id == self.ownid:
    		return
    	if self.user.mentioned_in(message):
    		userinput = message.content
    		inputlist = userinput.split(' ',2)
    		command = inputlist[1].lower()
    		args = []
    		if len(inputlist)>2:
    			arglist = inputlist[2]
    			if "|" in arglist:
    				arglist = arglist.split("|")
    			else:
    				arglist = [arglist]

    			args = args + arglist
    		if message.author.id == self.ownerid:
    			self.isowner = True
    		else:
    			self.isowner = False
    		if (self.isowner == True) or (command in self.commandlist):
    			if hasattr(self, command):
    				method = getattr(self, command)
    				attributenumber = method.__code__.co_argcount
    				attributeslist = method.__code__.co_varnames
    				report = "arguments:\nHas {} required argument(s).\n{}".format(attributenumber,attributeslist)
    				try:
    					response = await method(*args)
    				except:
    					response = report
    				await self.send_message(message.channel, response)
    		return
    	if ("sweetiebot" in message.content.lower()) or ("SB" in message.content):
            choice = random.choice(self.responselist)
            if choice == "me_irl":
                choice = await self.me_irl()
            await self.send_message(message.channel, choice)
    		return
    	#if random.randint(1,70) == 70:
    	#	choice = random.choice(self.responselist)
    	#	if choice == "me_irl":
    	#		choice = await self.me_irl()
    	#	await self.send_message(message.channel, choice)

    async def blob(self, text):
        thetext = TextBlob(text)
        sentences = thetext.sentences
        language = thetext.detect_language()
        report = "Language: {}\n{} sentence(s):\n".format(language,len(sentences))
        for s in sentences:
            sentiment = s.sentiment
            report = report + "{}\n-- {}\n".format(s,sentiment)
        return(report)

    async def spellcheck(self, text):
    	thetext = TextBlob(text)
    	corrected = thetext.correct()
    	return(corrected)

    async def translate(self, language, text):
    	b = TextBlob(text)
    	translated = b.translate(to=language)
    	return(translated)

    async def woof(self):
    	wuf = """
    	▄▀▄▀▀▀▀▄▀▄░░░░░░░░░
░█░░░░░░░░▀▄░░░░░░▄░
█░░▀░░▀░░░░░▀▄▄░░█░█
█░▄░█▀░▄░░░░░░░▀▀░░█
█░░▀▀▀▀░░░░░░░░░░░░█
█░░░░░░░░░░░░░░░░░░█
█░░░░░░░░░░░░░░░░░░█
░█░░▄▄░░▄▄▄▄░░▄▄░░█░
░█░▄▀█░▄▀░░█░▄▀█░▄▀░
░░▀░░░▀░░░░░▀░░░▀░░░
    	"""
    	return(wuf)

    async def restart(self):
    	print("restarting")
    	os.execv(sys.executable, ['python3'] + sys.argv)
    	return("restarted!")

    async def change_status(self,gamename):
    	self.GamePlaying.name = gamename
    	await self.change_presence(game = self.GamePlaying)
    	return("Updated Status!")

    async def fetchurl(self, url):
    	async with self.requestssession.get(url) as r:
    		return(r)

    async def fetchjson(self, url):
    	async with self.requestssession.get(url) as r:
    		resp = await r.json()
    		return(resp)

    async def meow(self):
    	res = await self.fetchjson('http://random.cat/meow')
    	cat = res['file']
    	return(cat)

    async def youtube(self, query, number=1):
    	query = query.replace(" ","+")
    	url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&q={}&maxResults={}&key={}&type=video'.format(query,number,self.googlekey)
    	res = await self.fetchjson(url)
    	videos = res['items']
    	result = "The top {} result(s):\n".format(number)
    	for x in videos:
    		result += "https://www.youtube.com/watch?v="+x['id']['videoId']+"\n"
    	return(result)

    async def wiki(self, query, number=1):
    	query = query.replace(" ","%20")
    	url = "https://en.wikipedia.org/w/api.php?action=opensearch&search={}&limit={}&format=json".format(query,number)
    	res = await self.fetchjson(url)
    	links = res[3]
    	result = "The top {} result(s)\n".format(number)
    	for x in links:
    		result += x+"\n"
    	return(result)

    async def me_irl(self):
    	url = "http://www.reddit.com/r/me_irl/random/.json"
    	res = await self.fetchjson(url)
    	me2thanks = res[0]['data']['children'][0]['data']['url']
    	return(me2thanks)

    async def commands(self):
    	response = "here is my command list :3\n" + str(self.commandlist)+"\nexample:\n`@sweetiebot command argument1|argument2|argument3`"
    	return(response)

bot = SweetieBot()
bot.run(token)