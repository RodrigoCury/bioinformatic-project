from flask import Flask, render_template, request, redirect, url_for

import datetime
import json

from model import db
from model import Sequence_model, Alignment_model
from pyHelpers.Sequence_helper import Sequence_Helper
from pyHelpers.Aligner import Aligner
from pyHelpers.Sequencer import Sequencer
from datetime import datetime


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

    if request.method == "POST":
        new_id, err = add_to_db(Sequence_Helper.parse_form(request.form))
        # TODO implement error message if unable adding sequence to db
        return redirect(url_for("genetic_translator", seq_id=new_id, add_to_db_error=err))

    elif seq_id:
        try:
            dna_data, rna_data, protein_data = Sequence_Helper.manage_db(
                seq_id)

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

        new_id, err = add_to_db(Aligner.parse_form(request.form))
        if err:
            print(err)
            return "NOT OKAY"
        return "OK, DB id = " + str(new_id)

    elif align_id:
        alignment_list, err = Aligner.align(align_id)
        if err:
            print(err)
            return str(err)
        lista = [al.__dict__ for al in alignment_list]
        return json.dumps(lista)

    else:
        pass

    if request.method == "POST":

        new_id, err = add_to_db(Aligner.parse_form(request.form))
        if err:
            return render_template("seq-alignment.html", err=err)
        return render_template("seq-alignment.html", align_id=new_id)

    elif align_id:
        alignment_list, err = Aligner.align(align_id)
        if err:
            return render_template("seq-alignment.html", err=err)
        lista = [al.__dict__ for al in alignment_list]
        return render_template("seq-alignment.html", alignment_list=lista)

    else:
        return render_template("seq-alignment.html")


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


def add_to_db(db_object):
    try:
        db.session.add(db_object)
        db.session.commit()

        # Return the object id to reload a new page and None to show no error messages
        return db_object.id, None

    except Exception as err:
        print("Failed to add to Database a new sequence")
        print(err)

        # Return no seq_id to reload a new page and True to show error messages on load
        return None, True
