var socket = io.connect('http://' + document.domain + ':' + location.port);
alert(socket)
// alert(document.domain + location.port)

socket.on('streaming',(frame) => {
    console.log(frame)
})