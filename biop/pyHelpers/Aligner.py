from Bio import pairwise2, Align
from Bio.pairwise2 import format_alignment
from data_structures.alignment_list import Alignment, PriorityQueue
from model import Alignment_model


class Aligner():
    def __init__(self):
        raise Exception("This class isn't supposed to be among mere mortals")

    @staticmethod
    def align(id):

        try:
            object = Alignment_model.query.get(id).__dict__

        except Exception as err:
            print(err)
            return None, err

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
            import json
            target = object['target_seq']
            query = object['query_seq']
            set_scores()
            pairwisealignments = aligner.align(target, query)
            alignment_list = Aligner.alignments_to_list(pairwisealignments)
            alignment_data = {
                "seq_type": object['seq_type'],
                "alignment_type": object['alignment_type'],
                "algorithm": str(aligner.algorithm),
                "alignment_list": alignment_list,
                "epsilon": str(aligner.epsilon),
                "score": pairwisealignments.score,
            }
            return json.dumps(alignment_data), None

        except Exception as err:
            return None, err

    @staticmethod
    def alignments_to_list(alignments):
        def format(alignment):
            return {
                "target": alignment.target,
                "query": alignment.query,
                "path": [list(p) for p in alignment.path]
            }
        try:
            if alignments[100]:
                print("TRY")
                return [format(alignments[i]) for i in range(100)]
        except:
            print("Except")
            return [format(
                    alignment) for alignment in alignments]

    # TODO REMAKE
    @staticmethod
    def parse_form(form):
        print(form.get("target_seq"))
        print(form.get("query_seq"))
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
