from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
from project_dataclasses.Processed_dna_rna import Processed_dna_rna
from project_dataclasses.Processed_protein import Processed_protein

import json


class Sequencer:
    def __init__(self):
        raise Exception(
            "Only a sorcerer can invoke this object. You are not a sorcerer!")

    @staticmethod
    def manage_sequence(data):
        if data.seq_type == "dna-seq":
            return Sequencer.manage_dna(data)
        elif data.seq_type == "rna-seq":
            return Sequencer.manage_rna(data)
        elif data.seq_type == "protein-seq":
            return Sequencer.manage_protein(data)
        else:
            raise ValueError(
                "Sequence Type provided by the database is not correct")

    @staticmethod
    def manage_dna(data):

        sequence = Seq(data.sequence,  IUPAC.unambiguous_dna)

        treated_data = Processed_dna_rna(
            creation_date=data.creation_date.strftime("%d/%m/%Y, %H:%M:%S"),
            translation_table=data.translation_table,
            coding_dna=str(sequence),
            dna_c=str(sequence.complement()),
            dna_rc=str(sequence.reverse_complement()),
            rna_m=str(sequence.transcribe()),
            rna_m_c=str(sequence.complement().transcribe()),
            protein=str(sequence.translate(
                table=data.translation_table)),
            protein_to_stop=str(sequence.translate(
                table=data.translation_table, to_stop=True))
        )

        return Sequencer.extract_sequence_data(treated_data)

    @staticmethod
    def manage_rna(data):
        sequence = Seq(data.sequence,  IUPAC.unambiguous_rna)

        treated_data = Processed_dna_rna(
            creation_date=data.creation_date.strftime("%d/%m/%Y, %H:%M:%S"),
            translation_table=data.translation_table,

            coding_dna=str(sequence.back_transcribe()),
            dna_c=str(sequence.back_transcribe().complement()),
            dna_rc=str(sequence.back_transcribe().reverse_complement()),
            rna_m=str(sequence),
            rna_m_c=str(sequence.complement()),
            protein=str(sequence.translate(
                table=data.translation_table)),
            protein_to_stop=str(sequence.translate(
                table=data.translation_table, to_stop=True))
        )

        return Sequencer.extract_sequence_data(treated_data)

    @staticmethod
    def manage_protein(data):

        sequence = Seq(data.sequence,  IUPAC.protein)

        treated_data = Processed_protein(
            creation_date=data.creation_date.strftime(
                "%d/%m/%Y, %H:%M:%S UTC"),
            translation_table=data.translation_table,
            protein=str(sequence),
            protein_to_stop=str(
                sequence) if "*" not in sequence else sequence[0:sequence.find("*")]
        )

        return Sequencer.extract_sequence_data(treated_data)

    @staticmethod
    def extract_sequence_data(object):
        from Bio.SeqUtils import GC, molecular_weight
        from Bio.SeqUtils import MeltingTemp as mt

        try:
            dna_data = {
                'coding_dna': str(object.coding_dna).upper(),
                'dna_c': str(object.dna_c).upper(),
                'dna_rc': str(object.dna_rc).upper(),
                'dna_nucleotide_count': {},
                'gc_count': GC(object.coding_dna),
                'at_count': 100 - GC(object.coding_dna),
                'mt': mt.Tm_NN(object.coding_dna),
                'single_strand_molecular_weight': molecular_weight(object.coding_dna, circular=False, double_stranded=False, seq_type="DNA"),
                'double_strand_molecular_weight': molecular_weight(object.coding_dna, circular=False, double_stranded=True, seq_type="DNA"),
                'circular_single_strand_molecular_weight': molecular_weight(object.coding_dna, circular=True, double_stranded=False, seq_type="DNA"),
                'circular_double_strand_molecular_weight': molecular_weight(object.coding_dna, circular=True, double_stranded=True, seq_type="DNA"),
            }
            for aa in "ATCG":
                dna_data['dna_nucleotide_count'][f"{aa}"] = object.coding_dna.count(
                    aa)
        except Exception as e:
            print(e)
            dna_data = None

        try:
            rna_data = {
                'rna_m': str(object.rna_m).upper(),
                'rna_m_c': str(object.rna_m_c).upper(),
                'rna_nucleotide_count': {},
                'gc_count': GC(object.rna_m),
                'au_count': 100 - GC(object.rna_m),
                'mt': mt.Tm_NN(object.rna_m),
                'single_strand_molecular_weight': molecular_weight(object.rna_m, circular=False, double_stranded=False, seq_type="RNA"),
                'double_strand_molecular_weight': molecular_weight(object.rna_m, circular=False, double_stranded=True, seq_type="RNA"),
                'circular_single_strand_molecular_weight': molecular_weight(object.rna_m, circular=True, double_stranded=False, seq_type="RNA"),
                'circular_double_strand_molecular_weight': molecular_weight(object.rna_m, circular=True, double_stranded=True, seq_type="RNA"),
            }
            for aa in "AUCG":
                rna_data['rna_nucleotide_count'][f"{aa}"] = object.rna_m.count(
                    aa)
        except Exception as e:
            print(e)
            rna_data = None

        return json.dumps(dna_data), json.dumps(rna_data), json.dumps(Sequencer._extract_protein_data(object))

    @staticmethod
    def _extract_protein_data(object):
        try:
            from Bio.SeqUtils import molecular_weight
            from Bio.Seq import Seq

            protein_data = {
                'frame1': str(object.protein).upper(),
                'aa_count': {},
                'molecular_weight_f1': molecular_weight(object.protein.upper().replace("*", ""), seq_type="protein"),
            }

            for aa in "FLSYCWPHQRIMTNKVADEG*":
                protein_data['aa_count'][f"{aa}"] = object.protein.count(aa)

            try:
                new_sequence = Seq(object.coding_dna)
                protein_data['frame2'] = str(new_sequence[1:].translate(
                    object.translation_table))
                protein_data['molecular_weight_f2'] = molecular_weight(
                    protein_data["frame2"].replace("*", ""), seq_type="protein")
                protein_data['frame3'] = str(new_sequence[2:].translate(
                    object.translation_table))
                protein_data['molecular_weight_f3'] = molecular_weight(
                    protein_data["frame3"].replace("*", ""), seq_type="protein")

            except:
                pass

        except Exception as e:
            print(e)
            protein_data = None

        return protein_data
