document.addEventListener("DOMContentLoaded", () => {
  fetchCommunityPosts()
  document.getElementById("new-post-form").addEventListener("submit", createPost)
})

async function fetchCommunityPosts() {
  try {
    const response = await fetch("/api/community-posts")
    const posts = await response.json()
    displayCommunityPosts(posts)
  } catch (error) {
    console.error("Error fetching community posts:", error)
  }
}

function displayCommunityPosts(posts) {
  const postsContainer = document.getElementById("community-posts")
  postsContainer.innerHTML = posts
    .map(
      (post) => `
        <div class="post">
            <p>${post.content}</p>
            <small>Posted by User ${post.user_id} on ${new Date(post.timestamp).toLocaleString()}</small>
        </div>
    `,
    )
    .join("")
}

async function createPost(event) {
  event.preventDefault()
  const content = document.getElementById("post-content").value

  try {
    const response = await fetch("/api/community-posts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ user_id: 1, content }), // Assuming user_id 1 for now
    })
    if (response.ok) {
      fetchCommunityPosts()
      event.target.reset()
    }
  } catch (error) {
    console.error("Error creating post:", error)
  }
}

