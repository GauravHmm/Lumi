document.addEventListener("DOMContentLoaded", () => {
  fetchGoals()
  document.getElementById("add-goal-form").addEventListener("submit", addGoal)
})

async function fetchGoals() {
  try {
    const response = await fetch("/api/goals")
    const goals = await response.json()
    displayGoals(goals)
  } catch (error) {
    console.error("Error fetching goals:", error)
  }
}

function displayGoals(goals) {
  const goalsList = document.getElementById("goals-list")
  goalsList.innerHTML = goals
    .map(
      (goal) => `
        <div class="goal">
            <h3>${goal.title}</h3>
            <p>${goal.description}</p>
            <p>Target Date: ${new Date(goal.target_date).toLocaleDateString()}</p>
            <p>Status: ${goal.completed ? "Completed" : "In Progress"}</p>
        </div>
    `,
    )
    .join("")
}

async function addGoal(event) {
  event.preventDefault()
  const title = document.getElementById("goal-title").value
  const description = document.getElementById("goal-description").value
  const targetDate = document.getElementById("goal-target-date").value

  try {
    const response = await fetch("/api/goals", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title, description, target_date: targetDate, user_id: 1 }), // Assuming user_id 1 for now
    })
    if (response.ok) {
      fetchGoals()
      event.target.reset()
    }
  } catch (error) {
    console.error("Error adding goal:", error)
  }
}

