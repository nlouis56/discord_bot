from os import link
from discord import Embed

help_message = Embed(title="L'aide de zeubi", description="vraiment joli ce truc")
help_message.add_field(name="Commandes :", value="\n>spam <quantité> <mot> \n> spamme <mot> <quantité> fois\n\n\
    >test \n> test du système de permissions et divers\n\n\
    >invite \n> afficher le lien d'invitation du bot dans le salon\n\n\
    >git \n> afficher le lien du repo GitHub de zeubi\n\n\
    >say <channel id> <message> \n> le bot dira <message> dans le channel correspondant à <channel id>\n\n\
    >infosys \n> donne les informations actuelles du serveur\n\n\
    >man_bash \n> affichage de la page 'man bash' (15k lignes)\n\n\
    >dump \n> affichage du message sans les embeds ou mises en forme quelconques\n\n")
help_message.add_field(name="Chatroom :", value=">addchannel \n> ajout du salon actuel dans le système de chatroom globale\n\n\
    >rmchannel \n> retrait du salon actuel du système de chatroom globale\n\n\
    >list_servers \n> liste les serveurs dans lesquels le bot est présent")
help_message.add_field(name="Perms Zone :", value=">killbot\n>reload_assets")
help_message.set_footer(text="et puis voilà hein faut pas trop en demander non plus")

permissions_error = Embed(title="Erreur !", description="", color=0xFC0303)
permissions_error.add_field(name="T'as pas les perms", value="Erreur de permissions, tu ne peux pas éxecuter cette commande")
permissions_error.set_footer(text="cheh mdr")

git_repo = Embed(title="zeubi_bot sur GitHub", link="https://github.com/nlouis56/zeubi_bot", description="https://github.com/nlouis56/zeubi_bot")

warning_stop_bot = Embed(title="Arrêt du bot !", description="Les chatrooms et autres commandes reviennent vite :)", color=0xFC0303)