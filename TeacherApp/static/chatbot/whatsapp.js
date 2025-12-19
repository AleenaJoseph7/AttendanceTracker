document.addEventListener("DOMContentLoaded", function () {

    // ================================
    // ELEMENT REFERENCES
    // ================================
    const chatBody = document.getElementById("chat-body");
    const messageBox = document.getElementById("messageBox");
    const sendBtn = document.getElementById("sendBtn");
    const clearBtn = document.getElementById("clearChatBtn");

    if (!chatBody || !messageBox || !sendBtn) {
        console.error("Chat elements missing in DOM");
        return;
    }

    // ================================
    // HELPERS
    // ================================
    function scrollDown() {
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    // ================================
    // LOAD MESSAGES
    // ================================
    async function loadMessages() {
    try {
        let url = "";

        if (senderSide === "teacher") {
            url = `${BASE_URL}/chat/${studentID}/`;
        } else {
            url = `${BASE_URL}/chat/get/`;
        }

        const res = await fetch(url);
        const data = await res.json();

        chatBody.innerHTML = "";

        data.messages.forEach(m => {
            const div = document.createElement("div");
            const isMe = m.sender === senderSide;

            div.className = "message " + (isMe ? "me" : "other");

            let ticks = "";
            if (isMe && m.read_status === "sent") ticks = "✓";
            if (isMe && m.read_status === "read") {
                ticks = "✓✓";
                div.classList.add("read");
            }

            div.innerHTML = `
                <span>${m.message}</span>
                <div class="meta">
                    <small>${m.time}</small>
                    <small class="ticks">${ticks}</small>
                </div>
            `;

            chatBody.appendChild(div);
        });

        chatBody.scrollTop = chatBody.scrollHeight;

    } catch (err) {
        console.error("Failed to load messages", err);
    }
}


    // ================================
    // SEND MESSAGE
    // ================================
    async function sendMessage() {
        const msg = messageBox.value.trim();
        if (!msg) return;

        try {
            let url = "";

            // ✅ Teacher sending to student
            if (senderSide === "teacher") {
                url = `${BASE_URL}/chat/send/${studentID}/`;
            }
            // ✅ Student sending to teacher
            else {
                url = `${BASE_URL}/chat/send/`;
            }

            await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: msg })
            });

            messageBox.value = "";
            loadMessages();

        } catch (err) {
            console.error("Failed to send message", err);
        }
    }

    // ================================
    // CLEAR CHAT
    // ================================
    async function clearChat() {
        try {
            let url = "";

            if (senderSide === "teacher") {
                url = `${BASE_URL}/chat/clear/${studentID}/`;
            } else {
                url = `${BASE_URL}/chat/clear/`;
            }

            await fetch(url, { method: "POST" });
            chatBody.innerHTML = "";

        } catch (err) {
            console.error("Failed to clear chat", err);
        }
    }

    // ================================
    // EVENTS
    // ================================
    sendBtn.addEventListener("click", sendMessage);

    messageBox.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
            sendMessage();
        }
    });

    if (clearBtn) {
        clearBtn.addEventListener("click", clearChat);
    }

    // ================================
    // AUTO REFRESH
    // ================================
    loadMessages();
    setInterval(loadMessages, 1500);
});
