# !/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, json, request
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import and_

import random
import sys
import logging
from logging.handlers import RotatingFileHandler

### Change default encoding to utf-8
reload(sys)
sys.setdefaultencoding("utf-8")

### init app & db
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

from models import *

def add_vocabulary(content, content_chinese, part_of_speech, hashtags):
	if is_vocabulary_exist(content, content_chinese) is False: 
		vol = Vocabulary(content, content_chinese, part_of_speech, hashtags)
		db.session.add(vol)
		db.session.commit()
		app.logger.info('%s is added' % vol)
		return True
	return False

def add_hashtag(tag_name):
	if is_hashtag_exist(tag_name) is False:
		hashtag = HashTags(tag_name)
		db.session.add(hashtag)
		db.session.commit()
		app.logger.info('%s is added' % hashtag)
		return True
	return False

def query_vocabulary(content, content_chinese, part_of_speech, hashtags):
	vols = Vocabulary.query\
			.filter(Vocabulary.content == content)\
			.filter(Vocabulary.content_chinese == content_chinese)
	return jsonify(vol=[v.serialize for v in vols])

def query_vocabulary_all():
	return Vocabulary.query.all()

def query_hashtags_all():
	return HashTags.query.all()

def is_vocabulary_exist(content, content_chinese):
	query = db.session.query(Vocabulary)\
			.filter(Vocabulary.content == content)\
			.filter(Vocabulary.content_chinese == content_chinese)
	return db.session.query(query.exists()).scalar()

def is_hashtag_exist(tag_name):
	query = db.session.query(HashTags)\
			.filter(HashTags.tag_name == tag_name)
	return db.session.query(query.exists()).scalar()

### api route settings
@app.route("/mem_vol", methods=['POST', 'GET'])
def men_vol():
	if request.method == 'POST':
		return show_info()
		
	elif request.method == 'GET':
		word = request.args.get('word', '')
		trans = request.args.get('trans', '')
		pos = request.args.get('pos', '')
		hashtags = request.args.get('hashtags', 'general,')		

		if word != '' and trans != '' and pos != '':
			if add_vocabulary(word, trans, pos, hashtags) is True:
				if hashtags != '':
					splited_hashtags = hashtags.split(',')
					for splited_hashtag in splited_hashtags:
						if splited_hashtag is not '':
				   			add_hashtag(splited_hashtag)

		return show_info()
	else:
		return render_template('mem_vol.html')

### for debug 
@app.route("/show_info")
def show_info():
	vols = query_vocabulary_all()
	hashtags = query_hashtags_all()
	return jsonify(vol=[v.serialize for v in vols], \
				   hashtags=[h.serialize for h in hashtags])
# def show_info(hashtags, show_all_hashtags=False):

@app.route("/pop_quiz")
def pop_quiz():

	vols = Vocabulary.query.all()
	pick_index = random.randint(0, len(vols)-1)

	words = vols[pick_index].content
	words_chinese = vols[pick_index].content_chinese
	words_split =[]

	for idx in range(0, len(words)):
		word = []
		word.append(random.randint(0,1))
		word.append(words[idx])
		word.append(idx)
		words_split.append( word )
	
	for word in words_split:
		if ( word [0] == 1 ): 
			first_blank_idx = word[2]
			break

	return render_template('pop_quiz.html', volcabulary=words_split, word=words, word_chi=words_chinese, first_word_idx=first_blank_idx)

### app main 
if __name__ == "__main__":
	formatter = logging.Formatter(\
		"[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
	handler = RotatingFileHandler('vol.log', maxBytes=10000, backupCount=2)
	handler.setLevel(logging.INFO)
	handler.setFormatter(formatter)
	app.logger.addHandler(handler)
	db.create_all()
	app.run(debug=True)

