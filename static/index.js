document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#display-name').onsubmit = () => {
        const name = document.querySelector('#name').value;
        localStorage.setItem("name", name);
    };
    document.querySelector('#add-channel').onsubmit = function() {
        const channel = document.querySelector('#channel').value;
    };
    document.querySelector('#add-message').onsubmit = function() {
        const channel = document.querySelector('#message').value;
    };
    document.querySelector('#display').innerHTML = localStorage.getItem("name");

});
