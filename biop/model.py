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
