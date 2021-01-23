class View {
    constructor(element) {
        this._ElementHTML = element
    }

    template() {

        throw new Error('Template needs another Vision Sorcerer to be able to be invoked, someone like Lord SequencesView.js');
    }

    update(model) {
        this._ElementHTML.innerHTML = this.template(model);
    }


}