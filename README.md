# zeubi_bot (a slightly violent discord bot)   
![Python](https://img.shields.io/badge/Python-3670A0?style=flat-square&logo=python&logoColor=ffdd54)   
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue?style=flat-square&logo=license-gplv3)](https://choosealicense.com/licenses/gpl-3.0/)   
   
zeubi now speaks english and french, language packs are here ! (i'll introduce more languages asap)   

He really dislikes getting pings from people, he'll probably stard insulting the sender of the message   

zeubi can link your server to a whole network of other servers through his "chatroom" functionality !
I strongly recommend the creation of a new channel for this.
Every message you send in the channel will be transmitted to all the other servers present on the "network" with a registered channel, you will then receive and be able to interact with their responses.   

#
## Useful commands (accessible by everyone)

> \>spam \<quantity> \<text>   
Used to spam text a certain amount in the current channel

> \>test   
Used to test the permission system

> \>invite   
Showing the invite link of the bot in the chat

> \>say \<channel id> \<text>   
Says the text in the channel   

> \>infosys   
Gives information on the system on which the bot is running

> \>man_bash   
Drops the man page of BASH (approx. 15k lines of obscure linux things)

> \>dump \<text>   
Shows the litteral text, without embedding emotes, gifs, or user tags

#
## Chatroom commands   

> \>addchannel   
Adds the current channel to the "global chatroom"   

> \>rmchannel   
Removes the current channel of the "global chatroom"

#
## Superuser commands

to access these, you just have to put your userid (or the userid of anyone you wish to make a superuser) in the "superusers" list of the settings.json file   


> \>killbot   
Kills the bot (duh)   

> \>startup   
Sends a message in all the chatrooms mentionning that the bot is back online

> \>reload_assets   
Hot-reload of the ping responses, automatic reactions, and everything in the json file. This command is used for minor changes with no downtime

#
### Various infos   

zeubi is still in developement, i'm trying to publish frequent updates to the code as i fix or add stuff. Feel free to contact me for any info/requests, i'm open for partnerships and such.   

License : [GPL v3](https://choosealicense.com/licenses/gpl-3.0/)