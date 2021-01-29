from flask import Flask, render_template, request, redirect, url_for

import datetime
import json

from model import db
from model import Sequence_model
from pyHelpers.Sequence_helper import Sequence_Helper
from pyHelpers.Sequencer import Sequencer
from datetime import datetime
from project_dataclasses.Sequence_dataclass import DataBase_Sequence


def create_flask_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seq.db'
    db.init_app(app)
    app.app_context().push()
    app.url_map.strict_slashes = False
    return app


app = create_flask_app()


@app.context_processor
def inject_data():
    return {'today_date': str(datetime.utcnow())}


@app.route("/", methods=["GET", "POST"])
@app.route("/<int:seq_id>", methods=["GET", "POST"])
def genetic_translator(seq_id=None):

    def _add_to_db(req):
        try:
            data_received = req.form
            new_object = Sequence_Helper.parse_form(data_received)
            db.session.add(new_object)
            db.session.commit()

            # Return the object id to reload a new page and None to show no error messages
            return new_object.seq_id, None
        except Exception as e:
            print("Failed to add to Database a new sequence")
            print(e)
            # Return no seq_id to reload a new page and True to show error messages on load
            return None, True

    if request.method == "POST":
        new_id, err = _add_to_db(request)
        # TODO implement error message if unable adding sequence to db
        return redirect(url_for("genetic_translator", seq_id=new_id, add_to_db_error=err))

    elif seq_id:
        try:
            data = Sequence_model.query.get(seq_id).__dict__

            # transform the data into a workable dataclass to process
            data_to_process = DataBase_Sequence(seq_id=data['seq_id'],
                                                sequence=data['sequence'],
                                                seq_type=data['seq_type'],
                                                translation_table=data['translation_table'],
                                                creation_date=data['creationDate'])

            dna_data, rna_data, protein_data = Sequencer.manage_sequence(
                data_to_process)

            return render_template("genetic-translator.html",
                                   received=True, dna_data=dna_data, rna_data=rna_data, protein_data=protein_data)

        except Exception as e:
            print(e)
            print(f"Sequence ID '{seq_id}' is not on our database")
        # TODO implement on HTML message if seq_id is not on db
            return render_template("genetic-translator.html", seq_not_in_db=True)

    else:
        return render_template("genetic-translator.html")


@app.route("/seq_alignment", methods=["GET", "POST"])
@app.route("/seq_alignment/<int:align_id>", methods=["GET", "POST"])
def seq_alignment(align_id=None):
    if request.method == "POST":
        print("POST")
        try:
            test = json.dumps(request.form)
            return str(test)
        except Exception as e:
            return str(e)
    else:
        return "OK"


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
