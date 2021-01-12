from model import Sequence_model


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
                                    conversions=data_received["conversions"],
                                    translation_table=data_received["translation_table"]
                                    )
        return new_object
