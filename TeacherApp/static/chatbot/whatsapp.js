// static/chatbot/whatsapp.js

document.addEventListener("DOMContentLoaded", function () {
    const chatBody   = document.getElementById("chat-body");
    const messageBox = document.getElementById("messageBox");
    const sendBtn    = document.getElementById("sendBtn");
    const clearBtn   = document.getElementById("clearChatBtn");

    const BASE_URL = "/TeacherAdmin";
    const sid = studentID;

    function scrollDown() {
        if (!chatBody) return;
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    // ------------ LOAD MESSAGES ------------
    async function loadMessages() {
        if (!sid || !chatBody) return;

        try {
            const res = await fetch(`${BASE_URL}/chat/${sid}/`);
            const data = await res.json();

            chatBody.innerHTML = "";

            data.messages.forEach(m => {
                const div = document.createElement("div");
                div.className = "message " + (m.sender === "teacher" ? "me" : "other");

                // Generate ticks based on read_status
                let ticks = "";
                if (m.sender === "teacher") {
                    if (m.read_status === "sent") {
                        ticks = "✓";
                    } else if (m.read_status === "delivered") {
                        ticks = "✓✓";
                    } else if (m.read_status === "read") {
                        ticks = '✓✓'; // blue tick styled in CSS
                        div.classList.add("read");
                    }
                }

                div.innerHTML = `
                    <span>${m.message}</span>
                    <small class="ticks">${ticks}</small>
                `;

                chatBody.appendChild(div);
            });

            scrollDown();

        } catch (err) {
            console.error("Error loading messages:", err);
        }
    }

    // ------------ SEND MESSAGE ------------
    async function sendMessage() {
        const msg = messageBox.value.trim();
        if (!msg || !sid) return;

        try {
            await fetch(`${BASE_URL}/chat/send/${sid}/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: msg })
            });

            messageBox.value = "";
            loadMessages();

        } catch (err) {
            console.error("Error sending:", err);
        }
    }

    // ------------ CLEAR CHAT ------------
    async function clearChat() {
        if (!sid) return;

        const ok = confirm("Clear chat?");
        if (!ok) return;

        try {
            await fetch(`${BASE_URL}/chat/clear/${sid}/`, { method: "POST" });

            chatBody.innerHTML = "";
            alert("Chat cleared!");

        } catch (err) {
            console.error("Error clearing chat:", err);
        }
    }

    // Listeners
    if (sendBtn) sendBtn.addEventListener("click", sendMessage);

    if (messageBox) {
        messageBox.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                sendMessage();
            }
        });
    }

    if (clearBtn) clearBtn.addEventListener("click", clearChat);

    // Auto refresh every 1.5 sec
    setInterval(loadMessages, 1500);
    loadMessages();
});
