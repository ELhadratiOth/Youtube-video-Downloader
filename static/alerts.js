window.customAlert = function(message) {
    // Check if the alert and overlay already exist in the DOM
    let alert = document.querySelector('.alert');
    let overlay = document.querySelector('.alert-overlay');

    // Create the alert and overlay only if they don't already exist
    if (!overlay && !alert) {
        // Create the alert div
        alert = document.createElement('div');
        // Create OK button
        const alertButton = document.createElement('button');
        //"OK" button style
        alertButton.textContent = "OK";
        alertButton.classList.add('okButton');

        // Alert style
        alert.classList.add('alert');
        // Append the OK button and the message to the alert
        alert.innerHTML = `<div>${message}</div>`;
        alert.appendChild(alertButton);

        document.body.appendChild(alert); // Append the alert to the DOM

        // Create the overlay
        overlay = document.createElement('div');
        overlay.classList.add('alert-overlay');
        document.body.appendChild(overlay);

        // Listening to the alert button to remove the overlay and alert window from the DOM
        alertButton.addEventListener('click', function() {
            alert.remove();
            overlay.remove();
        });

        // Set focus to the OK button to allow interaction with keyboard
        alertButton.focus();
    }
};
