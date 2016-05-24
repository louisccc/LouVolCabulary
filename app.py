# !/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, json
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy

import random
import sys

### Change default encoding to utf-8
reload(sys)
sys.setdefaultencoding("utf-8")

### init app & db
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

### DB model def
class Volcabulary(db.Model):
	# __tablename__ = "volca"

	vol_id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(40))
	content_chinese = db.Column(db.String(60))

	def __init__(self, content, content_chinese):
		self.content = content
		self.content_chinese = content_chinese

	def __repr__(self):
		return '<Volcabulary: %d %s %s>' % (self.vol_id, self.content, self.content_chinese)

	@property
	def serialize(self):
		return {
			'id' : self.vol_id,
			'content' : self.content,
			'content_chinese' : self.content_chinese
		}

### api route settings
@app.route("/")
def hello():
	vol = Volcabulary("astronaut", u"太空人")
	# print vol
	db.session.add(vol)
	db.session.commit()
	# print db.session
	# vols = Volcabulary.query.all()
	# print vols
	# print len(vols)
	# for v in vols:
	# 	print v
	return "Hello World!"

@app.route("/mem_vol")
def men_vol():
	pass

@app.route("/show_vol")
def show_vol():
	vols = Volcabulary.query.all()
	return jsonify(data=[v.serialize for v in vols])

@app.route("/pop_quiz")
def pop_quiz():

	words = 'astronaut'
	words_chinese = u'太空人'
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
    db.create_all()
    app.run(debug=True)

