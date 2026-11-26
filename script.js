
let subject = "";
let questions = [];
let current = 0;
let score = 0;
let lives = 3;
let correctCount = 0;
let wrongCount = 0;
let timer = null;
let timeLeft = 15;
let answered = false;
let loading = false;

const QUESTION_TIME = 15;

function showScreen(id) {
    document.querySelectorAll(".screen").forEach(screen => {
        screen.classList.remove("active");
    });

    document.getElementById(id).classList.add("active");
}

async function startGame(selected) {

    if (loading) return;

    loading = true;
    subject = selected;

    localStorage.setItem("lastSubject", selected);

    clearInterval(timer);
    showScreen("quiz");

    document.getElementById("question").textContent =
        "Generating fresh questions...";

    document.getElementById("options").innerHTML = "";

    try {
        const response = await fetch(
            `/api/questions?subject=${encodeURIComponent(selected)}`,
            { cache: "no-store" }
        );

        if (!response.ok) {
            throw new Error("Question server error");
        }

        const data = await response.json();

        questions = data.questions;

        current = 0;
        score = 0;
        lives = 3;
        correctCount = 0;
        wrongCount = 0;

        loadQuestion();

    } catch (error) {
        document.getElementById("question").textContent =
            "Unable to load questions. Please restart the server.";

        console.error(error);

    } finally {
        loading = false;
    }
}

function loadQuestion() {

    clearInterval(timer);

    if (current >= questions.length || lives <= 0) {
        endGame();
        return;
    }

    answered = false;

    const q = questions[current];

    document.getElementById("subjectName").textContent =
        subject.toUpperCase();

    document.getElementById("chapterName").textContent =
        q.chapter.toUpperCase();

    document.getElementById("question").textContent = q.q;

    document.getElementById("score").textContent = score;
    document.getElementById("lives").textContent = lives;
    document.getElementById("level").textContent = current + 1;

    document.getElementById("feedback").textContent = "";

    document.getElementById("nextBtn").hidden = true;

    document.getElementById("progressBar").style.width =
        `${(current / questions.length) * 100}%`;

    const optionsContainer = document.getElementById("options");

    optionsContainer.innerHTML = "";

    q.o.forEach((option, index) => {

        const button = document.createElement("button");

        button.className = "option";
        button.textContent = `${String.fromCharCode(65 + index)}. ${option}`;

        button.addEventListener("click", () => {
            checkAnswer(index);
        });

        optionsContainer.appendChild(button);
    });

    timeLeft = QUESTION_TIME;
    updateTimer();

    timer = setInterval(() => {

        timeLeft--;

        updateTimer();

        if (timeLeft <= 0) {
            checkAnswer(-1);
        }

    }, 1000);
}

function updateTimer() {

    const timerElement = document.getElementById("timer");

    timerElement.textContent = `${timeLeft}s`;

    timerElement.classList.toggle("danger", timeLeft <= 5);
}

function checkAnswer(selected) {

    if (answered) return;

    answered = true;

    clearInterval(timer);

    const q = questions[current];

    const buttons = document.querySelectorAll(".option");

    buttons.forEach((button, index) => {

        button.disabled = true;

        if (index === q.a) {
            button.classList.add("correct");
        }

        if (index === selected && selected !== q.a) {
            button.classList.add("wrong");
        }
    });

    const feedback = document.getElementById("feedback");

    if (selected === q.a) {

        score += 10;
        correctCount++;

        feedback.textContent = "✓ CORRECT ANSWER! +10 XP";
        feedback.style.color = "#22c55e";

    } else {

        lives--;
        wrongCount++;

        feedback.textContent = selected === -1
            ? "⏰ TIME UP! Correct answer highlighted."
            : "✗ INCORRECT! Correct answer highlighted.";

        feedback.style.color = "#ef4444";
    }

    document.getElementById("score").textContent = score;
    document.getElementById("lives").textContent = lives;

    document.getElementById("nextBtn").hidden = false;

    document.getElementById("nextBtn").textContent =
        current === questions.length - 1 || lives === 0
        ? "VIEW RESULTS →"
        : "NEXT QUESTION →";
}

function nextQuestion() {

    if (!answered) return;

    current++;

    loadQuestion();
}

function endGame() {

    clearInterval(timer);

    showScreen("result");

    const total = correctCount + wrongCount;

    const accuracy = total === 0
        ? 0
        : Math.round((correctCount / total) * 100);

    document.getElementById("finalScore").textContent =
        `${score} XP`;

    document.getElementById("correctCount").textContent =
        correctCount;

    document.getElementById("wrongCount").textContent =
        wrongCount;

    document.getElementById("accuracy").textContent =
        `${accuracy}%`;

    let rank;
    let message;

    if (accuracy === 100) {
        rank = "🏆 PERFECT GENIUS";
        message = "Outstanding! Every answer was correct.";

    } else if (accuracy >= 80) {
        rank = "⭐ EXCELLENT";
        message = "Amazing performance! Keep it up.";

    } else if (accuracy >= 60) {
        rank = "🔥 GOOD JOB";
        message = "You are improving. Keep practising.";

    } else {
        rank = "📚 KEEP LEARNING";
        message = "Revise your NCERT concepts and try again.";
    }

    document.getElementById("rank").textContent = rank;

    document.getElementById("resultMessage").textContent =
        message;
}

function goHome() {

    clearInterval(timer);

    localStorage.removeItem("lastSubject");

    showScreen("home");
}


// Automatically start a fresh round after browser refresh
window.addEventListener("DOMContentLoaded", () => {

    const previousSubject = localStorage.getItem("lastSubject");

    if (previousSubject) {
        startGame(previousSubject);
    }

});
