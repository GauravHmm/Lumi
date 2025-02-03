document.addEventListener("DOMContentLoaded", () => {
  fetchOverviewData()
})

async function fetchOverviewData() {
  try {
    const response = await fetch("/api/overview")
    const data = await response.json()
    updateOverviewCards(data)
  } catch (error) {
    console.error("Error fetching overview data:", error)
  }
}

function updateOverviewCards(data) {
  document.querySelector("#weekly-overview .overview-content").innerHTML = data.weekly_overview
  document.querySelector("#monthly-overview .overview-content").innerHTML = data.monthly_overview

  const goalsProgress = document.querySelector("#goals-progress .overview-content")
  goalsProgress.innerHTML = data.goals_progress
    .map((goal) => `<p>${goal.title}: ${goal.completed ? "Completed" : "In Progress"}</p>`)
    .join("")

  const meditationStats = document.querySelector("#meditation-stats .overview-content")
  meditationStats.innerHTML = `
        <p>Total Sessions: ${data.meditation_stats.total_sessions}</p>
        <p>Total Minutes: ${data.meditation_stats.total_minutes}</p>
    `
}

