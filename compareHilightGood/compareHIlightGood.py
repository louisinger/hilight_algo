# imports needed and logging
import gzip
import gensim 
import logging
import os
import json
# Load the Pandas libraries with alias 'pd' 
import pandas as pd 

from gensim import corpora
from pprint import pprint
from gensim import models
from gensim import similarities
from gensim.utils import simple_preprocess
from smart_open import smart_open


#################################################################################################
class SubCriteria:
	def __init__(self, name, grade, sentence):
		self.nameSubCriteria = name
		self.gradeSubCriteria = grade
		self.bestSentence = sentence
	def toString(self):
		print("	------------------------------------------------")
		print("		Name Sub Criteria  : " + self.nameSubCriteria)
		
		print("		Grade Sub Criteria : " + str(self.gradeSubCriteria))
		print("		Sentence           : " + self.bestSentence)

		
class Criteria:
	
	def __init__(self, name):
		self.subCriterias = []
		self.subCriterias.append(SubCriteria(" ", 4, " "))
		self.subCriterias.clear()
		self.nameCriteria = name
		self.gradeCriteria = -6 # -6 -> we don't know the grade
		self.lenSubCriteriaOk = 0
	def addSubCriteria(self, subCriteria):
		self.subCriterias.append(subCriteria)
		if(subCriteria.gradeSubCriteria != -100): # if = -100 -> ignore -> we don't know
			self.lenSubCriteriaOk+=1
			if(self.gradeCriteria == -6): #if first subcriteria added
				self.gradeCriteria = subCriteria.gradeSubCriteria
			else:
				total = 0
				for sub in self.subCriterias:
					if(sub.gradeSubCriteria != -100):
						total += sub.gradeSubCriteria
						self.gradeCriteria = total / self.lenSubCriteriaOk
	
	def displayCriteria(self):
		print("\n")
		print("--------------------------- Criteria --------------------------- ")
		print("Name Criteria : " + self.nameCriteria)
		print("Grade Criteria : " + str(self.gradeCriteria))
		print("\n")
		for sub in self.subCriterias:
			sub.toString()
#################################################################################################

