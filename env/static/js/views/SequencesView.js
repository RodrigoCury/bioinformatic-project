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

    update(model) {
        let newTemplate = this.template(model)
        this._ElementHTML.innerHTML = newTemplate[0];
        console.log(newTemplate[1])
        Object.entries(newTemplate[1]).forEach(([key, value]) => this.renderCanvas(key, value))
    }

    template(model) {
        let dictParser = objeto => Object.entries(objeto)

        let template = ``
        let sequences = [{ "DNA": { 'DNA Codificante': model.coding_dna,
                                    'DNA Complementar': model.dna_c, 
                                    "DNA Complementar 5'➡3'": model.dna_rc } },
                        { "RNA": { 'RNA Mensageiro': model.rna_m, 
                                    'RNA Mensageiro Complementar': model.rna_m_c } },
                        { "Proteína": { "Proteína": model.protein, 
                                        "Proteína até o Stop Códon": model.protein_to_stop } }]
        
        let counts = {
            "DNA" : model.dna_nucleotide_count,
            "RNA" : model.rna_nucleotide_count,
            "Proteína" : model.aa_count
        }

        let id = {}


        dictParser(sequences).forEach(([key, sequencetype]) => {

            template += `<div class='seq-output' `

            dictParser(sequencetype).forEach(([key, seq]) => {
                if (Object.entries(seq).some(el => el != null)) {

                    let idKey = key.toLowerCase().replaceAll(" ", '-') + "-canvas"

                    console.log(typeof key)


                    id[idKey] = counts[key]

                    template += `
                                id="${key.toLowerCase()}-div">
                                <svg xmlns="http://www.w3.org/2000/svg" class="${key.toLowerCase()}-div-btn" onclick='sequenceController.toggleDiv("${key.toLowerCase()}-div")' width="24" height="24" viewBox="0 0 24 24"><path d="M0 7.33l2.829-2.83 9.175 9.339 9.167-9.339 2.829 2.83-11.996 12.17z"/></svg>
                                <h2 class='seq-output-title'>${key}</h2>
                                `
                    
                    dictParser(seq).forEach(([key, value]) => value != null ? template += this._seq_div(key, value) : "")
                    
                    template += `<canvas height="15%" width="100%" id="${key.toLowerCase().replaceAll(" ", '-')}-canvas"></canvas>`
                }
            })


            template += "</div>"
        })

        return [template, id]
    }

    openCloseTab(id){
        let item =  document.getElementById(id).children
        item[2].classList.toggle("seq-text")
        item[2].classList.toggle("seq-text-open")
    }

    openCloseDiv(id){

        let itens =  document.getElementById(id).children

        console.log(itens)

        for (let i= 3; itens.length > i ; i++){
            itens[i].classList.toggle("none")
        }
    }

    renderCanvas(id, data){

        var ctx = document.getElementById(id).getContext('2d');

        let chartTitle = this.chartTitle(id)

        let xs = []
        let ys = []
        let backgroundColor = []
        let borderColor = []
        

        console.log(data)

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
        if (id == "proteína-canvas") return "Aminoácidos"
    }

    randomColors(){
        let r = Math.floor(Math.random()* 255)
        let g = Math.floor(Math.random()* 255)
        let b = Math.floor(Math.random()* 255)
        return `rgba(${r},${g},${b})`
    }
}