// HOME PAGE JS SCRIPT
const createEventFormFieldList = document.querySelectorAll('div.field');

// In case of error messages setting input's border to color RED so the customer could see which input is wrong.
if (createEventFormFieldList) {
    for (let i = 0; i < createEventFormFieldList.length; i++) {
        let fieldChildren = createEventFormFieldList[i].children;
        let errorDiv = fieldChildren[0]
        let inputDiv = fieldChildren[2]
        if (errorDiv.children.length > 0) {
            inputDiv.children[0].style.border = "1px solid red"
        }
    }
    // Add event form's last field adjustment (job description field)
    createEventFormFieldList[createEventFormFieldList.length - 1].style.flexBasis = "90%"
}

// When pressing on any table row it expands the Job Description tab
document.querySelector('table#eventTable').addEventListener('click', (e) => {
    if (e.target.className.includes("job-description")) {
        let tdDescription = e.target.parentElement.lastElementChild
        if (tdDescription.className == 'job-description') {
            tdDescription.className = 'job-description wrap';
        }
    }
})

// 'Add event' button sets display of the form into block instead of none and vice versa
document.querySelector('button.addEvent').addEventListener('click', (e) => {
    let eventDiv = document.querySelector('div.createEventDiv');
    if (eventDiv.style.display == 'block') {
        eventDiv.style.display = 'none'
    }
    else {
        eventDiv.style.display = 'block';
    }
})

// Change the background color for one of the li items (Events) to let user know which page we are currently looking at
let sidebarLiElement = document.querySelector('li.index');
if (sidebarLiElement) {
    sidebarLiElement.style.backgroundColor = 'rgb(177, 229, 242)'
    sidebarLiElement.style.color = 'black'
}

let errorList = document.querySelector('ul.errorlist');
if (errorList) {
    document.querySelector('div.createEventDiv').style.display = "block";
}

// 
document.querySelector('select#id_sortby').addEventListener('change', (e) => {
    let sortBy = e.target;
    let form = sortBy.parentElement
    window.sessionStorage.setItem('sortby', e.target.value);
    form.submit()
})

let sortbyValue = window.sessionStorage.getItem('sortby', '-pk');

Array.from(document.querySelector('select#id_sortby').children).forEach(optionEl => {
    if (optionEl.value == sortbyValue) {
        optionEl.selected = true;
    } else {
        optionEl.selected = false;
    }
})