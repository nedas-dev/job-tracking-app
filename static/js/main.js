document.getElementById('sidebar-icon').addEventListener('click', (e) => {
    var sidebarLines = document.querySelector('span.side-bar-container').children
    if (sidebarLines[0].className == 'sidebar sidebar1') {
        sidebarLines[0].className = 'sidebar';
        sidebarLines[1].className = 'sidebar';
        sidebarLines[2].className = 'sidebar';
        document.querySelector('div.sidebar-container').style.transform = "translate(-200px)"
    }
    else {
        sidebarLines[0].className = 'sidebar sidebar1';
        sidebarLines[1].className = 'sidebar sidebar2';
        sidebarLines[2].className = 'sidebar sidebar3';
        document.querySelector('div.sidebar-container').style.transform = "translate(0px)"
    }



})