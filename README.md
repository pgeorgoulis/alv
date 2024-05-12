## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Usage](#usage)
* [License](#license)

## General info
Alv is a discord bot made with the library discord.py. It's main functionality is reading one or more dates on wich each discord member is available and then using that input to calculate all the possible common available time periods and dates. The bot also has some general use and administrative functions such as making polls, posting memes, deleting user messages and keeping usage related logs.  
	
## Technologies
Project is created with:
* Python 3.10.6
* Discord.py version: 2.1.0
* asyncpraw version: 7.7.0

## Setup
Just like any other discord bot, install the needed libraries and run the main file with:
$./alv.py

For this bot to run, your discord and your asyncpraw (Reddit) token are required.

## Usage
While the main purpose of the bot is scheduling meetings and finding common meeting times between the discord server members it also has some admin and utility funcionalities all of wich are explained with the help command. All the commands available are discord slash commands and as a secondary functionality the bot can: 
* show, remove and provide statistics about the entered dates
* create and show logs of the commands to the administrator of the discord server
* restart a cog (available only to the server admin)
* create polls
* send memes
and much more! 
	
## License
MIT License
