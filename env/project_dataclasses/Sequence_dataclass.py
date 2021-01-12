from dataclasses import dataclass
import datetime


@dataclass
class DataBase_Sequence():
    seq_id: int
    seq_type: str
    sequence: str
    conversions: str
    translation_table: str
    creation_date: datetime.datetime
