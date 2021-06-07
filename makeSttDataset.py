import textPre.pdftxt as pdft
import textPre.ppttxt as pptt
import textPre.extprocess as prc
import textPre.lrword as lrw
import textPre.makejson as mjson
import os
import time
import pickle
import pandas as pd
from konlpy.tag import Mecab
import json
# start = time.time()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='YOUR GOOGLE CLOUD KEY PATH'

def openFile(url):
	if os.path.splitext(url)[1]=='.pdf':
		text = pdft.read_pdf_PDFMINER(url)
		print('filename extension: .pdf')
	elif os.path.splitext(url)[1]=='.pptx':
		text = pptt.read_ppt(url)
		print('filename extenstion: .pptx')
	else:
		print("error: unknown filename extension")
	return text

def cleanText(text):
	t = prc.clean_txt(text)
	# t = prc.check_spell(text)
	return t

def getStopwords():
	stopfile = 'stopword_ko.csv'
	stopdata = pd.read_csv(stopfile, encoding='utf-8')
	stopset = list(stopdata.stopword)
	#print(list(stopdata.stopword))
	return stopset

def getWords(text, stopset):
	mecab = Mecab()
	pos = mecab.pos(text)

	vocab_ko = {}
	noun_nn_pre = []
	noun_nn = []
	noun_fo = []

	tag_nn = ['NNG','NNP']
	noun_nn_pre = [w[0] for w in pos if w[1] in tag_nn]
	noun_fo = [w[0] for w in pos if w[1]=='SL']
	noun_nn = [word for word in noun_nn_pre if word not in stopset]
	for w in noun_nn:
		if w not in vocab_ko:
			vocab_ko[w] = 0
		vocab_ko[w] += 1
	vocab = sorted(vocab_ko.items(), key =lambda x: x[1], reverse=True)

	vocab_hr = [k for k, v in vocab if v>4]
	vocab_lr = [k for k, v in vocab if v<=4]

	temp=[w for w in noun_nn_pre if len(w)>1] + noun_fo
	afterset=list(set(temp))

	pos = [w[0] for w in pos]
	return pos, vocab_hr, vocab_lr, noun_fo, afterset

def writeResult(pos, vocab_fin, M):
	loc = "/home/yjlee/Desktop/"
	# pos: raw words from uploaded file
	f = open(loc +"raw_pos.txt", 'w')
	f.write(', '.join(pos))
	f.close()
	# Vocab_Fin : list sending to stt
	f = open(loc + "vocab_fin.txt", 'w')
	f.write("\n".join(vocab_fin))
	f.close()
	# sendig stt format - no weight
	f = open(loc + "w_request.txt", 'w')
	f.write(', '.join(M))
	f.close()

def writeAfterset(afterset):
   loc = '/home/ubuntu/workspace/demo/dataset/'
   f = open(loc +"afterset.txt", 'w')
   f.write(', '.join(afterset))
   f.close()
   print('Afterset Created')


def make_dataset(filename):

	# DIR WHERE FILE EXISTS
	loc = '/home/ubuntu/workspace/demo/data/'

	# line86 : will be deleted soon
	url = loc + filename#'note1.pdf'

	# NO NEED TO INPUT FILENAME, ONLY DIR NAME REQUIRED
	# filelist = os.listdir(loc)
	# url = loc + filelist[0]

	text = openFile(url)
	clean_txt = cleanText(text)
	stopset = getStopwords()
	pos, vocab_hr, vocab_lr, noun_fo, afterset = getWords(clean_txt, stopset)

	# for low rank
	vocab_lr_new = lrw.extractWord(vocab_lr)
	# final word dataset
	vocab_fin = vocab_hr + vocab_lr_new

	writeAfterset(afterset)

	M = []
	for i in vocab_fin:
		M.append('{ \"phrases\" : \"'+ i +'\", "boost" :' + '10' + ' }')
	#json.dumps(M)

	# write to textfile: rawdata, finaldata, sending format (with weight)
	#writeResult(pos, vocab_fin, M)
	# make json
	mjson.makejson("/home/ubuntu/workspace/demo/json/", vocab_fin)

	print("Success")



#make_dataset()
