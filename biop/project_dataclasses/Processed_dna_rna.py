from dataclasses import dataclass
from dataclasses_serialization.json import JSONSerializerMixin
from Bio.Seq import Seq


@dataclass
class Processed_dna_rna(JSONSerializerMixin):
    coding_dna: Seq = None
    dna_c: Seq = None
    dna_rc: Seq = None
    rna_m: Seq = None
    rna_m_c: Seq = None
    protein: Seq = None
    protein_to_stop: Seq = None
    translation_table: str = None
    creation_date: str = None

    def seq_data(self):

        if self.coding_dna or self.dna_c or self.dna_rc:
            for code in [self.coding_dna, self.dna_c, self.dna_rc]:
                if code:
                    self.dna_nucleotide_count = {}
                    for aa in "ATCG":
                        self.dna_nucleotide_count[f"{aa}"] = code.count(
                            aa)
                    break

        if self.rna_m or self.rna_m_c:
            for code in [self.rna_m, self.rna_m_c]:
                if code:
                    self.rna_nucleotide_count = {}
                    for aa in "AUCG":
                        self.rna_nucleotide_count[f"{aa}"] = code.count(aa)
                    break

        if self.protein or self.protein_to_stop:
            for code in [self.protein, self.protein_to_stop]:
                if code:
                    self.aa_count = {}
                    for aa in "FLSYCWPHQRIMTNKVADEG*":
                        self.aa_count[f"{aa}"] = code.count(aa)
                    break

    # def __dict__:
    # {"coding_dna": self.coding_dna,
    #  "dna_c": self.dna_c,
    #  "dna_rc": self.dna_rc,
    #  "rna_m": self.rna_m,
    #  "rna_m_c": self.rna_m_c,
    #  "protein": self.protein,
    #  "protein_to_stop": self.protein_to_stop,
    #  "translation_table": self.translation_table,
    #  "creation_date": self.creation_date
    #  }
