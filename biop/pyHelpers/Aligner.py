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

        try:
            if object['alignment_type'] == "local":
                aligner.mode = 'local'
                aligner.match_score = 1.0
                aligner.mismatch_score = -2.0
                aligner.gap_score = -2.5
                alignments_list = list(aligner.align(
                    object['seq1'], object['seq2']))
                # if len(alignments_list) > 10:
                #     return sorted(alignments_list)[:10], None
                return alignments_list, None

            elif object['alignment_type'] == "global":
                alignments_list = Aligner.convert_alignments_to_list(
                    pairwise2.align.globalms(object['seq1'], object['seq2'], 2, -1, -0.5, -0.1))
                # if len(alignments_list) > 10:
                #     return alignments_list[:10], None
                return alignments_list, None

            else:
                raise ValueError(
                    "Alignment_type asked is not avalilable or does not exist")

        except Exception as err:
            return None, err

        # try:
        #     if object['alignment_type'] == "local":
        #         alignments_list = Aligner.convert_alignments_to_list(
        #             pairwise2.align.localxx(object['seq1'], object['seq2']))
        #         return alignments_list, None

        #     elif object['alignment_type'] == "global":
        #         alignments_list = Aligner.convert_alignments_to_list(
        #             pairwise2.align.globalms(object['seq1'], object['seq2'], 2, -1, -0.5, -0.1))
        #         return alignments_list, None

        #     else:
        #         raise ValueError(
        #             "Alignment_type asked is not avalilable or does not exist")

        # except Exception as err:
        #     return None, err

    @staticmethod
    def convert_alignments_to_list(alignments):
        alignments_list = PriorityQueue()

        for alignment in alignments:
            seq1, align, seq2 = format_alignment(*alignment).split("\n")[:3]
            alignments_list.push(Alignment(seq1, align, seq2, alignment.score,
                                           alignment.start, alignment.end))

        return alignments_list

    @staticmethod
    def parse_form(form):
        return Alignment_model(seq1=form["seq1"],
                               seq2=form["seq2"],
                               alignment_type=form["align_type"])

    @staticmethod
    def manage_db(id):
        try:
            return Aligner.align(Alignment_model.query.get(id).__dict__)

        except Exception as err:
            return None, err
