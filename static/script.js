
const form = document.getElementById("chat-form");
const input = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");
const messagesContainer = document.getElementById("messages");
const welcome = document.getElementById("welcome");
const chatArea = document.getElementById("chat-area");

let conversation = [];
let busy = false;
let activeController = null;

function scrollToBottom() {
    if (chatArea) {
        chatArea.scrollTop = chatArea.scrollHeight;
    }
}

function addMessage(role, text, options = {}) {
    const row = document.createElement("div");
    row.className = "message " + role;

    if (options.error) {
        row.classList.add("error");
    }

    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.textContent = role === "user" ? "Y" : "B";

    const content = document.createElement("div");
    content.className = "message-content";

    const label = document.createElement("div");
    label.className = "message-label";
    label.textContent = role === "user" ? "YOU" : "BHASHAAI";

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = String(text);

    content.append(label, bubble);
    row.append(avatar, content);
    messagesContainer.appendChild(row);

    scrollToBottom();
    return row;
}

function showTyping() {
    hideTyping();

    const row = document.createElement("div");
    row.id = "typing-indicator";
    row.className = "message assistant";

    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.textContent = "B";

    const content = document.createElement("div");
    content.className = "message-content";

    const label = document.createElement("div");
    label.className = "message-label";
    label.textContent = "BHASHAAI";

    const bubble = document.createElement("div");
    bubble.className = "bubble typing";
    bubble.textContent = "Thinking…";

    content.append(label, bubble);
    row.append(avatar, content);
    messagesContainer.appendChild(row);
    scrollToBottom();
}

function hideTyping() {
    document.getElementById("typing-indicator")?.remove();
}

function setBusy(value) {
    busy = value;

    if (sendButton) {
        sendButton.disabled = value;
        sendButton.setAttribute("aria-busy", String(value));
    }

    if (input) {
        input.disabled = value;
    }
}

function resizeInput() {
    if (!input) return;
    input.style.height = "auto";
    input.style.height = Math.min(input.scrollHeight, 160) + "px";
}

function friendlyError(error) {
    if (error?.name === "AbortError") {
        return "The request was cancelled. Please try again.";
    }

    return error?.message ||
        "Something went wrong. Please try again.";
}

async function sendMessage(rawText) {
    const text = String(rawText || "").trim();

    if (!text || busy) return;

    if (welcome) {
        welcome.hidden = true;
    }

    addMessage("user", text);

    const candidateHistory = [
        ...conversation,
        { role: "user", content: text }
    ];

    input.value = "";
    resizeInput();
    setBusy(true);
    showTyping();

    activeController = new AbortController();

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify({
                messages: candidateHistory.slice(-16)
            }),
            signal: activeController.signal
        });

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            throw new Error(
                data.error ||
                `Server error (${response.status}). Please try again.`
            );
        }

        if (typeof data.reply !== "string" || !data.reply.trim()) {
            throw new Error("The assistant returned an empty response.");
        }

        conversation = [
            ...candidateHistory,
            { role: "assistant", content: data.reply }
        ].slice(-16);

        addMessage("assistant", data.reply);
    } catch (error) {
        addMessage("assistant", friendlyError(error), { error: true });
    } finally {
        hideTyping();
        setBusy(false);
        activeController = null;
        input?.focus();
    }
}

if (form && input && sendButton && messagesContainer) {
    form.addEventListener("submit", (event) => {
        event.preventDefault();
        sendMessage(input.value);
    });

    input.addEventListener("input", resizeInput);

    input.addEventListener("keydown", (event) => {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            form.requestSubmit();
        }
    });
}

document.querySelectorAll(".suggestion").forEach((button) => {
    button.addEventListener("click", () => {
        sendMessage(button.dataset.prompt || button.textContent || "");
    });
});

function clearConversation() {
    if (busy) return;

    conversation = [];
    messagesContainer?.replaceChildren();

    if (welcome) {
        welcome.hidden = false;
    }

    if (input) {
        input.value = "";
        resizeInput();
        input.focus();
    }
}

document.getElementById("new-chat")?.addEventListener(
    "click", clearConversation
);

document.getElementById("clear-chat")?.addEventListener(
    "click", clearConversation
);
