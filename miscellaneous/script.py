# -*- coding: utf-8 -*-

from fuzzywuzzy import fuzz

taux = 1

identiteResponsableTraitement = ["responsable", "traitement", "adresse", "nom", "denomination", "sociale", "adresse",
                                 "géographique", "siège", "social", "numéro", "téléphone", "postale", "electronique",
                                 "mail"]
identiteResponsableTraitementText = "Des commentaires ou des questions au sujet de la présente Politique de confidentialité ? Merci de nous en faire part en nous contactant ici ou en nous écrivant à l'adresse correspondante ci-dessous. Si vous habitez aux Ãtats-Unis, le responsable du traitement des données pour vos données à caractère personnel est Twitter, Inc., dont l'adresse est : Twitter, Inc. Attn : Privacy Policy Inquiry 1355 Market Street, Suite 900 San Francisco, CA 94103 Si vous habitez en dehors des Ãtats-Unis, le responsable du traitement des données est Twitter International Company, dont l'adresse est : Twitter International Company Attn : Data Protection Officer One Cumberland Place, Fenian Street Dublin 2, D02 AX07 IRLANDE Si vous habitez dans l'Union européenne ou dans les Ãtats de l'AELE, vous pouvez contacter le délégué à la protection des données de Twitter en toute confidentialité ici. Si vous souhaitez signaler un problème lié à notre utilisation de vos informations (et sans porter atteinte à tous autres droits dont vous pouvez disposer), vous avez le droit de vous adresser à votre autorité de supervision locale ou à l'autorité de supervision de Twitter International Company, à savoir l'Irish Data Protection Commission. Vous trouverez ses coordonnées ici."

precisionSurObjetDeCollecte = []

mentionDeLaFinalite = ["Traitement", "commandes", "Amélioration", "service", "Personnalisation", "service",
                       "Proposition", "offres", "Amélioration", "ciblage", "publicitaire", "A des fins d'études",
                       "fins", "fourniture", "responsable", "traitement", "vue", "valoriser"]
mentionDeLaFinaliteText = " Nous recevons des informations lorsque vous visionnez un contenu ou que vous interagissez autrement avec nos services, même si vous n'avez pas créé de compte ( Données de journal ). Par exemple, lorsque vous visitez nos sites Web, que vous vous authentifiez sur nos services, que vous interagissez avec nos notifications par email, que vous utilisez votre compte pour vous authentifier sur un service tiers, ou que vous visitez un service tiers comprenant un contenu Twitter, nous sommes susceptibles de recevoir des informations à votre sujet. Ces Données de journal sont par exemple votre adresse IP, le type de votre navigateur, votre système d'exploitation, la page Web d'oÃ¹ vous venez, les pages visitées, votre emplacement, votre opérateur téléphonique, des informations relatives à votre appareil (notamment les identifiants de l'appareil et de l'application), des termes de la recherche ou des informations de cookies. Nous recevons également des Données de journal lorsque vous cliquez, visualisez ou interagissez avec des liens sur nos services, y compris lorsque vous installez d'autres applications via Twitter. Nous utilisons les Données de journal pour exploiter nos services et assurer leur fonctionnement sécurisé, fiable et robuste. Par exemple, nous utilisons les Données de journal pour protéger la sécurité des comptes et pour déterminer quel contenu est populaire sur nos services. Nous utilisons également ces données pour améliorer le contenu que nous vous présentons, y compris les publicités. Nous utilisons les informations que vous nous fournissez et les données que nous recevons, telles que les Données de journal et des données provenant de tiers, pour déduire les thèmes qui peuvent vous intéresser, votre Ã¢ge et les langues que vous parlez. Cela nous aide à vous proposer des services pertinents et à personnaliser le contenu que nous vous présentons, y compris les publicités."


def checkText(textToAnalyse, wordsWhichMustBeIn):
    i = 0

    print(textToAnalyse)
    print
    print(wordsWhichMustBeIn)
    for f in identiteResponsableTraitement:
        if f in identiteResponsableTraitementText:
            print("Le text parle de " + f)
            i += 1
    print("il y a i = " + str(i) + " matchs")

    if (i == (len(identiteResponsableTraitement) - taux)):
        print("le text contiens un nombre acceptable de mots les mots")


# fonction pour trouver l'adresse du responsable de traitement
def checkResponsableTraitement(textToAnalyse):
    s = ""
    toFind = "responsable"

    indexToFind = textToAnalyse.find(toFind)

    textWhoMustContainTraitement = textToAnalyse[indexToFind:indexToFind + 25]

    print(fuzz.partial_ratio(textWhoMustContainTraitement, "responsable de traitement"))
    while (fuzz.partial_ratio(textWhoMustContainTraitement, "responsable de traitement") < 90):
        #textWhoMustContainTraitement = textWhoMustContainTraitement[indexToFind:]
        indexToFind = textToAnalyse.find(toFind)
        textWhoMustContainTraitement = textToAnalyse[indexToFind:indexToFind + 25]

    # gérer si le text n'existe pas

    # changer pour un switch avec les différentes formulations possible
    # a terme changer par vecteurs de mots
    if (fuzz.partial_ratio(textWhoMustContainTraitement, "adresse :") > fuzz.partial_ratio(textWhoMustContainTraitement, "adresse est")):
        toFind = "adresse :"
        indexToFind = textToAnalyse.find(toFind)
    else:
        toFind = "adresse est "
        indexToFind = textToAnalyse.find(toFind)

    textAdressContent = textToAnalyse[indexToFind + len(toFind):indexToFind + 200]

    alphabet = "azertyuiopqsdfghjklmwxcvbn"

    index = 0

    for s in textAdressContent:
        if (s in alphabet):
            break
        else:
            index += 1

    textAdressContent = textAdressContent[index - 1:index + 97]

    return textAdressContent


def putTextInform(textToAnalyse, wordsWhichMustBeIn):
    textToAnalyse.lower()
    for f in wordsWhichMustBeIn:
        f.lower()

    textToAnalyse.split(" ")
    textToAnalyse.split("'")

    checkText(textToAnalyse, wordsWhichMustBeIn)


# fonction à apeller depuis l'api
def takeFormText(textOfTheForm):
    textResult = checkResponsableTraitement(textOfTheForm)

    return textResult


# tests

def final(s):
    if (s=="Facebook"):
        f = open('facebook.txt', encoding="utf8")
        text = f.read()
        f.read()
        f.close()
        return takeFormText(text)


takeFormText(identiteResponsableTraitementText)
print(final("Facebook"))
