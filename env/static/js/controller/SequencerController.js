class SequencerController {
    constructor() {
        let $ = document.querySelector.bind(document)

        this.seqOutput = $("#seq-output")

        console.log(this.seqOutput.children)
        this.sequence = $("#sequence")
        this.translation_table = $("#translation_table")
        this.sequenceSpan = $("#sequence-span")
        this.postButton = $("#form-submit")

        this._checkboxes = [
            $('#coding-dna'),
            $('#dna-c'),
            $('#dna-rc'),
            $('#rna-m'),
            $('#rna-m-c'),
        ]

        this._regEx = new SequenceRegEx()
        if(this.seqOutput){
            this._sequencesView = new SequencesView(this.seqOutput)
            this._sequencesView.update(dataset)
        }

        this.dummieData1 = {
            "coding_dna": "ATCG",
            "dna_c": "TAGC",
            "dna_rc": "CGAT",
            "rna_m": "AUCG",
            "rna_m_c": "UAGC",
            "protein": "I",
            "protein_to_stop": "I",
            "translation_table": "1",
            "creation_date": "09/01/2021, 02:19:51",
            "dna_nucleotide_count": {
                "A": 1,
                "T": 1,
                "C": 1,
                "G": 1
            },
            "rna_nucleotide_count": {
                "A": 1,
                "U": 1,
                "C": 1,
                "G": 1
            },
            "aa_count": { "F": 0, "L": 0, "S": 0, "Y": 0, "C": 0, "W": 0, "P": 0, "H": 0, "Q": 0, "R": 0, "I": 1, "M": 0, "T": 0, "N": 0, "K": 0, "V": 0, "A": 0, "D": 0, "E": 0, "G": 0, "*": 0 }
        }

        this.dummieData2 = {
            "coding_dna": "ATCG",
            "dna_c": null,
            "dna_rc": null,
            "rna_m": null,
            "rna_m_c": null,
            "protein": null,
            "protein_to_stop": null,
            "translation_table": "1",
            "creation_date": "09/01/2021, 02:12:50",
            "dna_nucleotide_count": {
                "A": 1,
                "T": 1,
                "C": 1,
                "G": 1
            }
        }

        this.dummieData3 = {
            "protein": "ASIHHGNDANDIIADKAD",
            "protein_to_stop": "ASIHHGNDANDIIADKAD",
            "translation_table": "1",
            "creation_date": "09/01/2021, 23:49:21 UTC",
            "aa_count": {
                "F": 0, "L": 0, "S": 1, "Y": 0, "C": 0, "W": 0, "P": 0, "H": 2, "Q": 0, "R": 0, "I": 3, "M": 0, "T": 0, "N": 2,
                "K": 1, "V": 0, "A": 4, "D": 4, "E": 0, "G": 1, "*": 0
            }
        }
    }


    toggleTab(id){
        this._sequencesView.openCloseTab(id)
    }
    toggleDiv(id){
        this._sequencesView.openCloseDiv(id)
    }

    checkSequence() {

        this.sequence.value = this.sequence.value.replace(/\s\r\n|\n|\r/g, "")
        let sequence = this.sequence.value

        if (sequence == "") {

            this._validSequence()

        } else if (document.getElementById("dna-seq").checked) {
            if (!this._regEx.checkDNA(sequence)) {
                this._validSequence()

            } else {
                this._invalidSequence()

            }
        } else if (document.getElementById("rna-seq").checked) {
            if (!this._regEx.checkRNA(sequence)) {

                this._validSequence()

            } else {
                this._invalidSequence()

            }
        } else {

            let translation_table = this.translation_table.value

            if (!this._regEx.checkProtein(sequence, translation_table)) {
                this._validSequence()

            } else {
                this._invalidSequence()

            }
        }
    }

    _invalidSequence() {
        this.sequence.classList.add("seq-input-area-invalid")
        this.sequenceSpan.classList.remove("textarea-span")
        this.postButton.disabled = true
    }

    _validSequence() {
        this.sequence.classList.remove("seq-input-area-invalid")
        this.sequenceSpan.classList.add("textarea-span")
        this.postButton.disabled = false
    }

    disableDnaRnaCheckboxes() {
        this._checkboxes.forEach(checkbox => checkbox.disabled = true)
    }

    enableDnaRnaCheckboxes() {
        this._checkboxes.forEach(checkbox => checkbox.disabled = false)
    }
}