# coding=<utf-8>

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime
import json

from model import configure as config_db
from model import Sequence_model
from pyHelpers.Sequence_helper import Sequence_Helper
from pyHelpers.Sequencer import Sequencer
from datetime import datetime
from project_dataclasses.Sequence_dataclass import DataBase_Sequence
from dataclasses_serialization.json import JSONSerializer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seq.db'
config_db(app)
app.url_map.strict_slashes = False


@app.context_processor
def inject_data():
    return {'today_date': str(datetime.utcnow())}


@app.route("/", methods=["GET", "POST"])
@app.route("/<int:seq_id>", methods=["GET", "POST"])
def index(seq_id=None):

    if request.method == "POST":
        data_received = request.form
        new_object = Sequence_Helper.parse_form(data_received)
        app.db.session.add(new_object)
        app.db.session.commit()

        print(url_for("/", seq_id=new_object.seq_id))

        return redirect(url_for("/", seq_id=new_object.seq_id))

    elif seq_id:
        data = Sequence_model.query.get(seq_id)
        if not data:
            return render_template("index.html")

        data = data.__dict__
        data_to_process = DataBase_Sequence(seq_id=data['seq_id'],
                                            sequence=data['sequence'],
                                            seq_type=data['seq_type'],
                                            conversions=data['conversions'],
                                            translation_table=data['translation_table'],
                                            creation_date=data['creationDate'])

        processed_data = Sequencer.manage_sequence(data_to_process)
        processed_data.seq_data()

        return render_template("index.html",
                               data=json.dumps(processed_data.as_json()))

    else:
        return render_template("index.html")


@app.route("/deletedb", methods=["POST", "GET"])
def deletdb():
    if request.method == "POST":
        password = request.form["password"]
        if password == "debunkthatshit":
            all_sequences = Sequence_model.query.all()
            if all_sequences:
                for seq in all_sequences:
                    app.db.session.delete(seq)
        app.db.session.commit()
        return "Done"
    else:
        return render_template("deletedb.html")


if __name__ == "__main__":
    app.run(debug=True)
