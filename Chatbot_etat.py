#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import sys, logging, requests, time, math

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO) # Dans l'exercice des TPG c'est level=logging.DEBUG

logger = logging.getLogger(__name__)

CHOIX, RESTAURANTS,RETOUR_SORTIR, RESTAURANT_DETAILS, SORTIES,  LIEU, COORDONNEES, DETAILS, RETOUR_RESTAURANTS = range(9)

#==========================CODE RESTAURANT CHATBOT==================================#

#=========LES FONCTIONS DES RESAUARNTS=====#

# ====MESSAGE  DE BIEN VENU DE DEBUT DE CHATBOT===#
def start(bot, update):
    reply_keyboard = [['Sorties', 'Restaurants']]
    update.message.reply_text(
        'Bonjour {}, je suis bot guide. Je t\' aide à trouver des  restaurants à Genève. \n\n'
        'Tu peux écrire "/quitter  "pour arrêter la conversation .\n\n'
        'Sur quel sujet je peux je t\' aider  ?\n\n'.format(update.message.from_user.first_name),
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return CHOIX

#====AFFICHE LES 5 RESTAURNATS===#
def choix_des_restaurants(bot, update):
    reply_keyboard_restaurant= [
        ['Indien', 'Japonais', 'Chinois'],
        ['Maroccain', ' Francais'],
        ['Retour au menu principal']
    ]
    update.message.reply_text(
        '   Que veux- tu manger?',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard_restaurant,
            one_time_keyboard=True
        )
    )

    return RESTAURANTS

#====AFFICHE LES DIFFERENT SORTIES===#
def choix_de_sorties(bot, update):
    reply_keyboard_sorties = [
        ['Bars','Clubs','Musées'],
        ['Retour au menu principal']
    ]
    update.message.reply_text(
        'Quels genres de sorties pourraient te plaire?',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard_sorties,
            one_time_keyboard=True
        )
    )

    return SORTIES

#====AFFICHE LES RESTAURAINS SELON LES CUISINS CHOISI===#
def affiche_les_resultats(bot, update):
    reply_keyboard_liste_restaurant = [
        ['RAJPOUTE','Café des Amis','Mikado Sushi'],
        ['le Raisin d\'Or','Baroush'],
        ['Nouvelle recherche']
    ]
    update.message.reply_text(
        'Voici la listes des restaurants: \n\n',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard_liste_restaurant,
            one_time_keyboard=True
        )
    )

    return RESTAURANT_DETAILS


#====AFFICHE LES DETAILS DES RETAURNATS CHOISI===#
def affiche_les_details(bot, update):
    reply_keyboard_retour_restaurant = [
        [' Voir d\'autres restaurants']
    ]
    update.message.reply_text(
        'Nom: {} \n\n'
        'Note: 4,9 sur 5 étoiles\n'
        'Prix moyen: 25 - 35 CHF \n'
        'Horaire d\'aujourd\'hui: 12:00 - 00:00\n'
        'Adresse : rue de Carouge 77\n'.format(update.message.text),
    )
    update.message.reply_location(46.1899234, 6.1435749,
    reply_markup = ReplyKeyboardMarkup(
        reply_keyboard_retour_restaurant,
        one_time_keyboard=True
    )
    )

    return RETOUR_RESTAURANTS


#====AFFICHE LES 3 TOP MUSEES===#
def affiche_liste_musees(bot, update):
    update.message.reply_text(
        '1)Musée de Carouge \n\n'
        'Adresse: place de Sardaigne 2,1227 Carouge GE\n'
        'Horaire d\'aujourd\'hui: 14:00 - 18:00\n'
        'Prix: Gratuit\n '
    )
    update.message.reply_text(
        '2) Musée d\'histoire naturelle\n'
        'Adresse: route de Malagnou 1,1211 Genève \n'
        'Horaire d\'aujourd\'hui: 11:00 - 18:00\n'
        'Prix: Gratuit\n '
    )
    reply_keyboard_retour = [
        ['Retour']
    ]
    update.message.reply_text(
        '3) ICT Discovery\n\n'
        'Adresse: rue de Varembé 2,1202 Genève\n'
        'Horaire d\'aujourd\'hui: 10:00 - 17:00\n'
        'Prix: Gratuit\n ',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard_retour,
            one_time_keyboard=True
        )
    )
    return RETOUR_SORTIR

