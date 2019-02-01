#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 9 dï¿½c. 2018

@author: axelc & victorc
'''
import sys
import json
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from collections import defaultdict

# Ne pas oublier de dl toutes les libs
# nltk.download()
path = "./tmp/"
##### PREPROCESSING ######
def del_break(file):
    '''
     Remove breaks from a text
    '''


    f = open(file, "r",encoding = "utf8")
    raw = f.read().replace('\n','')
    f.close()
    output= open(path + file, "w", encoding="utf8")
    print(raw, file=output)
    output.close()

def sentence_tokenize(file, language):
    '''
        Separate texte into indexed sentences.
    '''
    # ATTENTION AU FORMAT DES FICHIERS sinon erreurs possibles -> pour twitter uft8
    # Il faudra adapter le path pour les fichiers des CGUs
    del_break(file)
    f = open(file, encoding="utf8")
    raw = f.read().replace('\n\n', '. ').replace('\n', ' ')
    f.close()
    # l'objet JSON
    data_stopwords = {}
    data = {}

    # segmentation par phrase
    stop_words = set(stopwords.words(language))

    # retire le mot 'not' -> voir quels autres stop words on veut garder
    if language == "english":
        stop_words.remove("not")

    sentences = sent_tokenize(raw)

    key = 0

    for sentence in sentences:
        filtered_sentence = ""

        for w in sentence.split():
            if not w.lower() in stop_words:
                filtered_sentence += ' ' +  w

        data[key] = sentence
        data_stopwords[key] = filtered_sentence
        key += 1


    # donnÃ©es JSON pour le traitement basique
    json_data = json.dumps(data, indent=2)

    # donnÃ©es JSON pour le traitement en retirant les stopwords
    json_data_stopwords = json.dumps(data_stopwords, indent=2)
    #print(json_data_stopwords)


    # rÃ©sultat pour l'instant est juste un fichier output.txt -> choisir le path Ã©galement
    output_file = open(path + "output.txt", "w", encoding="utf8")
    print(json_data, file=output_file)

    # rÃ©sultat pour l'instant est juste un fichier ouput_stopwords.txt -> choisir le path Ã©galement
    output_file_stopwords = open(path + "output_stopwords.txt", "w", encoding="utf8")
    print(json_data_stopwords, file=output_file_stopwords)

    return data, data_stopwords

### Trouver les phrases comportant les mots clefs
def find_sentences(file, language):

        '''
            find useful sentences in the text.
        '''


        (data, data_stopwords) = sentence_tokenize(file, language)

        # mots a chercher
        if language == "english":
            word_to_find = ("Personal data,professional data,Log data,account data,Financial data,Sensitive data,Conservation,Processing,profiling,data controller,third parties,third parties identities,right objection,right access,right delete,Right portability,Consent Security,Binding Corporate Rules ,BCRs,Biometric Data,Data Controller,Data Processor,Data Protection Authority,Data Protection Directive 95 46 EC,Data Protection Officer,DPO,Data Subject,Encrypted Data,Enterprise Content Management,ECM,Genetic Data,Personal Data,Personal Data Breach,Privacy by Design,Privacy Impact,Assessment,PIA,Processing,Profiling,Pseudonymisation,Right to Access,Right to Data Portability,Right to be Forgotten,Supervisory Authority ")
        elif language =="french":
            word_to_find = ("Données personnelles,données professionnelles,données de journal,données de compte,données financières,données sensibles,conservation,traitement,profilage,contrôleurs de données,tiers,identités de tiers,droit d'objection,droit d'accès,supprimer,portabilité,consentement")
        else:
            print("I don't know this language yet.")
        # on les separe pour stem
        word_to_find_2 = [re.split(' ',i) for i in word_to_find.split(",") ]
    #    word_to_find_2 = [i.remove(j) for i in word_to_find_2 for j in i if j == '']
        entire_word = [i for i in word_to_find.split(",")]


        #on stem les mots pour que tout les mots se retrouve avec leurs racines
        #print(entire_word)
        ps = PorterStemmer()
        data_stopwords_stem = set([ps.stem(i) for j in word_to_find_2 for i in j if i != ''])
        data_stopwords_compare = [i for j in word_to_find_2 for i in j]
        stem_new  = [ps.stem(j) for i in word_to_find_2 for j in i]
        stem_list = list()
        for i in word_to_find_2:
            temp_list = list()
            for j in i:
                temp_list.append(ps.stem(j))
            stem_list.append(temp_list)

        #print(stem_list)
        #stopword_test = [ps.stem(i) for i.split(' ') in entire_word for j in i]
        #print(stopword_test)
        mapOfWord = dict(zip(entire_word, stem_list))
        #print(stem_new)
        #print(data_stopwords_compare)
        #print(mapOfWord)
        #print(word_to_find_2)


        word_stem = list()
        for mot_normal in word_to_find_2:
            ls = list()
            for elem_mot_normal in mot_normal:

                for mot_stem in data_stopwords_stem:
                    if mot_stem in elem_mot_normal.lower() and mot_stem != '':
                        ls.append(mot_stem)
            word_stem.append(ls)
        #print(word_stem)

        #print(word_stem)
        # on stem tous les mots du texte à analyser
        words_analysed_from_text  = [{key : ps.stem(i)} for key, value in data_stopwords.items() for i in value.split(" ") ]
        #print(words_analysed_from_text)

        type(words_analysed_from_text)
        #print(words_analysed_from_text)
        #on cherche les mots equivalent ainsi que leur index
        word_found = [(key, value) for i in words_analysed_from_text for key, value in i.items() for k in data_stopwords_stem if value == k  ]
        type(word_found)

        #Same mais pour les mots groupés !
        #word_found_grouped = [(key, value) for i in ]

        # on rassemble les mots de la mÃªme phrases ensemble
        words_by_sentences = defaultdict(list)
        for k, v in word_found:
            words_by_sentences[k].append(v)

        #print(words_by_sentences)
        # on créer le dictonnaire des index + mots trouvés et on supprime les doublons

        index_found = dict([(k, list(set(v))) for k, v in dict(words_by_sentences).items() if v !=[] ])
        len(index_found)
        #print(index_found)
        # on cherche les phrases entieres correspondante
        useful_sentence = [{k1 : [v1,v2]} for k1,v1 in index_found.items() for k2,v2 in data.items() if k1==k2]



        #We try to find the grouped words in the find_sentences
        grouped_result = dict()
        for k,v  in words_by_sentences.items():
            groups = list()
            #print(k,v)

            for lists in word_stem:

                temp_list = list()
                temp_inc = 0

                for word in lists:
                    for elem in v:
                        if (word in elem and word not in temp_list):
                            temp_inc += 1

                            temp_list.append(elem)
                    if temp_inc == len(lists) and temp_list not in groups:
                        #print(temp_inc)
                        groups.append(temp_list)
            for item in groups:
                if item != None:
                    grouped_result.update({k:groups})
            #print(stem_new)
        final_data = dict()

        for index, stemword in grouped_result.items():

            temp_list = list()
            #print(stemword)
            #print(lengthstem)


            for lists in stemword:  # pour chaque listes de stemword


                for realword,stemword2 in mapOfWord.items(): # pour chaque vrai mots clefs associer aux listes de stemword
                    temp_inc = 0
                    temp_word = None

                    if len(lists) == len(stemword2):
                        for word in lists:  # pour chaque mot de la phrase
                            for word2 in stemword2: # pour chaque mot a de la map
                                    if word == word2 and temp_inc < len(lists):
                                        temp_inc += 1
                                        if temp_inc == len(lists):
                                            '''print(index , stemword)
                                            print(realword)
                                            print("break")'''
                                            break

                                    #print(word, word2, temp_inc, lengthstem, "\n")

                            if temp_inc == len(lists) :

                                temp_word = realword
                                break
                                #print(realword)


                        if temp_word != None:

                            temp_list.append(temp_word)
                            print(index,stemword, temp_list)
                            break

                    if len(temp_list) == len(stemword):
                        break

                if len(temp_list) == len(stemword):
                    break





                '''if len(stemword2) < 2 and temp_inc > 0 and temp_inc < 2:
                    temp_list.append(temp_word)

                elif len(stemword2) == 2 and temp_inc ==2:
                    temp_list.append(temp_word)


                elif len(stemword2)>2 and temp_inc > len(v)/2 +1 :
                    temp_list.append(temp_word)'''

            final_data.update({index : temp_list})

        print(final_data)
        #useful_sentence = [{k1 : [v1,v2]} for k1,v1 in index_found.items() for k2,v2 in data.items() if k1==k2]
        useful_sentence_full = [{k1 : [v1,v2]} for k1,v1 in final_data.items() for k2,v2 in data.items() if k1==k2]
        #on output
        #print(grouped_result)
        json_useful_sentence = json.dumps(useful_sentence, indent=3)
        output_useful_sentence = open("./useful_sentence.txt", "w", encoding="utf8")
        print(json_useful_sentence, file=output_useful_sentence)

        json_useful_sentence_full = json.dumps(useful_sentence_full, indent=3)
        output_useful_sentence_full = open("./useful_sentence_full.txt", "w", encoding="utf8")
        print(json_useful_sentence_full, file=output_useful_sentence_full)
        #print(json_useful_sentence)
        #print(json_useful_sentence)
        return json_useful_sentence_full

if __name__ == "__main__":
    find_sentences(sys.argv[1], sys.argv[2])

# COMPARER CES PHRASES AVEC l
