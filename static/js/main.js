class WebsiteControler {
    constructor() {
        this.sidebarActive = false
    }
}

const sidebarLines = document.querySelector('span.side-bar-container').children;
const sidebarContainer = document.querySelector('div.sidebar-container');
const mainContent = document.getElementById('content');
const websiteController = new WebsiteControler();


const closeSidebar = function () {
    sidebarLines[0].className = 'sidebar';
    sidebarLines[1].className = 'sidebar';
    sidebarLines[2].className = 'sidebar';
    sidebarContainer.style.transform = "translate(-200px)";

    websiteController.sidebarActive = false
}

const openSidebar = function () {
    sidebarLines[0].className = 'sidebar sidebar1';
    sidebarLines[1].className = 'sidebar sidebar2';
    sidebarLines[2].className = 'sidebar sidebar3';
    sidebarContainer.style.transform = "translate(0px)"

    websiteController.sidebarActive = true

    // { 'once': true} - run event listener given function exactly once and then stop tracking the event (remove event)
    mainContent.addEventListener('click', (e) => {
        closeSidebar()
    }, { 'once': true })

}

// This code is responsible for opening and closing sidebar.
document.getElementById('sidebar-icon').addEventListener('click', (e) => {
    if (websiteController.sidebarActive) {
        closeSidebar()
    }
    else {
        openSidebar()
    }
})
