import discord                 #import libraries
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
import cv2
import numpy as np
 
cap = cv2.VideoCapture('C:/New folder/video.avi')
 
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 5, (1280,720))
 
while True:
    ret, frame = cap.read()
    if ret == True:
        b = cv2.resize(frame,(1280,720),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
        out.write(b)
    else:
        break
    
cap.release()
out.release()
cv2.destroyAllWindows()
response = requests.post(                  #inizialize removebg api
    'https://api.remove.bg/v1.0/removebg',
    files={'image_file': open('bg.png', 'rb')},
    data={'size': 'auto'},
    headers={'X-Api-Key': 'API'},
)
image_types = ["png", "jpeg", "gif", "jpg"]       #setting up parameters for wide
wpercent= 40
basewidth = 180
hsize = 50

client = commands.Bot(command_prefix='.')    #define bot prefix

@client.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(bot.latency, 1)))
    
    
@client.event                 #message connect!
async def on_ready():
    print("Bot is ready")


@client.command()                                       # wide command and processing 
async def wide(ctx):

    try:
        url = ctx.message.attachments[0].url            # check for an image, call exception if none found
    except IndexError:
        print("Error: No attachments")
        await ctx.send("No attachments detected!")
    else:
        if url[0:26] == "https://cdn.discordapp.com":   # look to see if url is from discord
            r = requests.get(url, stream=True)
            imageName = 'fullsized_image' + '.png'      # save image to wide
            with open(imageName, 'wb') as out_file:
                print('Saving image: ' + imageName)
                shutil.copyfileobj(r.raw, out_file)     # save image from discord server
                img = Image.open('fullsized_image.png') 
                img = img.resize((460, 200), Image.ANTIALIAS)
                img.save('resized_image.png') # save image wide
                await ctx.send('Wide!', file=discord.File('resized_image.png'))


@client.command()
async def remove(ctx):                                  # define removebg command
    try:
        url = ctx.message.attachments[0].url            # check for an image, call exception if none found
    except IndexError:
        print("Error: No attachments")                  # check attachments presence
        await ctx.send("No attachments detected!")
    else:
        if url[0:26] == "https://cdn.discordapp.com":   # look to see if url is from discord
            r = requests.get(url, stream=True)
            imageName = 'bg' + '.png'                   # save bg image
            with open(imageName, 'wb') as out_file:
                print('Saving image: ' + imageName)
                shutil.copyfileobj(r.raw, out_file) # save image 
                
                   

        response = requests.post(                       # recall api for removebg
    'https://api.remove.bg/v1.0/removebg',
    files={'image_file': open('bg.png', 'rb')},
    data={'size': 'auto'},
    headers={'X-Api-Key': 'API'},
)
    

    with open('no-bg.png', 'wb') as out:
        out.write(response.content)

    await ctx.send('No Backgroud!', file=discord.File('no-bg.png'))     #send image without background in discord server


client.run('TOKEN')
