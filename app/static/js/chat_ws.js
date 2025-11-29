const ws = new WebSocket(`ws://${location.host}/chat/ws/${USER_ID}`);

ws.onmessage = (event) => {
    appendMessage(event.data);
};

document.querySelector("#send").onclick = () => {
    ws.send(document.querySelector("#msg").value);
};
