document.getElementById("meal-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = document.getElementById("meal-name").value;
    const description = document.getElementById("meal-description").value;

    const response = await fetch("/meals/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, description }),
    });

    const result = await response.json();
    alert(result.message);
});