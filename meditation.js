document.addEventListener("DOMContentLoaded", () => {
  fetchMeditationSuggestions()
  document.getElementById("log-meditation-form").addEventListener("submit", logMeditation)
})

async function fetchMeditationSuggestions() {
  try {
    const response = await fetch("/api/meditation-suggestions?user_id=1") // Assuming user_id 1 for now
    const suggestions = await response.json()
    document.getElementById("meditation-suggestions").innerHTML = `<h3>Suggestions:</h3><p>${suggestions}</p>`
  } catch (error) {
    console.error("Error fetching meditation suggestions:", error)
  }
}

async function logMeditation(event) {
  event.preventDefault()
  const duration = document.getElementById("meditation-duration").value
  const type = document.getElementById("meditation-type").value

  try {
    const response = await fetch("/api/meditation-log", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ user_id: 1, duration, type }), // Assuming user_id 1 for now
    })
    if (response.ok) {
      alert("Meditation session logged successfully!")
      event.target.reset()
      fetchMeditationSuggestions()
    }
  } catch (error) {
    console.error("Error logging meditation:", error)
  }
}

