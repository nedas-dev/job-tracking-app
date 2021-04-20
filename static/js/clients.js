const addClientDiv = document.querySelector('div.createClientDiv')
const addClientForm = document.querySelector('form.addClientForm');
const addClientButton = document.querySelector('button.addClient')
const clientsTable = document.getElementById('clientsTable');
const mainBody = document.getElementById('main');

function addClient() {
    var formData = new FormData();

    var csrfToken = document.cookie.split('=')[1]
    var name = document.getElementById('id_name').value;
    var address = document.getElementById('id_address').value;
    var email = document.getElementById('id_email_address').value;
    var phone = document.getElementById('id_phone_number').value;

    formData.append('csrfmiddlewaretoken', csrfToken)
    formData.append('name', name);
    formData.append('address', address);
    formData.append('email_address', email);
    formData.append('phone_number', phone);

    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            form_data = JSON.parse(xhttp.responseText)
            if (form_data['is_valid'] == true) {
                var trHeader = document.querySelector('tr.table-header').nextElementSibling
                var pk = trHeader.children[0].children[0].href
                var result = /\/(\d+)\//.exec(pk)[1]
                result = parseInt(result) + 1
                var parentNode = trHeader.parentElement
                var tr = document.createElement('tr');
                tr.classname = "table-row";

                tr.innerHTML = `
                <td class"link"><a class="link" href="/clients/${result}/">${form_data['name']}</a></td>
                <td> ${form_data['phone_number']} </td>
                <td> ${form_data['email_address']} </td>
                <td> ${form_data['address']} </td>
                `
                parentNode.insertBefore(tr, trHeader)
            }
        }
    };
    xhttp.open("POST", "", true);
    xhttp.send(formData);
}

function clearInputsAddClientForm() {
    document.getElementById('id_name').value = '';
    document.getElementById('id_address').value = '';
    document.getElementById('id_email_address').value = '';
    document.getElementById('id_phone_number').value = '';
}


addClientForm.addEventListener('submit', (e) => {
    e.preventDefault();
    addClientDiv.style.display = 'None';
    addClient()
    clearInputsAddClientForm()
})

addClientButton.addEventListener('click', (e) => {
    addClientDiv.style.display = 'Block';
    document.querySelector('p.formExit').addEventListener('click', (e) => {
        clearInputsAddClientForm()
        addClientDiv.style.display = 'None';
    }, { 'once': true })
})

// --------------------------------------------------------------
// Autocomplete address script for Google Place API
function initAutocomplete() {
    let address1Field = document.querySelector("#id_address");
    // Create the autocomplete object, restricting the search predictions to
    // addresses in the US.
    let autocomplete = new google.maps.places.Autocomplete(address1Field, {
        componentRestrictions: { country: ["us"] },
        fields: ["address_components", "geometry"],
        types: ["address"],
    });
}
