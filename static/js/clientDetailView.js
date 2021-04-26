const updateForm = document.querySelector('form.updateClientForm')

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
