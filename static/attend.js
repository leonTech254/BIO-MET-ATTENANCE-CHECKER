  var socket = io.connect("http://127.0.0.1:5000");
        socket.on('connect', function () {
            socket.emit('my event', { data: 'I\'m connected!' });
        });

function fecth_attendance()
{
    axios.get("http://127.0.0.1:5000/api/take_attendance")
    // socket.emit("take_attendance",{"credentials":"data"})

}

function Fetch_report()
{
    axios.get("http://127.0.0.1:5000/api/generateReport")

    // socket.emit("generateReport",{"credentials":"data"})

}