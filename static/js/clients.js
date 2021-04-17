var formData = new FormData();
formData.append('hello', 'labas');
var csrfToken = document.cookie.split('=')[1]
formData.append('csrfmiddlewaretoken', csrfToken)
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        console.log(JSON.parse(xhttp.responseText))
    }
};
xhttp.open("POST", "/clients/create-new", true);
xhttp.send(formData);