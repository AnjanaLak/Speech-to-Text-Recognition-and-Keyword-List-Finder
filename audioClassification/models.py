from datetime import datetime
from audioClassification import db
from audioClassification import ma


#################### DB models ######################################################################

class Audio_Record(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    candidateID = db.Column(db.String(20))
    examID = db.Column(db.String(20))
    chunkDirectory = db.Column(db.String(500))
    processed_time = db.Column(db.DateTime, default=datetime.now)
    keywords = db.Column(db.String(500))

    def __init__(self, candidateID, examID, chunkDirectory, processed_time, keywords):
        self.candidateID = candidateID
        self.examID = examID
        self.chunkDirectory = chunkDirectory
        self.processed_time = processed_time
        self.keywords = keywords

    def __repr__(self):
        return f"Audio_Record('{self.candidateID}', '{self.examID}', '{self.chunkDirectory}',  '{self.processed_time}', " \
               f"'{self.keywords}')"


### Class Candidate

# class Candidate(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
#     password = db.Column(db.String(60), nullable=False)
#     posts = db.relationship('Post', backref='author', lazy=True)
#
#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}', '{self.image_file}')"
#

class Audio_Record_Schema(ma.Schema):
    class Meta:
        fields = ('candidateID', 'examID', 'chunkDirectory', 'processed_time', 'keywords')


audio_Record_Schema = Audio_Record_Schema()
audio_Record_Schemas = Audio_Record_Schema(many=True)
