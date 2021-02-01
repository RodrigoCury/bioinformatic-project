from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()


class Sequence_model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seq_type = db.Column(db.String, nullable=False)
    sequence = db.Column(db.String, nullable=False)
    translation_table = db.Column(db.String, nullable=False)
    creationDate = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"sequencia {self.id} ; {self.seq_type} ; {self.sequence} ; {self.translation_table} ; {self.creationDate}"

    def __str__(self):
        return f"sequencia {self.id} ; {self.seq_type} ; {self.sequence} ; {self.translation_table} ; {self.creationDate}"


class Alignment_model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target_seq = db.Column(db.String, nullable=False)
    query_seq = db.Column(db.String, nullable=False)
    alignment_type = db.Column(db.String, nullable=False)
    score_schema = db.Column(db.String, nullable=False)
    substitution_matrix = db.Column(db.String, nullable=True)
    match_score = db.Column(db.Integer, nullable=True)
    mismatch_score = db.Column(db.Integer, nullable=True)
    gap_score = db.Column(db.Integer, nullable=True)
    target_internal_open_gap_score = db.Column(db.Integer, nullable=True)
    target_internal_extend_gap_score = db.Column(db.Integer, nullable=True)
    target_left_extend_gap_score = db.Column(db.Integer, nullable=True)
    target_left_open_gap_score = db.Column(db.Integer, nullable=True)
    target_right_open_gap_score = db.Column(db.Integer, nullable=True)
    target_right_extend_gap_score = db.Column(db.Integer, nullable=True)
    query_internal_open_gap_score = db.Column(db.Integer, nullable=True)
    query_internal_extend_gap_score = db.Column(db.Integer, nullable=True)
    query_left_open_gap_score = db.Column(db.Integer, nullable=True)
    query_left_extend_gap_score = db.Column(db.Integer, nullable=True)
    query_right_open_gap_score = db.Column(db.Integer, nullable=True)
    query_right_extend_gap_score = db.Column(db.Integer, nullable=True)
    creationDate = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __str__(self):
        return f"ID: {self.id}; \n 1st Sequence: {self.target} \n ; 2nd Sequence: {self.query}; \n"

    def __repr__(self):
        return f"ID: {self.id}; \n 1st Sequence: {self.target} \n ; 2nd Sequence: {self.query}; \n"
