var socket = io.connect("http://" + document.domain + ":" + location.port);

socket.on("streaming", (data) => {
  document.querySelector(".videos").src = `data:image/png;base64,${data.frame}`;
});

socket.on("active", (data) => {
  console.log(data.active);
});

document.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    socket.emit("capture", { data: "pressed Enter" });
    console.log("pressed Enter");
  }
});
