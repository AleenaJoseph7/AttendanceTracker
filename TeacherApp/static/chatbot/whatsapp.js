// static/chatbot/whatsapp.js

document.addEventListener("DOMContentLoaded", function () {
    const chatBody   = document.getElementById("chat-body");
    const messageBox = document.getElementById("messageBox");
    const sendBtn    = document.getElementById("sendBtn");
    const clearBtn   = document.getElementById("clearChatBtn");   // Clear chat button

    // Your app is mounted at /TeacherAdmin/
    const BASE_URL = "/TeacherAdmin";
    const sid = studentID;   // comes from <script> in Chatbot.html

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
                // "me" vs "other" should match your whatsapp.css
                div.className = "message " + (m.sender === "teacher" ? "me" : "other");
                div.innerText = m.message;
                chatBody.appendChild(div);
            });

            scrollDown();
        } catch (err) {
            console.error("Error loading messages:", err);
        }
    }

    // ------------ SEND MESSAGE ------------
    async function sendMessage() {
        if (!sid) return;
        const msg = messageBox.value.trim();
        if (msg === "") return;

        try {
            await fetch(`${BASE_URL}/chat/send/${sid}/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: msg })
            });

            messageBox.value = "";
            loadMessages();
        } catch (err) {
            console.error("Error sending message:", err);
        }
    }

    // ------------ CLEAR CHAT ------------
    async function clearChat() {
        if (!sid) return;

        const ok = confirm("Are you sure you want to clear this chat?");
        if (!ok) return;

        try {
            await fetch(`${BASE_URL}/chat/clear/${sid}/`, {
                method: "POST"
            });

            chatBody.innerHTML = "";
            alert("Chat cleared successfully.");
        } catch (err) {
            console.error("Error clearing chat:", err);
        }
    }

    // ------------ EVENT LISTENERS ------------
    if (sendBtn) {
        sendBtn.addEventListener("click", sendMessage);
    }

    if (messageBox) {
        messageBox.addEventListener("keydown", function (e) {
            if (e.key === "Enter") {
                e.preventDefault();
                sendMessage();
            }
        });
    }

    if (clearBtn) {
        clearBtn.addEventListener("click", clearChat);
    }

    // Auto refresh every 1.5 seconds
    setInterval(loadMessages, 1500);
    loadMessages();
});
