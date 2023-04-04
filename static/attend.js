  var socket = io.connect("http://192.168.43.225:5000");
        socket.on('connect', function () {
            socket.emit('my event', { data: 'I\'m connected!' });
        });

function fecth_attendance()
{
    socket.emit("take_attendance",{"credentials":"data"})

}

function Fetch_report()
{
    socket.emit("generateReport",{"credentials":"data"})

}