# -*- coding: utf-8 -*-

from fuzzywuzzy import fuzz

taux = 1

identiteResponsableTraitement = ["responsable", "traitement", "adresse", "nom", "denomination", "sociale", "adresse",
                                 "gÃ©ographique", "siÃ¨ge", "social", "numÃ©ro", "tÃ©lÃ©phone", "postale", "electronique",
                                 "mail"]
identiteResponsableTraitementText = "Des commentaires ou des questions au sujet de la prÃ©sente Politique de confidentialitÃ© ? Merci de nous en faire part en nous contactant ici ou en nous Ã©crivant Ã  lâadresse correspondante ci-dessous. Si vous habitez aux Ãtats-Unis, le responsable du traitement des donnÃ©es pour vos donnÃ©es Ã  caractÃ¨re personnel est Twitter, Inc., dont lâadresse est : Twitter, Inc. Attn : Privacy Policy Inquiry 1355 Market Street, Suite 900 San Francisco, CA 94103 Si vous habitez en dehors des Ãtats-Unis, le responsable du traitement des donnÃ©es est Twitter International Company, dont lâadresse est : Twitter International Company Attn : Data Protection Officer One Cumberland Place, Fenian Street Dublin 2, D02 AX07 IRLANDE Si vous habitez dans lâUnion europÃ©enne ou dans les Ãtats de lâAELE, vous pouvez contacter le dÃ©lÃ©guÃ© Ã  la protection des donnÃ©es de Twitter en toute confidentialitÃ© ici. Si vous souhaitez signaler un problÃ¨me liÃ© Ã  notre utilisation de vos informations (et sans porter atteinte Ã  tous autres droits dont vous pouvez disposer), vous avez le droit de vous adresser Ã  votre autoritÃ© de supervision locale ou Ã  lâautoritÃ© de supervision de Twitter International Company, Ã  savoir lâIrish Data Protection Commission. Vous trouverez ses coordonnÃ©es ici."

precisionSurObjetDeCollecte = []

mentionDeLaFinalite = ["Traitement", "commandes", "AmÃ©lioration", "service", "Personnalisation", "service",
                       "Proposition", "offres", "AmÃ©lioration", "ciblage", "publicitaire", "A des fins d'Ã©tudes",
                       "fins", "fourniture", "responsable", "traitement", "vue", "valoriser"]
mentionDeLaFinaliteText = " Nous recevons des informations lorsque vous visionnez un contenu ou que vous interagissez autrement avec nos services, mÃªme si vous nâavez pas crÃ©Ã© de compte (Â« DonnÃ©es de journal Â»). Par exemple, lorsque vous visitez nos sites Web, que vous vous authentifiez sur nos services, que vous interagissez avec nos notifications par email, que vous utilisez votre compte pour vous authentifier sur un service tiers, ou que vous visitez un service tiers comprenant un contenu Twitter, nous sommes susceptibles de recevoir des informations Ã  votre sujet. Ces DonnÃ©es de journal sont par exemple votre adresse IP, le type de votre navigateur, votre systÃ¨me dâexploitation, la page Web dâoÃ¹ vous venez, les pages visitÃ©es, votre emplacement, votre opÃ©rateur tÃ©lÃ©phonique, des informations relatives Ã  votre appareil (notamment les identifiants de lâappareil et de lâapplication), des termes de la recherche ou des informations de cookies. Nous recevons Ã©galement des DonnÃ©es de journal lorsque vous cliquez, visualisez ou interagissez avec des liens sur nos services, y compris lorsque vous installez dâautres applications via Twitter. Nous utilisons les DonnÃ©es de journal pour exploiter nos services et assurer leur fonctionnement sÃ©curisÃ©, fiable et robuste. Par exemple, nous utilisons les DonnÃ©es de journal pour protÃ©ger la sÃ©curitÃ© des comptes et pour dÃ©terminer quel contenu est populaire sur nos services. Nous utilisons Ã©galement ces donnÃ©es pour amÃ©liorer le contenu que nous vous prÃ©sentons, y compris les publicitÃ©s. Nous utilisons les informations que vous nous fournissez et les donnÃ©es que nous recevons, telles que les DonnÃ©es de journal et des donnÃ©es provenant de tiers, pour dÃ©duire les thÃ¨mes qui peuvent vous intÃ©resser, votre Ã¢ge et les langues que vous parlez. Cela nous aide Ã  vous proposer des services pertinents et Ã  personnaliser le contenu que nous vous prÃ©sentons, y compris les publicitÃ©s."


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

    # gÃ©rer si le text n'existe pas

    # changer pour un switch avec les diffÃ©rentes formulations possible
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


# fonction Ã  apeller depuis l'api
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
