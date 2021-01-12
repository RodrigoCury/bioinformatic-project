from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
from project_dataclasses.Processed_dna_rna import Processed_dna_rna
from project_dataclasses.Processed_protein import Processed_protein

import datetime


class Sequencer:
    def __init__(self):
        raise Exception(
            "Only a sorcerer can invoke this object. You are not a sorcerer!")

    @staticmethod
    def manage_dna(data):

        treated_data = Processed_dna_rna(
            creation_date=data.creation_date.strftime("%d/%m/%Y, %H:%M:%S"), translation_table=data.translation_table)

        sequence = Seq(data.sequence,  IUPAC.unambiguous_dna)

        if data.conversions[0] == "1":
            treated_data.coding_dna = str(sequence)

        if data.conversions[1] == "1":
            treated_data.dna_c = str(sequence.complement())

        if data.conversions[2] == "1":
            treated_data.dna_rc = str(sequence.reverse_complement())

        if data.conversions[3] == "1":
            treated_data.rna_m = str(sequence.transcribe())

        if data.conversions[4] == "1":
            treated_data.rna_m_c = str(sequence.complement().transcribe())

        if data.conversions[5] == "1":
            treated_data.protein = str(sequence.translate(
                table=data.translation_table))

        if data.conversions[6] == "1":
            treated_data.protein_to_stop = str(sequence.translate(
                table=data.translation_table, to_stop=True))

        return treated_data

    @staticmethod
    def manage_rna(data):
        treated_data = Processed_dna_rna(
            creation_date=data.creation_date.strftime("%d/%m/%Y, %H:%M:%S"), translation_table=data.translation_table)

        sequence = Seq(data.sequence,  IUPAC.unambiguous_rna)

        if data.conversions[0] == "1":
            treated_data.coding_dna = str(sequence.back_transcribe())

        if data.conversions[1] == "1":
            treated_data.dna_c = str(sequence.back_transcribe().complement())

        if data.conversions[2] == "1":
            treated_data.dna_rc = str(sequence.back_transcribe().complement())

        if data.conversions[3] == "1":
            treated_data.rna_m = str(sequence)

        if data.conversions[4] == "1":
            treated_data.rna_m_c = str(sequence.complement())

        if data.conversions[5] == "1":
            treated_data.protein = str(sequence.translate(
                table=data.translation_table))

        if data.conversions[6] == "1":
            treated_data.protein_to_stop = str(sequence.translate(
                table=data.translation_table, to_stop=True))

        return treated_data

    @staticmethod
    def manage_protein(data):
        treated_data = Processed_protein(
            creation_date=data.creation_date.strftime("%d/%m/%Y, %H:%M:%S UTC"), translation_table=data.translation_table)

        print(type(treated_data))

        sequence = Seq(data.sequence,  IUPAC.protein)

        data.conversions = data.conversions

        if data.conversions[5] == "1":
            treated_data.protein = str(sequence)

        if data.conversions[6] == "1" and "*" in sequence:
            sequence = sequence[0:sequence.find("*")]
            treated_data.protein_to_stop = str(sequence)
        elif data.conversions[6]:
            treated_data.protein_to_stop = str(sequence)

        return treated_data

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
