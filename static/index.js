document.addEventListener('DOMContentLoaded', () => {

    // connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // if no channel selected appoint general as default
    if (localStorage.getItem("page") == null)
        localStorage.setItem("page", "general");


    // takes display name from form and stores it
    document.querySelector('#display-name').onsubmit = () => {
        const name = document.querySelector('#name').value;
        localStorage.setItem("name", name);
    };

    // updates displayname
    document.querySelector('#display').innerHTML = localStorage.getItem("name");


    // when connected, configure buttons
    socket.on('connect', () => {

        // updates the current channel when a link is clicked
        document.querySelectorAll('.nav-link li a').forEach(link => {
            link.onclick = () => {
                const page = link.innerHTML;
                localStorage.setItem("page", page);
                socket.emit('current page', {'page': page});
                return false;
            };
        });

        // displays the new current channel
        document.querySelector('#current_page').innerHTML = localStorage.getItem("page");


        // takes user input from the create channel form
        document.querySelector('#add-channel').onsubmit = () => {
            var channel = document.querySelector('#channel').value;

            // checks that the string is not empty
            if (channel.length == 0 || channel === ' ')
                return false;
            socket.emit('submit channel', {'channel': channel});
            document.querySelector('#channel').value = "";
            return false;
        };


        // takes user input from the message form
        document.querySelector('#add-message').onsubmit = () => {
            var message = document.querySelector('#message').value;
            var channel = localStorage.getItem("page");

            // checks that the string is not empty
            if (message.length == 0 || message === ' ')
                return false;

            // adds the display name to the message
            message = localStorage.getItem("name") + ": " + message;
            socket.emit('submit message', {'message': message, 'channel': channel});
            document.querySelector('#message').value = "";
            return false;
        };



        // If scrolled to bottom, load the next 20 posts.
        window.onscroll = () => {
            if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
                load();
            }
        };



    });

    // adds the new channel to the channels list
    socket.on('announce channel', data => {
        const li = document.createElement('li');
        li.innerHTML = `<a href="">${data.channel}</a>`;
        document.querySelector('#channels').append(li);
    });

    // adds the new message to the messages list
    socket.on('announce message', data => {
        const li = document.createElement('li');
        li.innerHTML = `${data.message}`;
        document.querySelector('#messages').append(li);
    });

    // displays the current channel
    socket.on('current page', data => {
        document.querySelector('#current_page').innerHTML = data.current_page;
    });

    // Start with first post.
    let counter = 1;

    // Load posts 20 at a time.
    const quantity = 20;

    // Load next set of posts.
    function load() {

        // Set start and end post numbers, and update counter.
        const start = counter;
        const end = start + quantity - 1;
        counter = end + 1;

        // Open new request to get new posts.
        const request = new XMLHttpRequest();
        request.open('POST', '/messages');
        request.onload = () => {
            const data = JSON.parse(request.responseText);
            data.forEach(add_post);
        };

        // Add start and end points to request data.
        const data = new FormData();
        data.append('start', start);
        data.append('end', end);

        // Send request.
        request.send(data);
    };

    function add_post(contents) {
        const li = document.createElement('li');
        li.innerHTML = contents;
        document.querySelector('#messages').append(li);
    }

});