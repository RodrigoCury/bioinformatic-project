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
