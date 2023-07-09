var socket = io.connect("http://" + document.domain + ":" + location.port);

socket.on("streaming", (data) => {
  document.querySelector(".videos").src = `data:image/png;base64,${data.frame}`;
});
