from os import link
from discord import Embed

help_fr = Embed(title="L'aide de zeubi", description="vraiment joli ce truc")
help_fr.add_field(name="Commandes :", value="\n>spam <quantité> <mot> \n> spamme <mot> <quantité> fois\n\n\
    >test \n> test du système de permissions et divers\n\n\
    >invite \n> afficher le lien d'invitation du bot dans le salon\n\n\
    >git \n> afficher le lien du repo GitHub de zeubi\n\n\
    >say <channel id> <message> \n> le bot dira <message> dans le channel correspondant à <channel id>\n\n\
    >infosys \n> donne les informations actuelles du serveur\n\n\
    >man_bash \n> affichage de la page 'man bash' (15k lignes)\n\n\
    >dump \n> affichage du message sans les embeds ou mises en forme quelconques\n\n\
    >decompose <message id> \n> si <message id> désigne un embed, le bot va décomposer et afficher le code brut de l'embed\n\n\
    >ping \n> calcule et affiche le ping avec le serveur de discord\n\n")
help_fr.add_field(name="Chatroom :", value=">addchannel \n> ajout du salon actuel dans le système de chatroom globale\n\n\
    >rmchannel \n> retrait du salon actuel du système de chatroom globale\n\n\
    >list_servers \n> liste les serveurs dans lesquels le bot est présent")
help_fr.add_field(name="Perms Zone :", value=">killbot\n>reload_assets\n>startup", inline=False)
help_fr.set_footer(text="et puis voilà hein faut pas trop en demander non plus")

help_en = Embed(title="zeubi's Help", description="lookin' all nice")
help_en.add_field(name="Commands :", value="\n>spam <quantity> <text> \n> spams <text> <quantity> times\n\n\
    >test \n> used to test the permission system and random stuff sometimes\n\n\
    >invite \n> sends the bot's invite link\n\n\
    >git \n> sends the link to the bot's GitHub repo\n\n\
    >say <channel id> <message> \n> the bot will say <message> in the channel associated with <channel id> (bot must have access to channel)\n\n\
    >infosys \n> Gives the current system information of the hosting device\n\n\
    >man_bash \n> displays the 'man bash' page (15k lines)\n\n\
    >dump <message> \n> displays <message> without embedding any links or emotes\n\n\
    >decompose <message id> \n> if <message id> designates an embed, the bot will decompose and display the raw code of the embed\n\n\
    >ping \n> gets and displays the ping with discord.gg server\n\n")
help_en.add_field(name="Chatroom :", value=">addchannel \n> adds the current channel in the global chatroom system\n\n\
    >rmchannel \n> removes the current channel from the global chatroom system\n\n\
    >list_servers \n> lists the servers in which the bot is present")
help_en.add_field(name="Perms Zone :", value=">killbot\n>reload_assets\n>startup", inline=False)
help_en.set_footer(text="and yeah that's basically it")

help_message = {"fr": help_fr, "en": help_en}



perm_error_fr = Embed(title="Erreur !", description="", color=0xFC0303)
perm_error_fr.add_field(name="T'as pas les perms", value="Erreur de permissions, tu ne peux pas éxecuter cette commande")
perm_error_fr.set_footer(text="cheh mdr")

perm_error_en = Embed(title="Error !", description="", color=0xFC0303)
perm_error_en.add_field(name="You don't have the permissions", value="Permissions error, you can't execute this command")
perm_error_en.set_footer(text="oopsies")

permissions_error = {"fr": perm_error_fr, "en": perm_error_en}



git_repo = Embed(title="zeubi_bot on GitHub", link="https://github.com/nlouis56/zeubi_bot", description="https://github.com/nlouis56/zeubi_bot")



stop_bot_fr = Embed(title="Arrêt du bot !", description="Les chatrooms et autres commandes reviennent vite :)", color=0xFC0303)

stop_bot_en = Embed(title="Stopping the bot !", description="The chatrooms and other commands are coming back soon ! :)", color=0xFC0303)

stopping_message = {"fr": stop_bot_fr, "en": stop_bot_en}



startup_fr = Embed(title="zeubi est de retour !", description="Le serveur a redémarré sans encombre", color=0x2BC442)

startup_en = Embed(title="zeubi is back !", description="The server restarted properly", color=0x2BC442)

startup_message = {"fr": startup_fr, "en": startup_en}


def make_embed(title, description, color=0x000000) :
    em = Embed(title=title, description=description, color=color)
    return(em)