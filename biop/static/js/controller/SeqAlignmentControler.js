class SeqAlignmentControler {
    constructor(alignmentList = null, epsilon = null, algorithm = null) {
        const $ = document.querySelector.bind(document)

        // divs
        this._alignmentTypeDiv = $("#alignment-type-div")
        this._scoreSchemaDiv = $("#score-schema-div")
        this._subMatrixProteinDiv = $("#substitution-matrix-protein-div")
        this._subMatrixDnaDiv = $("#substitution-matrix-dna-div")
        this._simpleScoreDiv = $("#simple-score-div")
        this._complexScoreDiv = $("#complex-score-div")

        //radios
        this._dnaSeq = $("#dna-seq")
        this._rnaSeq = $("#rna-seq")
        this._proteinSeq = $("#protein-seq")
        this._simpleScore = $("#simple-score")
        this._complexScore = $("#complex-score")

        //matrices
        this._subMatrixDna = $("#substitution-matrix-dna")
        this._subMatrixProtein = $("#substitution-matrix-protein")

        //match/mismatc_scores
        this._matchMismatchScore = document.querySelectorAll("#match-score, #mismatch-score")

        //Submit
        this.postButton = $("#form-submit")

        //SeqRegex

        this._seqRegEx = new SequenceRegEx()


        // if (alignmentList && epsilon && algorithm) {
        //     this._alignmentView = new AlignmentView("#alignments")
        //     this._alignmentView.update(alignmentList, epsilon, algorithm)
        // }
    }

    checkSequence(id) {

        let sequence = document.getElementById(id)
        let sequenceSpan = document.getElementById(`${id}-span`)
        let _invalidSequence = () => {
            sequence.classList.add("seq-input-area-invalid")
            sequenceSpan.classList.remove("textarea-span")
            this.postButton.disabled = true
        }

        let _validSequence = () => {
            sequence.classList.remove("seq-input-area-invalid")
            sequenceSpan.classList.add("textarea-span")
            this.postButton.disabled = false
        }

        sequence.value = sequence.value.replace(/\s\r\n|\n|\r/g, "")

        if (sequence.value == "") {

            _validSequence()

        } else if (document.getElementById("dna-seq").checked) {
            if (!this._seqRegEx.checkDNA(sequence.value)) {
                _validSequence()

            } else {
                _invalidSequence()

            }
        } else if (document.getElementById("rna-seq").checked) {
            if (!this._seqRegEx.checkRNA(sequence.value)) {

                _validSequence()

            } else {
                _invalidSequence()

            }
        } else {
            if (!this._seqRegEx.checkProteinAlign(sequence.value)) {
                _validSequence()

            } else {
                _invalidSequence()
            }
        }

    }

    onClickDNA(e) {
        this._subMatrixDnaDiv.classList.remove("none")
        this._subMatrixDna.disabled = false
        this._subMatrixDna.click()
        this._subMatrixProteinDiv.classList.add("none")
        this._subMatrixProtein.disabled = true
    }

    onClickRNA(e) {
        this._subMatrixDnaDiv.classList.add("none")
        this._subMatrixDna.disabled = true
        this._subMatrixProteinDiv.classList.add("none")
        this._subMatrixProtein.disabled = true
    }


    onClickProtein(e) {
        this._subMatrixDnaDiv.classList.add("none")
        this._subMatrixDna.disabled = true
        this._subMatrixProteinDiv.classList.remove("none")
        this._subMatrixProtein.disabled = false
        this._matchMismatchScore.forEach(child => {
            child.disabled = true
            child.classList.add("none")
        })
    }

    onClickSimple(e) {
        this._simpleScoreDiv.classList.remove("none")
        this._simpleScoreDiv.childNodes.forEach(child => child.disabled = false)
        this._complexScoreDiv.classList.add("none")
        this._complexScoreDiv.childNodes.forEach(child => child.disabled = true)
    }

    onClickComplex(e) {
        this._complexScoreDiv.classList.remove("none")
        this._complexScoreDiv.childNodes.forEach(child => child.disabled = false)
        this._simpleScoreDiv.classList.add("none")
        this._simpleScoreDiv.childNodes.forEach(child => child.disabled = true)
    }

    onChangeSubMatrixDNA(e) {
        if (this._subMatrixDna.value == ""
            || this._subMatrixDna.disabled == true
            && this._proteinSeq.checked == false) {
            this._matchMismatchScore.forEach(child => {
                child.disabled = false
                child.classList.remove("none")
            })
        } else {
            this._matchMismatchScore.forEach(child => {
                child.disabled = true
                child.classList.add("none")
            })
        }
    }
}