let activeStudent = null;

function scrollDown() {
    const chatBody = document.getElementById("chat-body");
    chatBody.scrollTop = chatBody.scrollHeight;
}

function openChat(id, name) {
    activeStudent = id;  // FIXED

    document.getElementById("chatName").innerText = name;
    document.getElementById("messageBox").disabled = false;
    document.getElementById("sendBtn").disabled = false;

    loadMessages();
}

async function loadMessages() {
    if (!activeStudent) return;

    const res = await fetch(`/chat/${activeStudent}/`);
    const data = await res.json();

    const chatBody = document.getElementById("chat-body");
    chatBody.innerHTML = "";

    data.messages.forEach(m => {
        let div = document.createElement("div");
        div.className = "message " + (m.sender === "teacher" ? "me" : "other");
        div.innerText = m.message;
        chatBody.appendChild(div);
    });

    scrollDown();
}

setInterval(loadMessages, 1500);

document.getElementById("sendBtn").onclick = async () => {
    const messageBox = document.getElementById("messageBox");
    let msg = messageBox.value.trim();

    if (msg === "" || !activeStudent) return;

    await fetch(`/chat/send/${activeStudent}/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg })
    });

    messageBox.value = "";
    loadMessages();
};