def initModel():
	criterias = [] # length 22
	criterias.append(Criteria("Clarification on the purpose of the collection"))
	criterias.append(Criteria("Clarification on the collection process"))
	criterias.append(Criteria("Mention of the purpose"))
	criterias.append(Criteria("Conservation"))
	criterias.append(Criteria("Profiling"))
	criterias.append(Criteria("Identity of the controller"))
	criterias.append(Criteria("Carrying out a processing operation by a subcontractor"))
	criterias.append(Criteria("Disclosure of data to third parties"))
	criterias.append(Criteria("Mention of the identity of third parties"))
	criterias.append(Criteria("Mention of the purpose of the transfer"))
	criterias.append(Criteria("Right of opposition"))
	criterias.append(Criteria("Right to access"))
	criterias.append(Criteria("Right of rectification "))
	criterias.append(Criteria("Right to erase"))
	criterias.append(Criteria("Right to portability "))
	criterias.append(Criteria("Information on the existence of cookies and other tracking tools"))
	criterias.append(Criteria("Mention of the existence of links with social networks or other sites "))
	criterias.append(Criteria("Consent / Acceptance"))
	criterias.append(Criteria("Scope of consent"))
	criterias.append(Criteria("Information on the unilateral amendment of the charter"))
	criterias.append(Criteria("Consent to the amendment"))
	criterias.append(Criteria("Safety and security"))
	criterias.append(Criteria("Measures taken to ensure security"))
	#################################################################################################


	dir = os.path.dirname(__file__)
	filename = os.path.join(dir, 'GrilleHiLights-Edited-v1-English-test.csv')
	#filename = os.path.join(dir, 'GrilleHiLights-Edited-v1-French.csv')

	# Read data from file 'filename.csv' 
	# (in the same directory that your python process is based)
	# Control delimiters, rows, column names with read_csv (see later) 
	data = pd.read_csv(filename) 

	dictVariableSubVariable=[]

	cpt = 0
	for subVariable in data['Sous-variables']:
		subVariable = str(subVariable)
		res = subVariable.split(" ", 1)
		if(len(res) > 1):
			tempstring = res[1]
			# print(data['Variable'][cpt] +" " +tempstring)
			dictVariableSubVariable.append(str(data['u'][cpt]) +" " +tempstring)
		cpt+=1

	# print("longueur sub variable" + str(len(dictVariableSubVariable)))
		
	# Tokenize the docs
	tokenized_list = [simple_preprocess(doc) for doc in dictVariableSubVariable]

	# Create the Corpus
	mydict = corpora.Dictionary()
	mycorpus = [mydict.doc2bow(doc, allow_update=True) for doc in tokenized_list]

	#build model
	tfidf = models.TfidfModel(mycorpus)
	index = similarities.SparseMatrixSimilarity(tfidf[mycorpus], num_features=500)



	dictBad = []
	dictOk = []
	dictGood = []

	############################### bad ###############################
	for phrase in data['-1']:
		phrase = str(phrase)
		if(phrase==' ' or phrase=='nan'):
			phrase = "None"
		# print(data['Variable'][cpt] +" " +tempstring)
		dictBad.append(phrase)

	# Tokenize the docs
	tokenized_list_bad = [simple_preprocess(doc) for doc in dictBad]

	# Create the Corpus
	mycorpus_bad = [mydict.doc2bow(doc, allow_update=True) for doc in tokenized_list_bad]

	#build model
	tfidf_bad = models.TfidfModel(mycorpus_bad)
	index_bad = similarities.SparseMatrixSimilarity(tfidf_bad[mycorpus_bad], num_features=1000)


	############################### ok ###############################
	for phrase2 in data['0']:
		phrase2 = str(phrase2)
		if(phrase2==' ' or phrase2=='nan'):
			phrase2 = "None"
		# print(data['Variable'][cpt] +" " +tempstring)
		dictOk.append(phrase2)

	# Tokenize the docs
	tokenized_list_Ok = [simple_preprocess(doc) for doc in dictOk]

	# Create the Corpus
	mycorpus_Ok = [mydict.doc2bow(doc, allow_update=True) for doc in tokenized_list_Ok]

	#build model
	tfidf_Ok = models.TfidfModel(mycorpus_Ok)
	index_oK = similarities.SparseMatrixSimilarity(tfidf_Ok[mycorpus_Ok], num_features=1000)

	############################### good ###############################
	for phrase3 in data['1']:
		phrase3 = str(phrase3)
		if(phrase3==' ' or phrase3=='nan'):
			phrase3 = "None"
		# print(data['Variable'][cpt] +" " +tempstring)
		dictGood.append(phrase3)

	# Tokenize the docs
	tokenized_list_good = [simple_preprocess(doc) for doc in dictGood]

	# Create the Corpus
	mycorpus_good = [mydict.doc2bow(doc, allow_update=True) for doc in tokenized_list_good]

	#build model
	tfidf_good = models.TfidfModel(mycorpus_good)
	index_good = similarities.SparseMatrixSimilarity(tfidf_good[mycorpus_good], num_features=1000)
	
	####################################### json processing
	#fileName = 'AI prototype v1.0_useful_sentence_full.json'

	fileName = 'goodJson.json'

	###########################################
	file2 = os.path.join(dir, fileName)

	with open(file2) as jsonpolicy:
			dataJsonPolicy = json.load(jsonpolicy)

	keysTable = []
	for key in dataJsonPolicy:
		totalkey = ""
		for keys in key["keywords"]:
			##total key from the json
			totalkey += keys + " "
		keysTable.append(totalkey)


	j=0
	for st in keysTable:
		if(st == ''):
			keysTable[j] ="None"
		j+=1

	# Tokenize the docs
	tokenized_list_keyPrivacy = [simple_preprocess(doc) for doc in keysTable]

	# Create the Corpus
	mycorpus_keyPrivacy = [mydict.doc2bow(doc, allow_update=True) for doc in tokenized_list_keyPrivacy]

	#build model
	tfidf_keyPrivacy = models.TfidfModel(mycorpus_keyPrivacy)
	index_keyPrivacy = similarities.SparseMatrixSimilarity(tfidf_keyPrivacy[mycorpus_keyPrivacy], num_features=1000)





