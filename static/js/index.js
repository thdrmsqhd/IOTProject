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
      const id = each.id;
      const time = each.time;
      const picture_file = each.picture_file;
      return `
        <div class="dataRow" style="display: flex; justify-content: center; align-items: center; height: 10%; border-bottom: 1px solid">
          <div style="width: 5%">${id}</div>
          <div style="width: 40%">${time}</div>
          <div style="width: 55%">
            <img src="data:image/jpg;base64,${picture_file}" style="width: 50px; height: 50px" />
          </div>
        </div>
      `;
    })
    .join("");
  document.querySelector(".dataList").innerHTML = resultStr;
});

socket.on("plugStatus", (data) => {
  const plugStatus = data.plugStatus;
  controlPlugStatus(plugStatus);
});

document.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    socket.emit("capture");
    console.log("pressed Enter");
  }
});

function openImage(imageSrc) {
  const html = `
          <!DOCTYPE html>
          <html>
            <head>
              <meta charset="UTF-8">
              <title>Image Viewer</title>
              <style>
                img {
                  display: block;
                  margin: auto;
                  max-width: 100%;
                  max-height: 100%;
                }
              </style>
            </head>
            <body>
              <img src="data:image/jpg;base64, ${imageSrc}">
            </body>
          </html>
        `;

  const imageWindow = window.open();
  imageWindow.document.open();
  imageWindow.document.write(html);
  imageWindow.document.close();
}

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

function controlPlugStatus(plugStatus) {
  if (plugStatus === "ON") {
    document.querySelector(".plugLight").classList.add("green");
    document.querySelector(".plugLight").classList.remove("red");
  } else {
    document.querySelector(".plugLight").classList.add("red");
    document.querySelector(".plugLight").classList.remove("green");
  }
}
