from Bio import pairwise2, Align
from Bio.pairwise2 import format_alignment
from data_structures.alignment_list import Alignment, PriorityQueue
from model import Alignment_model


class Aligner():
    def __init__(self):
        raise Exception("This class isn't supposed to be among mere mortals")

    @staticmethod
    def align(id):

        object = Alignment_model.query.get(id).__dict__

        aligner = Align.PairwiseAligner()

        def set_scores():
            # checks which alignment type
            if object['alignment_type'] == "local":
                aligner.mode = 'local'

            elif object['alignment_type'] != "global":
                raise ValueError(
                    f"Alignment type {object['alignment_type']} asked is not available or does not exist")

            """
            Checks if a substitution matrix has been chosen
                if not it requires the match/mismatch score
            """
            if object['substitution_matrix']:
                from Bio.Align import substitution_matrices
                try:
                    aligner.substitution_matrix = substitution_matrices.load(
                        object['substitution_matrix'])
                except:
                    raise FileNotFoundError(
                        f"There's No {object['substitution_matrix']} matrix")

            elif not object['substitution_matrix']:
                aligner.match_score = object['match_score']
                aligner.mismatch_score = object['mismatch_score']

            else:
                raise ValueError(
                    f"Score schema must be 'LOCAL/GLOBAL' not {object['score-schema']}")

            if object['score_schema'] == 'simple':
                aligner.gap_score = object['gap_score']
            elif object['score_schema'] == 'complex':
                aligner.target_internal_open_gap_score = object['target_internal_open_gap_score']
                aligner.target_internal_extend_gap_score = object['target_internal_extend_gap_score']
                aligner.target_left_open_gap_score = object['target_left_open_gap_score']
                aligner.target_left_extend_gap_score = object['target_left_extend_gap_score']
                aligner.target_right_open_gap_score = object['target_right_open_gap_score']
                aligner.target_right_extend_gap_score = object['target_right_extend_gap_score']
                aligner.query_internal_open_gap_score = object['query_internal_open_gap_score']
                aligner.query_internal_extend_gap_score = object['query_internal_extend_gap_score']
                aligner.query_left_open_gap_score = object['query_left_open_gap_score']
                aligner.query_left_extend_gap_score = object['query_left_extend_gap_score']
                aligner.query_right_open_gap_score = object['query_right_open_gap_score']
                aligner.query_right_extend_gap_score = object['query_right_extend_gap_score']

        try:
            target = object['target_seq']
            query = object['query_seq']
            set_scores()
            pairwisealignments = aligner.align(target, query)
            alignments_list = [Aligner._format_generalized(
                alignment) for alignment in pairwisealignments]
            epsilon = aligner.epsilon
            algorithm = aligner.algorithm
            return epsilon, algorithm, alignments_list, None

        except Exception as err:

            return None, None, None, err

    # TODO REMAKE
    @staticmethod
    def parse_form(form):
        return Alignment_model(target_seq=form.get("target_seq"),
                               query_seq=form.get("query_seq"),
                               alignment_type=form.get("alignment_type"),
                               score_schema=form.get("score_schema"),
                               substitution_matrix=form.get(
                                   "substitution_matrix") if form.get(
                                   "substitution_matrix") != "" else None,
                               match_score=form.get("match_score"),
                               mismatch_score=form.get("mismatch_score"),
                               gap_score=form.get("gap_score"),
                               target_internal_open_gap_score=form.get(
                                   "target_internal_open_gap_score"),
                               target_internal_extend_gap_score=form.get(
                                   "target_internal_extend_gap_score"),
                               target_left_extend_gap_score=form.get(
                                   "target_left_extend_gap_score"),
                               target_left_open_gap_score=form.get(
                                   "target_left_open_gap_score"),
                               target_right_open_gap_score=form.get(
                                   "target_right_open_gap_score"),
                               target_right_extend_gap_score=form.get(
                                   "target_right_extend_gap_score"),
                               query_internal_open_gap_score=form.get(
                                   "query_internal_open_gap_score"),
                               query_internal_extend_gap_score=form.get(
                                   "query_internal_extend_gap_score"),
                               query_left_open_gap_score=form.get(
                                   "query_left_open_gap_score"),
                               query_left_extend_gap_score=form.get(
                                   "query_left_extend_gap_score"),
                               query_right_open_gap_score=form.get(
                                   "query_right_open_gap_score"),
                               query_right_extend_gap_score=form.get(
                                   "query_right_extend_gap_score")
                               )

    @staticmethod
    def manage_db(id):
        try:
            return Aligner.align(Alignment_model.query.get(id).__dict__)

        except Exception as err:
            return None, None, None, err

    @staticmethod
    def _format_generalized(alignment):
        seq1 = alignment.target
        seq2 = alignment.query
        n1 = len(seq1)
        n2 = len(seq2)
        aligned_seq1 = []
        aligned_seq2 = []
        pattern = []
        path = alignment.path
        end1, end2 = path[0]
        if end1 > 0 or end2 > 0:
            if end1 <= end2:
                for c2 in seq2[: end2 - end1]:
                    s2 = str(c2)
                    s1 = " " * len(s2)
                    aligned_seq1.append(s1)
                    aligned_seq2.append(s2)
                    pattern.append(s1)
            else:  # end1 > end2
                for c1 in seq1[: end1 - end2]:
                    s1 = str(c1)
                    s2 = " " * len(s1)
                    aligned_seq1.append(s1)
                    aligned_seq2.append(s2)
                    pattern.append(s2)
        start1 = end1
        start2 = end2
        for end1, end2 in path[1:]:
            if end1 == start1:
                for c2 in seq2[start2:end2]:
                    s2 = str(c2)
                    s1 = "-" * len(s2)
                    aligned_seq1.append(s1)
                    aligned_seq2.append(s2)
                    pattern.append(s1)
                start2 = end2
            elif end2 == start2:
                for c1 in seq1[start1:end1]:
                    s1 = str(c1)
                    s2 = "-" * len(s1)
                    aligned_seq1.append(s1)
                    aligned_seq2.append(s2)
                    pattern.append(s2)
                start1 = end1
            else:
                for c1, c2 in zip(seq1[start1:end1], seq2[start2:end2]):
                    s1 = str(c1)
                    s2 = str(c2)
                    m1 = len(s1)
                    m2 = len(s2)
                    if c1 == c2:
                        p = "|"
                    else:
                        p = "."
                    if m1 < m2:
                        space = (m2 - m1) * " "
                        s1 += space
                        pattern.append(p * m1 + space)
                    elif m1 > m2:
                        space = (m1 - m2) * " "
                        s2 += space
                        pattern.append(p * m2 + space)
                    else:
                        pattern.append(p * m1)
                    aligned_seq1.append(s1)
                    aligned_seq2.append(s2)
                start1 = end1
                start2 = end2
        aligned_seq1 = " ".join(aligned_seq1)
        aligned_seq2 = " ".join(aligned_seq2)
        pattern = " ".join(pattern)
        align_dict = {
            'target': aligned_seq1,
            'query': aligned_seq2,
            'pattern': pattern,
            'score': alignment.score,
            'path': path
        }
        return align_dict