#return a vector from the words given
def vectoriceText(textToVector, dictionarydoc2bow):
	ToTest=[]
	ToTest.append(textToVector)
	# Tokenize the docs
	tokenized_list_test_privacy = [simple_preprocess(doc) for doc in ToTest]
	
	mycorpus_test_privacy = [dictionarydoc2bow.doc2bow(doc, allow_update=True) for doc in tokenized_list_test_privacy]
	
	# print("********* vector value *********")
	# print(mycorpus_test_privacy)
	# print("********* vector value *********")
	
	return mycorpus_test_privacy
	
def getSimilaritiesFromVectorToModel(indexGeneric, tfidfGeneric, vectorToCompare):
	return indexGeneric[tfidfGeneric[vectorToCompare]]
	
def getHighestSimilarities(simVector):
	i=0
	maxValue=-1
	maxI=-1
	for test in simVector:
		# print (test)
		for testV in test:
			if(maxValue < testV):
				maxValue = testV
				maxI=i
			i+=1

	# print (maxI)
	return maxI
	# print (tokenized_list[maxi])

def getHighestSimilaritiesPercent(simVector):
	i=0
	maxValue=-1
	maxI=-1
	for test in simVector:
		# print (test)
		for testV in test:
			if(maxValue < testV):
				maxValue = testV
				maxI=i
			i+=1

	# print (simVector)
	return maxValue
	#print (tokenized_list[maxi])
	
def getSimilaritiesWithNumber(simVector, numberToCompare):
	i=0
	# print("numberToCompare")
	# print(numberToCompare)
	# print(simVector)
	return(simVector[0][numberToCompare])
	

