let curr_room = null;

document.addEventListener("DOMContentLoaded", () => {
    const socket = io("https://flask-messaging-app.onrender.com");
    

    socket.emit('join', {
        'user1' : user1,
        'user2' : user2
    });

    socket.on('joined_room', function(data) {
        curr_room = data['room'];
    })

    document.getElementById("msg-form").addEventListener("submit", function (e) {
        e.preventDefault();
        const msg = document.getElementById("msg").value;
        socket.emit('send_message', {'message' : msg, 'room' : curr_room});
        document.getElementById("msg").value = "";

    })

    socket.on("receive_msg", function(data) {
        const msgList = document.getElementById('messages');
        const newMsg = document.createElement('li');

        newMsg.textContent = data['sender'] + ": " + data['message'];
        msgList.appendChild(newMsg);
    });

    document.getElementById("return-button").addEventListener("click", () => {
        socket.emit('leave', {'room' : curr_room});
    });
});