#====AFFICHE LES 3 TOP BARS===#
def affiche_liste_bars(bot, update):
    update.message.reply_text(
        '1) KAMPAI \n\n'
        'Adresse: rue de Monthoux 25,1201 Genève\n'
        'Horaire d\'aujourd\'hui: 11:00 - 00:00\n'
        'Prix moyen: 25 CHF\n ',
    )
    update.message.reply_text(
        '2) La Salle \n\n'
        'Adresse: boulevard du Pont-d\'Arve 28,1205 Genève\n'
        'Horaire d\'aujourd\'hui: 17:00 - 01:00\n'
        'Prix moyen: 15 CHF\n ',
    )
    reply_keyboard_retour = [
        ['Retour']
    ]
    update.message.reply_text(
        '3) Qu\'importe Bar \n\n'
        'Adresse:rue Ancienne 1,1227 Carouge GE\n'
        'Horaire d\'aujourd\'hui: 17:00 - 02:00\n'
        'Prix moyen: 15 CHF\n',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard_retour,
            one_time_keyboard=True
        )
    )
    return RETOUR_SORTIR

#====AFFICHE LES 3 TOP CLUBS===#
def affiche_liste_clubs(bot, update):
    update.message.reply_text(
        '1) Java Club\n\n'
        'Adresse :Quai du Mont-Blanc 19, 1201 Genève\n'
        'Horaire d\'aujourd\'hui: 23:00 - 5:00\n'
        'Prix d\'entrée : 50 CHF')
    update.message.reply_text(
        '2) The Baroque Club\n\n'
        'Adresse :Place de la Fusterie 12, 1204 Genève\n'
        'Horaire d\'aujourd\'hui: 00:00 - 04:00\n'
        'Prix d\'entrée : 40 CHF')
    reply_keyboard_retour = [
        ['Retour']
    ]
    update.message.reply_text(
        '3) Point Bar Club\n\n'
        'Adresse :rue du Marché 3Bis,1204 Genève\n'
        'Horaire d\'aujourd\'hui: 22:00 - 05:30\n'
        'Prix d\'entrée : 50 CHF',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard_retour,
            one_time_keyboard=True
        )
    )

    return RETOUR_SORTIR