def getPrivacyGradesPerCriter(ParfileName):
	# initModel()
	criterias = [] # length 22
	criterias.append(Criteria("Clarification on the purpose of the collection"))
	criterias.append(Criteria("Clarification on the collection process"))
	criterias.append(Criteria("Mention of the purpose"))
	criterias.append(Criteria("Conservation"))
	criterias.append(Criteria("Profiling"))
	criterias.append(Criteria("Identity of the controller"))
	criterias.append(Criteria("Carrying out a processing operation by a subcontractor"))
	criterias.append(Criteria("Disclosure of data to third parties"))
	criterias.append(Criteria("Mention of the identity of third parties"))
	criterias.append(Criteria("Mention of the purpose of the transfer"))
	criterias.append(Criteria("Right of opposition"))
	criterias.append(Criteria("Right to access"))
	criterias.append(Criteria("Right of rectification "))
	criterias.append(Criteria("Right to erase"))
	criterias.append(Criteria("Right to portability "))
	criterias.append(Criteria("Information on the existence of cookies and other tracking tools"))
	criterias.append(Criteria("Mention of the existence of links with social networks or other sites "))
	criterias.append(Criteria("Consent / Acceptance"))
	criterias.append(Criteria("Scope of consent"))
	criterias.append(Criteria("Information on the unilateral amendment of the charter"))
	criterias.append(Criteria("Consent to the amendment"))
	criterias.append(Criteria("Safety and security"))
	criterias.append(Criteria("Measures taken to ensure security"))
	#################################################################################################


	dir = os.path.dirname(__file__)
	filename = os.path.join(dir, 'GrilleHiLights-Edited-v1-English-test.csv')
	#filename = os.path.join(dir, 'GrilleHiLights-Edited-v1-French.csv')

	# Read data from file 'filename.csv' 
	# (in the same directory that your python process is based)
	# Control delimiters, rows, column names with read_csv (see later) 
	data = pd.read_csv(filename) 

	dictVariableSubVariable=[]

	cpt = 0
	for subVariable in data['Sous-variables']:
		subVariable = str(subVariable)
		res = subVariable.split(" ", 1)
		if(len(res) > 1):
			tempstring = res[1]
			# print(data['Variable'][cpt] +" " +tempstring)
			dictVariableSubVariable.append(str(data['u'][cpt]) +" " +tempstring)
		cpt+=1

	# print("longueur sub variable" + str(len(dictVariableSubVariable)))
		
	# Tokenize the docs
	tokenized_list = [simple_preprocess(doc) for doc in dictVariableSubVariable]

	# Create the Corpus
	mydict = corpora.Dictionary()
	mycorpus = [mydict.doc2bow(doc, allow_update=True) for doc in tokenized_list]

	#build model
	tfidf = models.TfidfModel(mycorpus)
	index = similarities.SparseMatrixSimilarity(tfidf[mycorpus], num_features=500)



	dictBad = []
	dictOk = []
	dictGood = []

	############################### bad ###############################
	for phrase in data['-1']:
		phrase = str(phrase)
		if(phrase==' ' or phrase=='nan'):
			phrase = "None"
		# print(data['Variable'][cpt] +" " +tempstring)
		dictBad.append(phrase)

	# Tokenize the docs
	tokenized_list_bad = [simple_preprocess(doc) for doc in dictBad]

	# Create the Corpus
	mycorpus_bad = [mydict.doc2bow(doc, allow_update=True) for doc in tokenized_list_bad]

	#build model
	tfidf_bad = models.TfidfModel(mycorpus_bad)
	index_bad = similarities.SparseMatrixSimilarity(tfidf_bad[mycorpus_bad], num_features=1000)


	############################### ok ###############################
	for phrase2 in data['0']:
		phrase2 = str(phrase2)
		if(phrase2==' ' or phrase2=='nan'):
			phrase2 = "None"
		# print(data['Variable'][cpt] +" " +tempstring)
		dictOk.append(phrase2)

	# Tokenize the docs
	tokenized_list_Ok = [simple_preprocess(doc) for doc in dictOk]

	# Create the Corpus
	mycorpus_Ok = [mydict.doc2bow(doc, allow_update=True) for doc in tokenized_list_Ok]

	#build model
	tfidf_Ok = models.TfidfModel(mycorpus_Ok)
	index_oK = similarities.SparseMatrixSimilarity(tfidf_Ok[mycorpus_Ok], num_features=1000)

	############################### good ###############################
	for phrase3 in data['1']:
		phrase3 = str(phrase3)
		if(phrase3==' ' or phrase3=='nan'):
			phrase3 = "None"
		# print(data['Variable'][cpt] +" " +tempstring)
		dictGood.append(phrase3)

	# Tokenize the docs
	tokenized_list_good = [simple_preprocess(doc) for doc in dictGood]

	# Create the Corpus
	mycorpus_good = [mydict.doc2bow(doc, allow_update=True) for doc in tokenized_list_good]

	#build model
	tfidf_good = models.TfidfModel(mycorpus_good)
	index_good = similarities.SparseMatrixSimilarity(tfidf_good[mycorpus_good], num_features=1000)
	
	####################################### json processing
	#fileName = 'AI prototype v1.0_useful_sentence_full.json'

	fileName = 'goodJson.json'

	###########################################
	#file2 = os.path.join(dir, fileName)
	file2 = ParfileName

