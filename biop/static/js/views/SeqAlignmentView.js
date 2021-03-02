class SeqAlignmentView extends View {

    constructor(element, data) {
        super(element);
        this._data = data
        this.update(0)
    }

    update(index) {
        let receivedData = this._formatter(this._data.alignment_list[index])
        let len = this._data.alignment_list.length + 1
        let template = `
        <div class="alignment-data">
            <table>
                <thead class="data-titles">
                    <tr class="tr-thead">
                        <th class="alignment-data-t">Algoritmo Usado</th>
                        <th class="alignment-data-t">Score</th>
                        <th class="alignment-data-t">Identidade</th>
                        <th class="alignment-data-t">Similaridade</td>
                        <th class="alignment-data-t">Epsilon</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="alignment-data-r">${this._data.algorithm}</td>
                        <td class="alignment-data-r">${this._data.score}</td>
                        <td class="alignment-data-r">${this._getSeqIdentidy(index)}</td>
                        <td class="alignment-data-r"></td>
                        <td class="alignment-data-r">${this._data.epsilon}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="alignment">
            <p style="font-family: monospace;">${receivedData.target}</p>
            <p style="font-family: monospace;">${receivedData.pattern}</p>
            <p style="font-family: monospace;">${receivedData.query}</p>
        </div>

        <div class="alignment-chooser">
            <div class="direct-choice">
                <input class="alignment-choice" id="direct-choice" name="direct-choice" type="number" min="1"
                    max="${len - 1}" value="${index + 1}" onkeypress="seqAlignmentControler.getItemSelector(event)">
                <label for="direct-choice">de ${len - 1}</label>
            </div>
            <div class="previous-next-choice">
                <button class="previous choice-submit"  ${index > 0 ? 'onclick="seqAlignmentControler.getItem(' + (index - 1).toString() + ')"' : "disabled"}>&#60;-</button>
                <p class="actual">${index + 1}</p>
                <button class="next choice-submit" ${index < len - 2 ? 'onclick="seqAlignmentControler.getItem(' + (index + 1).toString() + ')"' : "disabled"} >-&#62;</button>
            </div>
            <button class="csv">.CSV</button>
        </div>
        `
        this._ElementHTML.innerHTML = template
    }

    openCloseDiv(id) {

        let itens = document.getElementById(id).children
        document.querySelector(".form-parent-node-btn").classList.toggle("rotate")

        for (let i = 1; itens.length > i; i++) {
            itens[i].classList.toggle("hidden")
        }
    }

    _getSeqIdentidy(index) {
        let score = this._data.score
        let len = this._data.alignment_list[index]
            .query
            .length

        let similarity = (score / len * 100) == 100 ? 100 : (score / len * 100).toFixed(3)



        return `${similarity}%`
    }

    _formatter(seq) {
        let seq1 = seq.target
        let seq2 = seq.query
        let n1 = seq1.length
        let n2 = seq2.length
        let alignedSeq1 = ""
        let alignedSeq2 = ""
        let pattern = ""
        let path = seq.path
        let end1 = path[0][0]
        let end2 = path[0][1]
        if (end1 > 0 || end2 > 0) {
            let end = end1 >= end2 ? end1 : end2
            alignedSeq1 += ("&nbsp;".repeat(end - end1) + seq1.slice(0, end1))
            alignedSeq2 += ("&nbsp;".repeat(end - end2) + seq2.slice(0, end2))
            pattern += "&nbsp;".repeat(end)
        }
        let start1 = end1
        let start2 = end2
        for (let i = 1; i < path.length; i++) {
            end1 = path[i][0]
            end2 = path[i][1]
            let gap = 0
            if (end1 == start1) {
                gap = end2 - start2
                alignedSeq1 += "&#8209;".repeat(gap)
                alignedSeq2 += seq2.slice(start2, end2)
                pattern += "&#8209;".repeat(gap)
            } else if (end2 == start2) {
                gap = end1 - start1
                alignedSeq1 += seq1.slice(start1, end1)
                alignedSeq2 += "&#8209;".repeat(gap)
                pattern += "&#8209;".repeat(gap)
            } else {

                let s1 = seq1.slice(start1, end1)
                let s2 = seq2.slice(start2, end2)
                alignedSeq1 += s1
                alignedSeq2 += s2
                for (let c in s1) {
                    let c1 = s1[c]
                    let c2 = s2[c]
                    if (c1 == c2) {
                        pattern += "|"
                    } else {
                        pattern += "."
                    }
                }
            }
            start1 = end1
            start2 = end2
        }
        n1 -= end1
        n2 -= end2
        let n = n1 >= n2 ? n1 : n2
        console.log(n, n1)
        console.log(n, n2)
        alignedSeq1 += seq1.slice(end1, seq1.length) + "&nbsp;".repeat(n - n1)
        alignedSeq2 += seq2.slice(end2, seq2.length) + "&nbsp;".repeat(n - n2)
        pattern += "&nbsp;".repeat(n)
        let dict = {
            target: alignedSeq1,
            query: alignedSeq2,
            pattern: pattern
        }
        return dict
    }


}