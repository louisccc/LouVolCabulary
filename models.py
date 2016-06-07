from app import db
### DB model def
class Vocabulary(db.Model):

	vol_id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(40))
	content_chinese = db.Column(db.String(60))
	part_of_speech = db.Column(db.String(10))
	hashtags = db.Column(db.String(256))


	def __init__(self, content, content_chinese, part_of_speech, hashtags):
		self.content = content
		self.content_chinese = content_chinese
		self.part_of_speech = part_of_speech
		self.hashtags = hashtags
	def __repr__(self):
		return '<Vocabulary: vol_id=%d content=%s chi_content=%s pos=%s hashtags=%s>' \
		% (self.vol_id, self.content, self.content_chinese, self.part_of_speech, self.hashtags)
	@property
	def serialize(self):
		return {
			'id' : self.vol_id,
			'content' : self.content,
			'content_chinese' : self.content_chinese,
			'part_of_speech': self.part_of_speech,
			'hashtags': self.hashtags
		}

class HashTags(db.Model):
	tag_id = db.Column(db.Integer, primary_key=True)
	tag_name = db.Column(db.String(64))

	def __init__(self, tag_name):
		self.tag_name = tag_name
	def __repr__(self):
		return '<HashTags: tag_id=%d, tag_name=%s>' \
		% (self.tag_id, self.tag_name)
	@property
	def serialize(self):
		return {
			'tag_id': self.tag_id,
			'tag_name': self.tag_name
		}