#	with open(file2) as jsonpolicy:
#           dataJsonPolicy = json.load(jsonpolicy)
        
	dataJsonPolicy =json.loads(ParfileName['result'])
	keysTable = []
	for key in dataJsonPolicy:
		totalkey = ""
		for keys in key["keywords"]:
			##total key from the json
			totalkey += keys + " "
		keysTable.append(totalkey)


	j=0
	for st in keysTable:
		if(st == ''):
			keysTable[j] ="None"
		j+=1

	# Tokenize the docs
	tokenized_list_keyPrivacy = [simple_preprocess(doc) for doc in keysTable]
	# Create the Corpus
	mycorpus_keyPrivacy = [mydict.doc2bow(doc, allow_update=True) for doc in tokenized_list_keyPrivacy]

	#build model
	tfidf_keyPrivacy = models.TfidfModel(mycorpus_keyPrivacy)
	index_keyPrivacy = similarities.SparseMatrixSimilarity(tfidf_keyPrivacy[mycorpus_keyPrivacy], num_features=1000)

	########################################################
	#file2 = os.path.join(dir, ParfileName)
	
	#with open(file2) as jsonpolicy:
		#dataJsonPolicy = json.load(jsonpolicy)

	dataJsonPolicy =json.loads(ParfileName['result'])

	keysTable = []
	for key in dataJsonPolicy:
		totalkey = ""
		for keys in key["keywords"]:
			#total key from the json
			totalkey += keys + " "
		keysTable.append(totalkey)
		
	j=0
	for st in keysTable:
		if(st == ''):
			keysTable[j] ="None"
		j+=1

	# !comment Tokenize the docs
	tokenized_list_keyPrivacy = [simple_preprocess(doc) for doc in keysTable]

	# !comment Create the Corpus
	mycorpus_keyPrivacy = [mydict.doc2bow(doc, allow_update=True) for doc in tokenized_list_keyPrivacy]

	# !comment build model
	tfidf_keyPrivacy = models.TfidfModel(mycorpus_keyPrivacy)
	index_keyPrivacy = similarities.SparseMatrixSimilarity(tfidf_keyPrivacy[mycorpus_keyPrivacy], num_features=1000)

	# !comment getSimilaritiesFromVectorToModel(index_keyPrivacy, tfidf_keyPrivacy, vectoriceText("data")) -> matrice
	
	highestMatchPerCriter = []
	listScore = []
	i = 0
	subCriteriaIndex = 0
	for subvariable in dictVariableSubVariable:
		#lengthCriterias =[6,4,8,2,2,8,3,5,1,5,1,1,1,1,3,7,1,3,3,4,3,2,6]
		
		highestMatchPerCriter.append(0)
		listScore.append(0)
		
		#text2Vec for the subCriteria
		subvariableVectorized = vectoriceText(subvariable, mydict)
		
		#get the vector similarities between subvariable and keys of privacy extracted from (json) 
		simVector = getSimilaritiesFromVectorToModel(index_keyPrivacy, tfidf_keyPrivacy, subvariableVectorized)
		
		idHihestSim = getHighestSimilarities(simVector)
		# !comment matching keywords : tokenized_list_keyPrivacy[idHihestSim]
		highestMatchPerCriter[i] = idHihestSim
		
		# print(dataJsonPolicy[idHihestSim])
		j=0
		# !comment optimisable
		bestSentenceFromPolicy = ""
		for key in dataJsonPolicy:
			if(j == idHihestSim):
				# !comment phrase to compare -> key[sentence]
				phraseVectorized = vectoriceText(key["sentence"],mydict)
				
				# !comment bad
				similaritiesBad = getSimilaritiesFromVectorToModel(index_bad, tfidf_bad, phraseVectorized)
				percentageBad = getSimilaritiesWithNumber (similaritiesBad,i)
				# print("debug similaritiesBad")
				
				# !comment ok
				similaritiesOk = getSimilaritiesFromVectorToModel(index_oK, tfidf_Ok, phraseVectorized)
				percentageOk = getSimilaritiesWithNumber (similaritiesOk,i)
				# print("debug similaritiesOk")
				
				# !comment good
				similaritiesGood = getSimilaritiesFromVectorToModel(index_good, tfidf_good, phraseVectorized)
				percentageGood = getSimilaritiesWithNumber (similaritiesGood,i)
				# print("debug similaritiesGood")
				
				# print('-----')
				# print(percentageBad)
				# print(percentageOk)
				# print(percentageGood)
				
				score=6
				if(percentageBad > percentageOk):
					if (percentageBad > percentageGood):
						score = -1
					elif (percentageBad < percentageGood):
						score = 1
					else: #score = 6 si tout egal
						score = 6
				elif (percentageBad < percentageOk):
					if (percentageOk > percentageGood):
						score = 0
					elif (percentageOk < percentageGood):
						score = 1
					else: #score = 6 si tout egal
						score = 6
				
				listScore[i] = score
				
				bestSentenceFromPolicy = key["sentence"]
				# put score here -> listScore[i] =
			j+=1
		i+=1
		
		# get id of the max similarities
	# for idVariable in highestMatchPerCriter:
		# if(idVariable != 0):
		if(listScore[subCriteriaIndex] == 6): # we don't know
			subCriteriaTempo = SubCriteria(subvariable, -100, "We don't know")
		else:
			subCriteriaTempo = SubCriteria(subvariable, listScore[subCriteriaIndex], bestSentenceFromPolicy)
		if(subCriteriaIndex < 6):
			criterias[0].addSubCriteria(subCriteriaTempo)
			# print(criterias[0].displayCriteria())
		elif(subCriteriaIndex < 10):
			criterias[1].addSubCriteria(subCriteriaTempo)
			# print(criterias[1].displayCriteria())
		elif(subCriteriaIndex < 18):
			criterias[2].addSubCriteria(subCriteriaTempo)
			# print(criterias[2].displayCriteria())
		elif(subCriteriaIndex < 20):
			criterias[3].addSubCriteria(subCriteriaTempo)
			# print(criterias[3].displayCriteria())
		elif(subCriteriaIndex < 22):
			criterias[4].addSubCriteria(subCriteriaTempo)
			# print(criterias[4].displayCriteria())
		elif(subCriteriaIndex < 30):
			criterias[5].addSubCriteria(subCriteriaTempo)
			# print(criterias[5].displayCriteria())
		elif(subCriteriaIndex < 33):
			criterias[6].addSubCriteria(subCriteriaTempo)
			# print(criterias[6].displayCriteria())
		elif(subCriteriaIndex < 38):
			criterias[7].addSubCriteria(subCriteriaTempo)
			# print(criterias[7].displayCriteria())
		elif(subCriteriaIndex < 39):
			criterias[8].addSubCriteria(subCriteriaTempo)
			# print(criterias[8].displayCriteria())
		elif(subCriteriaIndex < 44):
			criterias[9].addSubCriteria(subCriteriaTempo)
			# print(criterias[9].displayCriteria())
		elif(subCriteriaIndex < 45):
			criterias[10].addSubCriteria(subCriteriaTempo)
			# print(criterias[10].displayCriteria())
		elif(subCriteriaIndex < 46):
			criterias[11].addSubCriteria(subCriteriaTempo)
			# print(criterias[11].displayCriteria())
		elif(subCriteriaIndex < 47):
			criterias[12].addSubCriteria(subCriteriaTempo)
			# print(criterias[12].displayCriteria())
		elif(subCriteriaIndex < 48):
			criterias[13].addSubCriteria(subCriteriaTempo)
			# print(criterias[13].displayCriteria())
		elif(subCriteriaIndex < 51):
			criterias[14].addSubCriteria(subCriteriaTempo)
			# print(criterias[14].displayCriteria())
		elif(subCriteriaIndex < 58):
			criterias[15].addSubCriteria(subCriteriaTempo)
			# print(criterias[15].displayCriteria())
		elif(subCriteriaIndex < 59):
			criterias[16].addSubCriteria(subCriteriaTempo)
			# print(criterias[16].displayCriteria())
		elif(subCriteriaIndex < 62):
			criterias[17].addSubCriteria(subCriteriaTempo)
			# print(criterias[17].displayCriteria())
		elif(subCriteriaIndex < 65):
			criterias[18].addSubCriteria(subCriteriaTempo)
			# print(criterias[18].displayCriteria())
		elif(subCriteriaIndex < 69):
			criterias[19].addSubCriteria(subCriteriaTempo)
			# print(criterias[19].displayCriteria())
		elif(subCriteriaIndex < 72):
			criterias[20].addSubCriteria(subCriteriaTempo)
			# print(criterias[20].displayCriteria())
		elif(subCriteriaIndex < 74):
			criterias[21].addSubCriteria(subCriteriaTempo)
			# print(criterias[21].displayCriteria())
		#elif(subCriteriaIndex < 80):
		else:
			criterias[22].addSubCriteria(subCriteriaTempo)
			# print(criterias[22].displayCriteria())
			
		subCriteriaIndex+=1
	'''for c in criterias:
		c.displayCriteria()'''
		
	json_string = json.dumps(listScore)
	return json_string
	#return listScore



#print(getPrivacyGradesPerCriter(fileName))
#oui = (getPrivacyGradesPerCriter("goodJson.json"))
#print(oui)
#getPrivacyGradesPerCriter("goodJson.json")

	

		
	
	
	
	
	
	
	
	
	
	
	
	
	
	



