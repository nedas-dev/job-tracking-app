const addClientDiv = document.querySelector('div.createClientDiv')
const addClientForm = document.querySelector('form.addClientForm');
const addClientButton = document.querySelector('button.addClient')
const clientsTable = document.getElementById('clientsTable');
const mainBody = document.getElementById('main');

function createClient() {
    var formData = new FormData();
    var csrfToken = document.cookie.split('=')[1]
    formData.append('csrfmiddlewaretoken', csrfToken)

    var name = document.getElementById('id_name').value;
    var address = document.getElementById('id_address').value;
    var email = document.getElementById('id_email_address').value;
    var phone = document.getElementById('id_phone_number').value;

    formData.append('name', name);
    formData.append('address', address);
    formData.append('email_address', email);
    formData.append('phone_number', phone);
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            form_data = JSON.parse(xhttp.responseText)
            if (form_data['is_valid'] == true) {
                var client = `
                <tr class="table-row">
                    <td> ${form_data['name']} </td>
                    <td> ${form_data['phone_number']} </td>
                    <td> ${form_data['email_address']} </td>
                    <td> ${form_data['address']} </td>
                </tr>`
                clientsTable.innerHTML += client
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
    createClient()
    clearInputsAddClientForm()
})

addClientButton.addEventListener('click', (e) => {
    addClientDiv.style.display = 'Block';
    document.querySelector('p.formExit').addEventListener('click', (e) => {
        clearInputsAddClientForm()
        addClientDiv.style.display = 'None';
    }, { 'once': true })
})

