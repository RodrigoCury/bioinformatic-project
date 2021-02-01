from model import Sequence_model
from project_dataclasses.Sequence_dataclass import DataBase_Sequence
from pyHelpers.Sequencer import Sequencer


class Sequence_Helper():
    def __init__(self):
        raise Exception("This class isn't supposed to be among mere mortals")

    @staticmethod
    def parse_form(data_received):
        return Sequence_model(seq_type=data_received["seq"],
                              sequence=data_received["sequence"],
                              translation_table=data_received["translation-table"]
                              )

    @staticmethod
    def manage_db(id):
        data = Sequence_model.query.get(id).__dict__

        # transform the data into a workable dataclass to process

        return Sequencer.manage_sequence(DataBase_Sequence(seq_id=data['id'],
                                                           sequence=data['sequence'],
                                                           seq_type=data['seq_type'],
                                                           translation_table=data['translation_table'],
                                                           creation_date=data['creationDate']))
