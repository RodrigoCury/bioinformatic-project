from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class Sequence_model(db.Model):
    seq_id = db.Column(db.Integer, primary_key=True)
    seq_type = db.Column(db.String, nullable=False)
    sequence = db.Column(db.String, nullable=False)
    translation_table = db.Column(db.String, nullable=False)
    creationDate = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"sequencia {self.seq_id} ; {self.seq_type} ; {self.sequence} ; {self.translation_table} ; {self.creationDate}"

    def __str__(self):
        return f"sequencia {self.seq_id} ; {self.seq_type} ; {self.sequence} ; {self.translation_table} ; {self.creationDate}"


class Alignment_model(db.Model):
    align_id = db.Column(db.Integer, primary_key=True)
    seq1 = db.Column(db.String, nullable=False)
    seq2 = db.Column(db.String, nullable=False)
    alignment_type = db.Column(db.String, nullable=False)
    creationDate = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __str__(self):
        return f"ID: {self.align_id}; \n 1st Sequence: {self.seq1} \n ; 2nd Sequence: {self.seq2}; \n"

    def __repr__(self):
        return f"ID: {self.align_id}; \n 1st Sequence: {self.seq1} \n ; 2nd Sequence: {self.seq2}; \n"
