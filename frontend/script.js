const questionInput = document.getElementById("question");
const askButton = document.getElementById("ask-button");
const answerBox = document.getElementById("answer");
const answerText = document.getElementById("answer-text");
const loading = document.getElementById("loading");

const exampleQuestions = document.querySelectorAll(".example-question");

function formatAnswer(text) {
    const escaped = text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");

    return escaped
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/\n/g, "<br>");
}

async function askAnalyst(question) {
    if (!question.trim()) {
        return;
    }

    answerBox.classList.add("hidden");
    loading.classList.remove("hidden");
    askButton.disabled = true;

    try {
        const response = await fetch("http://127.0.0.1:8000/ai/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }

        const data = await response.json();

        answerText.innerHTML = formatAnswer(data.answer);
        answerBox.classList.remove("hidden");

    } catch (error) {
        console.error(error);

        answerText.textContent =
            "Unable to connect to the AI analyst. Make sure the FastAPI server is running.";

        answerBox.classList.remove("hidden");

    } finally {
        loading.classList.add("hidden");
        askButton.disabled = false;
    }
}

askButton.addEventListener("click", () => {
    askAnalyst(questionInput.value);
});

exampleQuestions.forEach((button) => {
    button.addEventListener("click", () => {
        const question = button.textContent.trim();

        questionInput.value = question;

        askAnalyst(question);
    });
});

questionInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        askAnalyst(questionInput.value);
    }
});