# ====FIN DU PROGRAMME===#
def quitter(bot, update):
    update.message.reply_text(' Ravie de pouvoir t\'aider  Merci et à bientôt!',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

#==========================CODE TRANSPORT CHATBOT==================================#
#=========LES FONCTIONS DES TRANSPORT=====#
#Récupèration des données sur Opendata
def appeler_opendata(path):
    url = "http://transport.opendata.ch/v1/" + path
    reponse = requests.get(url)
    return reponse.json()

#====INDICATION DE TEMPS RETANT===#
def calcul_temps_depart(timestamp):
    seconds = timestamp-time.time()
    minutes = math.floor(seconds/60)
    if minutes < 1:
        return "dépèche toi!!!!"
    if minutes > 60:
        return "> {} h.".format(math.floor(minutes/60))
    return "dans {} min.".format(minutes)


#====PREPARATION DES MESSAGES===#

#====RENVOIS LES RESULTATS DES STATION AUTOUR===#
def afficher_arrets(update, arrets):
    texte_de_reponse = "Voici les arrêts:\n"
    for station in arrets['stations']:
        if station['id'] is not None:
            texte_de_reponse += "\n/a" + station['id'] + " " + station['name']
    update.message.reply_text(texte_de_reponse)

#====DETAILS DES STATIONS===#
def afficher_departs(update, departs):
    texte_de_reponse = "Voici les prochains départs:\n\n"
    for depart in departs['stationboard']:
        texte_de_reponse += "{} {} dest. {} - {}\n".format(
            depart['category'],
            depart['number'],
            depart['to'],
            calcul_temps_depart(depart['stop']['departureTimestamp'])
        )
    texte_de_reponse += "\nAfficher a nouveau: /a" + departs['station']['id']

    coordinate = departs['station']['coordinate']
    update.message.reply_location(coordinate['x'], coordinate['y'])
    update.message.reply_text(texte_de_reponse)


#====REPONSES=====##
#====MESSAGE D'AQUEIL===#
def bienvenu(bot, update):
    update.message.reply_text("Bonjour {}, je suis là pour te donner les information sur les TPG.\n"
                              "Merci d'envoyer ta localisation "
                              .format(update.message.from_user.first_name))
    return LIEU

#====AFFICHE LES ARRETES QUI SONT AUTOUR===#
def lieu_a_chercher(bot, update):
    resultats_opendata = appeler_opendata("locations?query=" + update.message.text)
    afficher_arrets(update, resultats_opendata)

    return COORDONNEES

#====RECHERCHE PAR LOCATION===#
def coordonnees_a_traiter(bot, update):
    location = update.message.location
    resultats_opendata = appeler_opendata("locations?x={}&y={}".format(location.latitude, location.longitude))
    afficher_arrets(update, resultats_opendata)

    return DETAILS


def details_arret(bot, update):
    arret_id = update.message.text[2:]
    afficher_departs(update, appeler_opendata("stationboard?id=" + arret_id))


#=========LA FONCTION MAIN RRESTAURNT=====#
def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(sys.argv[1])
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO

#==LES FONCTIONSRRESTAURNT==#
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],#LA PERSONNE DOIT ECRIRE "/start"

        states={
            CHOIX: [
                RegexHandler('Sorties',  choix_de_sorties),
                RegexHandler('Restaurants', choix_des_restaurants),
                # PERMET à LA PERSONNE DE QUITTER à N'IMPORT QUEL MOMENTS EN ECRIVANT "/quitter"
                CommandHandler('quitter', quitter),
                # QUELQUE SOIT LE MOTS ECRIT IL VA DERIGER VERS -> start
                RegexHandler('', start)
            ],

            RESTAURANTS: [
                RegexHandler('Indien', affiche_les_resultats),
                RegexHandler('Japonais', affiche_les_resultats),
                RegexHandler('Chinois', affiche_les_resultats),
                RegexHandler('Maroccain', affiche_les_resultats),
                RegexHandler('Francais', affiche_les_resultats),
                RegexHandler('Retour au menu principal', start),
                # PERMET à LA PERSONNE DE QUITTER à N'IMPORT QUEL MOMENTS EN ECRIVANT "/quitter"
                CommandHandler('quitter', quitter),
                # QUELQUE SOIT LE MOTS ECRIT IL VA DERIGER VERS -> choix_des_restaurants
                RegexHandler('', choix_des_restaurants)
            ],

            SORTIES: [
                RegexHandler('Musées',  affiche_liste_musees),
                RegexHandler('Bars', affiche_liste_bars),
                RegexHandler('Clubs',  affiche_liste_clubs),
                RegexHandler('Retour au menu principal', start),
                # PERMET à LA PERSONNE DE QUITTER à N'IMPORT QUEL MOMENTS EN ECRIVANT "/quitter"
                CommandHandler('quitter', quitter),
                # QUELQUE SOIT LE MOTS ECRIT IL VA DERIGER VERS -> choix_de_sorties
                RegexHandler('',choix_de_sorties)
            ],

            RETOUR_SORTIR: [
                RegexHandler('Retour', choix_de_sorties),
                # PERMET à LA PERSONNE DE QUITTER à N'IMPORT QUEL MOMENTS EN ECRIVANT "/quitter"
                CommandHandler('quitter', quitter),
                # QUELQUE SOIT LE MOTS ECRIT IL VA DERIGER VERS -> choix_de_sorties
                RegexHandler('', choix_de_sorties)

            ],

            RESTAURANT_DETAILS: [
                RegexHandler('RAJPOUTE',  affiche_les_details),
                RegexHandler('Mikado Sushi',  affiche_les_details),
                RegexHandler('le Raisin d\'Or',  affiche_les_details),
                RegexHandler('Baroush',  affiche_les_details),
                RegexHandler('Café des Amis',  affiche_les_details),
                RegexHandler('Nouvelle recherche', choix_des_restaurants),
                # PERMET à LA PERSONNE DE QUITTER à N'IMPORT QUEL MOMENTS EN ECRIVANT "/quitter"
                CommandHandler('quitter', quitter),
                # QUELQUE SOIT LE MOTS ECRIT IL VA DERIGER VERS -> affiche_les_resultats
                RegexHandler('', affiche_les_resultats)
            ],

            RETOUR_RESTAURANTS: [
                RegexHandler('Autres restaurants', affiche_les_resultats),
                # PERMET à LA PERSONNE DE QUITTER à N'IMPORT QUEL MOMENTS EN ECRIVANT "/quitter"
                CommandHandler('quitter', quitter),
                # QUELQUE SOIT LE MOTS ECRIT IL VA DERIGER VERS -> affiche_les_resultats
                RegexHandler('', affiche_les_resultats)

            ]
        },

        fallbacks=[]
    )

##======LA FONCTION MAIN TRANSPORT=====#
    conv_handler_transport = ConversationHandler(
        entry_points = [CommandHandler('transport', bienvenu)],

        states={
            LIEU: [MessageHandler(Filters.text, lieu_a_chercher)],
            COORDONNEES: [MessageHandler(Filters.location, coordonnees_a_traiter)],
            DETAILS: [MessageHandler(Filters.command, details_arret)]
        },

        fallbacks=[CommandHandler('quitter', quitter)]#PERMET à LA PERSONNE DE QUITTER LORSQUE IL ECRIR /quitter
    )

    dp.add_handler(conv_handler)
    dp.add_handler(conv_handler_transport)
    # Start the Bot
    updater.start_polling(timeout=2)
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
