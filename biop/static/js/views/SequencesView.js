class SequencesView extends View {

    constructor(element) {

        super(element);
        this._seq_div = ((key, value) => {
            return `
            <div class="seq-output-child" id="${key.toLowerCase().replaceAll(" ", '-').replace("'➡3'", "")}">
                <svg xmlns="http://www.w3.org/2000/svg" class="${key.replaceAll(" ", '-').replace("'➡3'", "").toLowerCase()}-btn" onclick='sequenceController.toggleTab("${key.toLowerCase().replaceAll(" ", '-').replace("'➡3'", "")}")' width="24" height="24" viewBox="0 0 24 24"><path d="M0 7.33l2.829-2.83 9.175 9.339 9.167-9.339 2.829 2.83-11.996 12.17z"/></svg>
                <h3 class="seq-header">${key}</h3>
                <p class="seq-text">${value}</p>
            </div>
             `
        })
    }

    update(dnaData, rnaData, proteinData) {
        let newTemplate = this.template(dnaData, rnaData, proteinData)
        this._ElementHTML.innerHTML = newTemplate;
        this.renderCanvas("dna-canvas", dnaData.dna_nucleotide_count)
        this.renderCanvas("rna-canvas", rnaData.rna_nucleotide_count)
        this.renderCanvas("protein-canvas", proteinData.aa_count)
    }

    template(dnaData, rnaData, proteinData) {
        let template = ``

        if (dnaData) {
            let dnaTemplate = `
                <div class='seq-output' id="dna-div">
                    <svg xmlns="http://www.w3.org/2000/svg" class="dna-div-btn" onclick='sequenceController.toggleDiv("dna-div")' width="24" height="24" viewBox="0 0 24 24"><path d="M0 7.33l2.829-2.83 9.175 9.339 9.167-9.339 2.829 2.83-11.996 12.17z"/></svg>
                    <h2 class='seq-output-title'>DNA</h2>
                    <div class="seq-output-child" id="coding-dna">
                        <svg xmlns="http://www.w3.org/2000/svg" class="coding-dna-btn" onclick='sequenceController.toggleTab("coding-dna")' width="24" height="24" viewBox="0 0 24 24"><path d="M0 7.33l2.829-2.83 9.175 9.339 9.167-9.339 2.829 2.83-11.996 12.17z"/></svg>
                        <h3 class="seq-header">DNA Codificante</h3>
                        <p class="seq-text">${dnaData.coding_dna}</p>
                    </div>
                    <div class="seq-output-child" id="dna-c">
                        <svg xmlns="http://www.w3.org/2000/svg" class="dna-c-btn" onclick='sequenceController.toggleTab("dna-c")' width="24" height="24" viewBox="0 0 24 24"><path d="M0 7.33l2.829-2.83 9.175 9.339 9.167-9.339 2.829 2.83-11.996 12.17z"/></svg>
                        <h3 class="seq-header">Fita Complementar</h3>
                        <p class="seq-text">${dnaData.dna_c}</p>
                    </div>
                    <div class="seq-output-child" id="dna-c-r">
                        <svg xmlns="http://www.w3.org/2000/svg" class="dna-c-r-btn" onclick='sequenceController.toggleTab("dna-c-r")' width="24" height="24" viewBox="0 0 24 24"><path d="M0 7.33l2.829-2.83 9.175 9.339 9.167-9.339 2.829 2.83-11.996 12.17z"/></svg>
                        <h3 class="seq-header">Fita Complementar 5' > 3'</h3>
                        <p class="seq-text">${dnaData.dna_rc}</p>
                    </div>
                    <canvas height="15%" width="100%" id="dna-canvas"></canvas>
                    <div class="seq-table-div">
                        <table class="seq-table">
                            <tbody>
                                <tr>
                                    <td>Densidate de GC</td>
                                    <td>${dnaData.gc_count.toFixed(2)}%</td>
                                </tr>
                                <tr>
                                    <td>Densidate de AT</td>
                                    <td>${dnaData.at_count.toFixed(2)}%</td>
                                </tr>
                                <tr>
                                    <td>Temperatura de anelamento</td>
                                    <td>${dnaData.mt.toFixed(2)}°C</td>
                                </tr>
                                <tr>
                                    <td colspan="2" style="text-align:center; font-weight:bold;">Peso Molecular</td>
                                </tr>
                                <tr>
                                    <td>Fita simples</td>
                                    <td>${dnaData.single_strand_molecular_weight.toFixed(2)} U</td>
                                </tr>
                                <tr>
                                    <td>Fita Dupla</td>
                                    <td>${dnaData.double_strand_molecular_weight.toFixed(2)} U</td>
                                </tr>
                                <tr>
                                    <td>Fita Simples Circular</td>
                                    <td>${dnaData.circular_single_strand_molecular_weight.toFixed(2)} U</td>
                                </tr>
                                <tr>
                                    <td>Fita Dupla Circular</td>
                                    <td>${dnaData.circular_double_strand_molecular_weight.toFixed(2)} U</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            `
            template += dnaTemplate
        }
        if (rnaData) {
            let rnaTemplate = `
                <div class='seq-output' id="rna-div">
                    <svg xmlns="http://www.w3.org/2000/svg" class="rna-div-btn" onclick='sequenceController.toggleDiv("rna-div")' width="24" height="24" viewBox="0 0 24 24"><path d="M0 7.33l2.829-2.83 9.175 9.339 9.167-9.339 2.829 2.83-11.996 12.17z"/></svg>
                    <h2 class='seq-output-title'>RNA</h2>
                    <div class="seq-output-child" id="rna-m">
                        <svg xmlns="http://www.w3.org/2000/svg" class="rna-m-btn" onclick='sequenceController.toggleTab("rna-m")' width="24" height="24" viewBox="0 0 24 24"><path d="M0 7.33l2.829-2.83 9.175 9.339 9.167-9.339 2.829 2.83-11.996 12.17z"/></svg>
                        <h3 class="seq-header">RNA Mensageiro</h3>
                        <p class="seq-text">${rnaData.rna_m}</p>
                    </div>
                    <div class="seq-output-child" id="rna-c">
                        <svg xmlns="http://www.w3.org/2000/svg" class="rna-c-btn" onclick='sequenceController.toggleTab("rna-c")' width="24" height="24" viewBox="0 0 24 24"><path d="M0 7.33l2.829-2.83 9.175 9.339 9.167-9.339 2.829 2.83-11.996 12.17z"/></svg>
                        <h3 class="seq-header">Fita Complementar</h3>
                        <p class="seq-text">${rnaData.rna_m_c}</p>
                    </div>

                    <canvas height="15%" width="100%" id="rna-canvas"></canvas>
                    <div class="seq-table-div">
                        <table class="seq-table">
                            <tbody>
                                <tr>
                                    <td>Densidate de GC</td>
                                    <td>${rnaData.gc_count.toFixed(2)}%</td>
                                </tr>
                                <tr>
                                    <td>Densidate de AU</td>
                                    <td>${rnaData.au_count.toFixed(2)}%</td>
                                </tr>
                                <tr>
                                    <td>Temperatura de anelamento</td>
                                    <td>${rnaData.mt.toFixed(2)}°C</td>
                                </tr>
                                <tr>
                                    <td colspan="2" style="text-align:center; font-weight:bold;">Peso Molecular</td>
                                </tr>
                                <tr>
                                    <td>Fita simples</td>
                                    <td>${rnaData.single_strand_molecular_weight.toFixed(2)} U</td>
                                </tr>
                                <tr>
                                    <td>Fita Dupla</td>
                                    <td>${rnaData.double_strand_molecular_weight.toFixed(2)} U</td>
                                </tr>
                                <tr>
                                    <td>Fita Simples Circular</td>
                                    <td>${rnaData.circular_single_strand_molecular_weight.toFixed(2)} U</td>
                                </tr>
                                <tr>
                                    <td>Fita Dupla Circular</td>
                                    <td>${rnaData.circular_double_strand_molecular_weight.toFixed(2)} U</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            `
            template += rnaTemplate
        }
        if (proteinData) {
            let proteinTemplate = `
                    <div class='seq-output' id="protein-div">
                        <svg xmlns="http://www.w3.org/2000/svg" class="protein-div-btn" onclick='sequenceController.toggleDiv("protein-div")' width="24" height="24" viewBox="0 0 24 24"><path d="M0 7.33l2.829-2.83 9.175 9.339 9.167-9.339 2.829 2.83-11.996 12.17z"/></svg>
                        <h2 class='seq-output-title'>Proteína</h2>
                        <div class="seq-output-child" id="frame1">
                            <svg xmlns="http://www.w3.org/2000/svg" class="frame1-btn" onclick='sequenceController.toggleTab("frame1")' width="24" height="24" viewBox="0 0 24 24"><path d="M0 7.33l2.829-2.83 9.175 9.339 9.167-9.339 2.829 2.83-11.996 12.17z"/></svg>
                            <h3 class="seq-header">Proteína Frame 1</h3>
                            <p class="seq-text">${proteinData.frame1}</p>
                        </div>
                        <div class="seq-output-child" id="frame2">
                            <svg xmlns="http://www.w3.org/2000/svg" class="frame2-btn" onclick='sequenceController.toggleTab("frame2")' width="24" height="24" viewBox="0 0 24 24"><path d="M0 7.33l2.829-2.83 9.175 9.339 9.167-9.339 2.829 2.83-11.996 12.17z"/></svg>
                            <h3 class="seq-header">Proteína Frame 2</h3>
                            <p class="seq-text">${proteinData.frame2}</p>
                        </div>
                        <div class="seq-output-child" id="frame2">
                            <svg xmlns="http://www.w3.org/2000/svg" class="frame2-btn" onclick='sequenceController.toggleTab("frame2")' width="24" height="24" viewBox="0 0 24 24"><path d="M0 7.33l2.829-2.83 9.175 9.339 9.167-9.339 2.829 2.83-11.996 12.17z"/></svg>
                            <h3 class="seq-header">Proteína Frame 3</h3>
                            <p class="seq-text">${proteinData.frame3}</p>
                        </div>
                        <canvas height="15%" width="100%" id="protein-canvas"></canvas>
                        <div class="seq-table-div">
                            <table class="seq-table">
                                <tbody>
                                    <tr>
                                        <td colspan="2" style="text-align:center; font-weight:bold;">Peso Molecular</td>
                                    </tr>
                                    <tr>
                                        <td>Frame 1</td>
                                        <td>${proteinData.molecular_weight_f1.toFixed(2)} U</td>
                                    </tr>
                                    <tr>
                                        <td>Frame 2</td>
                                        <td>${proteinData.molecular_weight_f2.toFixed(2)} U</td>
                                    </tr>
                                    <tr>
                                        <td>Frame 3</td>
                                        <td>${proteinData.molecular_weight_f3.toFixed(2)} U</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                `
            template += proteinTemplate
        }



        return template;
    }


    _template(model) {
        let dictParser = objeto => Object.entries(objeto)

        let template = ``
        let sequences = [{
            "DNA": {
                'DNA Codificante': model.coding_dna,
                'DNA Complementar': model.dna_c,
                "DNA Complementar 5'➡3'": model.dna_rc
            }
        },
        {
            "RNA": {
                'RNA Mensageiro': model.rna_m,
                'RNA Mensageiro Complementar': model.rna_m_c
            }
        },
        {
            "Proteína": {
                "Proteína": model.protein,
                "Proteína até o Stop Códon": model.protein_to_stop
            }
        }]

        let counts = {
            "DNA": model.dna_nucleotide_count,
            "RNA": model.rna_nucleotide_count,
            "Proteína": model.aa_count
        }

        let id = {}


        dictParser(sequences).forEach(([key, sequencetype]) => {

            template += ``

            dictParser(sequencetype).forEach(([key, seq]) => {
                if (Object.entries(seq).some(el => el != null)) {

                    let idKey = key.toLowerCase().replaceAll(" ", '-') + "-canvas"

                    console.log(typeof key)


                    id[idKey] = counts[key]

                    template += `
                                
                                `

                    dictParser(seq).forEach(([key, value]) => value != null ? template += this._seq_div(key, value) : "")

                    template += `<canvas height="15%" width="100%" id="${key.toLowerCase().replaceAll(" ", '-')}-canvas"></canvas>`
                }
            })


            template += "</div>"
        })

        return [template, id]
    }

    openCloseTab(id) {
        let item = document.getElementById(id).children
        item[2].classList.toggle("seq-text")
        item[2].classList.toggle("seq-text-open")
    }

    openCloseDiv(id) {

        let itens = document.getElementById(id).children

        for (let i = 3; itens.length > i; i++) {
            itens[i].classList.toggle("none")
        }
    }

    renderCanvas(id, data) {

        var ctx = document.getElementById(id).getContext('2d');

        let chartTitle = this.chartTitle(id)

        let xs = []
        let ys = []
        let backgroundColor = []
        let borderColor = []

        Object.entries(data).forEach(([key, value]) => {
            xs.push(key)
            ys.push(value)
            backgroundColor.push(this.randomColors())
            borderColor.push(this.randomColors() + "0.2")
        })

        const myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: xs,
                datasets: [{
                    label: chartTitle,
                    data: ys,
                    backgroundColor: backgroundColor,
                    borderColor: borderColor,
                    borderWidth: 1
                }]
            },
            options: {
                maintainAspectRatio: true,
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                },
            }
        });

    }

    chartTitle(id) {
        if (id == "dna-canvas" || id == "rna-canvas") return "Nucleotídeos"
        if (id == "protein-canvas") return "Aminoácidos"
    }

    randomColors() {
        let r = Math.floor(Math.random() * 255)
        let g = Math.floor(Math.random() * 255)
        let b = Math.floor(Math.random() * 255)
        return `rgba(${r},${g},${b})`
    }
}