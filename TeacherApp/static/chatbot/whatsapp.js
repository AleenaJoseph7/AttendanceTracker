document.addEventListener("DOMContentLoaded", function () {
    const chatBody = document.getElementById("chat-body");
    const messageBox = document.getElementById("messageBox");
    const sendBtn = document.getElementById("sendBtn");

    // because your app is mounted as path('TeacherAdmin/', include(...))
    const BASE_URL = "/TeacherAdmin";
    const sid = studentID;  // from the <script> tag in template

    function scrollDown() {
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    async function loadMessages() {
        if (!sid) return;

        try {
            const res = await fetch(`${BASE_URL}/chat/${sid}/`);
            const data = await res.json();

            chatBody.innerHTML = "";

            data.messages.forEach(m => {
                let div = document.createElement("div");
                // Make sure "me" and "other" match your CSS
                div.className = "message " + (m.sender === "teacher" ? "me" : "other");
                div.innerText = m.message;
                chatBody.appendChild(div);
            });

            scrollDown();
        } catch (err) {
            console.error("Error loading messages:", err);
        }
    }

    async function sendMessage() {
        const msg = messageBox.value.trim();
        if (msg === "" || !sid) return;

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

    sendBtn.addEventListener("click", sendMessage);

    messageBox.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
            e.preventDefault();
            sendMessage();
        }
    });

    // auto refresh chat every 1.5s
    setInterval(loadMessages, 1500);
    loadMessages();
});
