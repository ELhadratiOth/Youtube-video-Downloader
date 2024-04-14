// the use of 'window' is to link the changes to all tha window and not for a spesific element bcs i want all the page be averlayded   
window.customAlert = function(message) {
    // Creat the alert div
    const alert = document.createElement('div');
    // Creat OK button
    const alertButton = document.createElement('button');
    //"OK" bitton style
    alertButton.textContent = "OK";
    alertButton.classList.add('okButton');

    //Alert  style

    alert.classList.add('alert');
 
    //alert.style.zIndex = 1001; // add les cordonne d'alert  sur le menu cette valeur assure que  l'alerte est toujours en avant aperes  overlay element 
    // integrat  the button  and the convenable text in the Alert
    alert.innerHTML = `<div>${message}</div>`;
    alert.appendChild(alertButton);

    document.body.appendChild(alert); // to set the alert in the DOM

    // Create the overlay 
    const overlay = document.createElement('div');
    overlay.classList.add('alert-overlay');

    document.body.appendChild(overlay);

    

    // lisning to the alertbuton to remove overlay and  alert window from the DOM
    alertButton.addEventListener('click', function() {
        alert.remove();
        overlay.remove();
    });

    // Set focus to the OK button to allow interaction with keyboard
    alertButton.focus();
};
