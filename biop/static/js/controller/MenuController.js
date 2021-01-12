class MenuController {
    constructor() {

        let $ = document.querySelector.bind(document)

        this._menuButton = $("#menubtn")
        this._menuSidebar = $("#sidebar")
        this._logoUFU = $("#logo-ufu")
        this._sidebarFooter = $("#h-footer")
        this._siteTools = $("#site-tools")
        this._main = $("main")
    }

    hideShowMenu(event) {
        this._menuSidebar.classList.toggle("sidebar-closed")
        this._menuSidebar.classList.toggle("sidebar-open")
        this._main.classList.toggle("main-closed")
        this._main.classList.toggle("main-open")
        this._siteTools.classList.toggle("site-tools-closed")
        this._siteTools.classList.toggle("site-tools-open")
        this._sidebarFooter.classList.toggle("h-footer-closed")
        this._sidebarFooter.classList.toggle("h-footer-open")
    }
}
