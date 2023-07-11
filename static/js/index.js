var socket = io.connect("http://" + document.domain + ":" + location.port);

socket.on("streaming", (data) => {
  document.querySelector(".videos").src = `data:image/png;base64,${data.frame}`;
});

socket.on("active", (data) => {
  console.log(data.active);
});

socket.on("refreshData", (data) => {
  const resultStr = data.datas
    .map((each) => {
      return `<div>${each.id}, ${each.time}</div>`;
    })
    .join("");
  document.querySelector(".dataList").innerHTML = resultStr;
});

socket.on("plugStatus", (data) => {
  const plugStatus = data.plugStatus
  controlPlugStatus(plugStatus)
});

document.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    socket.emit("capture");
    console.log("pressed Enter");
  }
});


setInterval(setTime, 1000);
function setTime() {
  const now = new Date();
  const hour = now.getHours() <= 9 ? "0" + now.getHours() : now.getHours();
  const minute = now.getMinutes() <= 9 ? "0" + now.getMinutes() : now.getMinutes();
  const second = now.getSeconds() <= 9 ? "0" + now.getSeconds() : now.getSeconds();

  document.querySelector(".time").innerHTML = `${dateFormat(now)} ${hour}:${minute}:${second}`;
}

function dateFormat(date) {
  let dateFormat2 =
    date.getFullYear() +
    "-" +
    (date.getMonth() + 1 < 9 ? "0" + (date.getMonth() + 1) : date.getMonth() + 1) +
    "-" +
    (date.getDate() < 9 ? "0" + date.getDate() : date.getDate());
  return dateFormat2;
}

function controlPlugStatus(plugStatus){
  if (plugStatus === "ON"){
    document.querySelector(".plugLight").classList.add("green")
  }else{
    document.querySelector(".plugLight").classList.add("red")
  }
}