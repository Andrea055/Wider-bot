import discord
from discord.ext import commands
from discord.ext.commands import bot
import asyncio
import datetime as dt
import uuid
import requests
import shutil
from requests import Response
from PIL import Image
import time
import os
import sys
response = requests.post(
    'https://api.remove.bg/v1.0/removebg',
    files={'image_file': open('bg.png', 'rb')},
    data={'size': 'auto'},
    headers={'X-Api-Key': 'API'},
)
image_types = ["png", "jpeg", "gif", "jpg"]
wpercent= 40
basewidth = 180
hsize = 50
client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print("Bot is ready")


@client.command()
async def wide(ctx):
    # USAGE: use command .save in the comment box when uploading an image to save the image as a jpg
    try:
        url = ctx.message.attachments[0].url            # check for an image, call exception if none found
    except IndexError:
        print("Error: No attachments")
        await ctx.send("No attachments detected!")
    else:
        if url[0:26] == "https://cdn.discordapp.com":   # look to see if url is from discord
            r = requests.get(url, stream=True)
            imageName = 'fullsized_image' + '.png'     
            with open(imageName, 'wb') as out_file:
                print('Saving image: ' + imageName)
                shutil.copyfileobj(r.raw, out_file)     # save image (goes to project directory)
                img = Image.open('fullsized_image.png')
                img = img.resize((460, 200), Image.ANTIALIAS)
                img.save('resized_image.png') # save image (goes to project directory)
                await ctx.send('Wide!', file=discord.File('resized_image.png'))


@client.command()
async def remove(ctx):
    try:
        url = ctx.message.attachments[0].url            # check for an image, call exception if none found
    except IndexError:
        print("Error: No attachments")
        await ctx.send("No attachments detected!")
    else:
        if url[0:26] == "https://cdn.discordapp.com":   # look to see if url is from discord
            r = requests.get(url, stream=True)
            imageName = 'bg' + '.png'     
            with open(imageName, 'wb') as out_file:
                print('Saving image: ' + imageName)
                shutil.copyfileobj(r.raw, out_file) # save image (goes to project directory)
                
                   

        response = requests.post(
    'https://api.remove.bg/v1.0/removebg',
    files={'image_file': open('bg.png', 'rb')},
    data={'size': 'auto'},
    headers={'X-Api-Key': 'API'},
)
    

    with open('no-bg.png', 'wb') as out:
        out.write(response.content)

    await ctx.send('No Backgroud!', file=discord.File('no-bg.png'))


client.run('API')
