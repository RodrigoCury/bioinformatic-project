class SequencerController {
    constructor(dnaData = null, rnaData = null, proteinData = null) {
        let $ = document.querySelector.bind(document)

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

        if (dnaData || rnaData || proteinData) {
            this._sequencesView = new SequencesView($('#seq-output'))
            this._sequencesView.update(dnaData, rnaData, proteinData)
        }

    }


    toggleTab(id) {
        this._sequencesView.openCloseTab(id)
    }
    toggleDiv(id) {
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
}