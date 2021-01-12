from dataclasses import dataclass
from dataclasses_serialization.json import JSONSerializerMixin
from Bio.Seq import Seq


@dataclass
class Processed_protein(JSONSerializerMixin):
    protein: Seq = None
    protein_to_stop: Seq = None
    translation_table: str = None
    creation_date: str = None

    def seq_data(self):
        self.aa_count = {}
        for aa in "FLSYCWPHQRIMTNKVADEG*":
            self.aa_count[f"{aa}"] = self.protein.count(aa)
