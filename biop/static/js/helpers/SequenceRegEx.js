class SequenceRegEx {
    constructor() {
        this._regexDNA = /^[ATCG]+$/i
        this._regexRNA = /^[AUCG]+$/i
        this._regexProtein = {
            '1': /^[FLSY*CWPHQRIMTNKVADEG]+$/i,
            '2': /^[FLSY*CWPHQRIMTNKVADEG]+$/i,
            '3': /^[FLSY*CWTPHQRIMNKVADEG]+$/i,
            '4': /^[FLSY*CWPHQRIMTNKVADEG]+$/i,
            '5': /^[FLSY*CWPHQRIMTNKVADEG]+$/i,
            '9': /^[FLSY*CWPHQRIMTNKVADEG]+$/i,
            '10': /^[FLSY*CWPHQRIMTNKVADEG]+$/i,
            '11': /^[FLSY*CWPHQRIMTNKVADEG]+$/i,
            '12': /^[FLSY*CWPHQRIMTNKVADEG]+$/i,
            '13': /^[FLSY*CWPHQRIMTNKGVADE]+$/i,
            '14': /^[FLSY*CWPHQRIMTNKVADEG]+$/i,
            '16': /^[FLSY*CWPHQRIMTNKVADEG]+$/i,
            '21': /^[FLSY*CWPHQRIMTNKVADEG]+$/i,
            '22': /^[FLS*YCWPHQRIMTNKVADEG]+$/i,
            '23': /^[F*LSYCWPHQRIMTNKVADEG]+$/i,
            '24': /^[FLSY*CWPHQRIMTNKVADEG]+$/i,
            '25': /^[FLSY*CGWPHQRIMTNKVADE]+$/i,
            '26': /^[FLSY*CWAPHQRIMTNKVDEG]+$/i,
            '27': /^[FLSYQCWPHRIMTNKVADEG]+$/i,
            '28': /^[FLSYQCWPHRIMTNKVADEG]+$/i,
            '29': /^[FLSYC*WPHQRIMTNKVADEG]+$/i,
            '30': /^[FLSYEC*WPHQRIMTNKVADG]+$/i,
            '31': /^[FLSYECWPHQRIMTNKVADG]+$/i,
            '33': /^[FLSY*CWPHQRIMTNKVADEG]+$/i
        }
    }

    checkDNA(sequence) {
        return !this._regexDNA.test(sequence)
    }

    checkRNA(sequence) {
        return !this._regexRNA.test(sequence)
    }

    checkProtein(sequence, translationTable) {
        return !this._regexProtein[translationTable].test(sequence)
    }

    checkProteinAlign(sequence) {
        return !this._regexProtein['1'].test(sequence)
    }
}