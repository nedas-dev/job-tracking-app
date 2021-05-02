// HOME PAGE JS SCRIPT
const createEventFormFieldList = document.querySelectorAll('div.field');

if (createEventFormFieldList) {
    for (let i = 0; i < createEventFormFieldList.length; i++) {
        let fieldChildren = createEventFormFieldList[i].children;
        let errorDiv = fieldChildren[0]
        let inputDiv = fieldChildren[2]
        if (errorDiv.children.length > 0) {
            inputDiv.children[0].style.border = "1px solid red"
        }
    }
    // Add event form's last field adjustment
    createEventFormFieldList[createEventFormFieldList.length - 1].style.flexBasis = "90%"
}

// When pressing on any table row it expands the Job Description tab (or minimizes)
document.querySelector('table#eventTable').addEventListener('click', (e) => {
    if (e.target.parentElement.className == 'table-row') {
        let tdDescription = e.target.parentElement.lastElementChild
        if (tdDescription.className == 'job-description wrap') {
            tdDescription.className = 'job-description';
        }
        else {
            tdDescription.className = 'job-description wrap'
        }
    }
})