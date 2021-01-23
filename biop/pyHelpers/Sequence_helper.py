from model import Sequence_model
import json


class Sequence_Helper():
    def __init__(self):
        raise Exception("This class isn't supposed to be among mere mortals")

    @staticmethod
    def sequence_form(form):
        conversion_types = ['coding-dna', 'dna-c',
                            'dna-rc', 'rna-m', 'rna-m-c',  'protein', 'protein-to-stop']
        conversion_table = ""

        for conversion_type in conversion_types:
            if conversion_type in form:
                conversion_table += "1"
            else:
                conversion_table += "0"

        sequence_dict = {
            "seq_type": form["seq"],
            "sequence": form["sequence"],
            "conversions": conversion_table,
            "translation_table": form['translation-table']
        }
        return sequence_dict

    @staticmethod
    def parse_form(data_received):
        data_received = Sequence_Helper.sequence_form(data_received.to_dict())
        new_object = Sequence_model(seq_type=data_received["seq_type"],
                                    sequence=data_received["sequence"],
                                    translation_table=data_received["translation_table"]
                                    )
        return new_object

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

        return json.dumps(dna_data), json.dumps(rna_data), json.dumps(Sequence_Helper._extract_protein_data(object))

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
