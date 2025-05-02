// script.js
const navItems = document.querySelectorAll(".sidebar li");
const sections = document.querySelectorAll(".main section");

navItems.forEach((item, index) => {
  item.addEventListener("click", () => {
    sections.forEach(section => section.classList.remove("active"));
    sections[index].classList.add("active");
  });
});

function startOnboarding() {
  document.getElementById("login-screen").style.display = "none";
  document.getElementById("onboarding-screen").style.display = "flex";
}

function finishOnboarding() {
  document.getElementById("onboarding-screen").style.display = "none";
  document.getElementById("app").style.display = "flex";
}

async function generatePlan() {
  const course = document.getElementById("course-input").value;
  const style = document.getElementById("learning-style").value;
  const interest = document.getElementById("interest-input").value;
  const hours = document.getElementById("hours-input").value;
  const output = document.getElementById("plan-output");

  output.innerHTML = "Generating your lesson plan...";

  const response = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer YOUR_OPENAI_API_KEY`
    },
    body: JSON.stringify({
      model: "gpt-3.5-turbo",
      messages: [
        { role: "system", content: "You are an AI assistant that creates personalized lesson plans based on student input." },
        { role: "user", content: `Create a weekly study plan for the course: ${course}. Learning style: ${style}. Student is interested in: ${interest} and has ${hours} hours available per week.` }
      ]
    })
  });

  const data = await response.json();
  const reply = data.choices[0].message.content;

  output.innerHTML = `<pre>${reply}</pre>`;
  document.getElementById("task-list").innerHTML += `<li>📚 Start: ${course}</li>`;
  document.getElementById("opportunity-list").innerHTML += `
    <div>
      <strong>Opportunity: AI Assistant for ${course}</strong>
      <p>Based on your interests: ${interest}</p>
      <button onclick="addTask('Apply for opportunity: ${interest}')">Add to Tasks</button>
    </div>
  `;
}

function addTask(text) {
  document.getElementById("task-list").innerHTML += `<li>${text}</li>`;
}

