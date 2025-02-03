document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("routine-form").addEventListener("submit", analyzeRoutine)
  fetchRoutineHistory()
})

async function analyzeRoutine(event) {
  event.preventDefault()
  const routineData = document.getElementById("routine-data").value

  try {
    const response = await fetch("/api/routine-analysis", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ routine_data: routineData, user_id: 1 }), // Assuming user_id 1 for now
    })
    const data = await response.json()
    document.getElementById("analysis-result").innerHTML = `<h3>Analysis:</h3><p>${data.analysis}</p>`
    fetchRoutineHistory()
  } catch (error) {
    console.error("Error analyzing routine:", error)
  }
}

async function fetchRoutineHistory() {
  try {
    const response = await fetch("/api/routine-history?user_id=1") // Assuming user_id 1 for now
    const history = await response.json()
    displayRoutineHistory(history)
  } catch (error) {
    console.error("Error fetching routine history:", error)
  }
}

function displayRoutineHistory(history) {
  const historyList = document.getElementById("history-list")
  historyList.innerHTML = history
    .map(
      (item) => `
        <li>
            <strong>${new Date(item.date).toLocaleDateString()}</strong>
            <p>${item.data}</p>
            <p><em>Analysis: ${item.analysis}</em></p>
        </li>
    `,
    )
    .join("")
}

