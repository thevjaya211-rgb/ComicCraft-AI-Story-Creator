async function generateStory() {
    const prompt = document.getElementById("prompt").value;
    const result = document.getElementById("result");

    if (!prompt) {
        result.innerText = "Please enter a comic idea.";
        return;
    }

    result.innerText = "Generating...";

    try {
        const response = await fetch("http://127.0.0.1:8000/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                prompt: prompt,
                provider: "gemini",
                type: "text"
            })
        });

        const text = await response.text();

        console.log("STATUS:", response.status);
        console.log("RESPONSE:", text);

        if (!text) {
            result.innerText = "Empty response from server";
            return;
        }

        const data = JSON.parse(text);

        result.innerText = data.result || "No result received";

    } catch (error) {
        result.innerText = "Error: " + error.message;
    }
}