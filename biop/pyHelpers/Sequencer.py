from pyHelpers.Sequence_helper import Sequence_Helper
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
from project_dataclasses.Processed_dna_rna import Processed_dna_rna
from project_dataclasses.Processed_protein import Processed_protein


class Sequencer:
    def __init__(self):
        raise Exception(
            "Only a sorcerer can invoke this object. You are not a sorcerer!")

    @ staticmethod
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

        return Sequence_Helper.extract_sequence_data(treated_data)

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

        return Sequence_Helper.extract_sequence_data(treated_data)

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

        return Sequence_Helper.extract_sequence_data(treated_data)
