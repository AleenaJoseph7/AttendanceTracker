document.addEventListener("DOMContentLoaded", function () {

    // ================================
    // ELEMENT REFERENCES
    // ================================
    const chatBody = document.getElementById("chat-body");
    const messageBox = document.getElementById("messageBox");
    const sendBtn = document.getElementById("sendBtn");
    const clearBtn = document.getElementById("clearChatBtn");

    // SAFETY CHECK
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

            // Teacher side → needs studentID in URL
            if (studentID) {
                url = `${BASE_URL}/chat/${studentID}/`;
            }
            // Student side → session-based
            else {
                url = `${BASE_URL}/chat/`;
            }

            const res = await fetch(url);
            const data = await res.json();

            chatBody.innerHTML = "";

            data.messages.forEach(m => {
                const div = document.createElement("div");

                const isMe = m.sender.toLowerCase() === senderSide;
                div.className = "message " + (isMe ? "me" : "other");



                // READ TICKS (only for sender)
                    let ticks = "";
                    if (isMe && m.read_status === "sent") {
                    ticks = "✓";
                    }

                    if (isMe && m.read_status === "read") {
                        ticks = "✓✓";
                        div.classList.add("read");
                        }




                div.innerHTML = `
                    <span>${m.message}</span>
                    <div class="meta">
                        <small>${m.time || ""}</small>
                        <small class="ticks">${ticks}</small>
                    </div>
                `;

                chatBody.appendChild(div);
            });

            scrollDown();

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

            // Teacher side
            if (studentID) {
                url = `${BASE_URL}/chat/send/${studentID}/`;
            }
            // Student side
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

            if (studentID) {
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
