export async function predictHeartDisease(patient) {
  const response = await fetch("/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(patient),
  });

  if (!response.ok) {
    throw new Error("Prediction request failed.");
  }

  return response.json();
}

export async function askChatbot(question) {
  const response = await fetch("/ask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question: question,
    }),
  });

  if (!response.ok) {
    throw new Error("Chatbot request failed.");
  }

  return response.json();
}

export async function checkHealth() {
  const response = await fetch("/health");

  if (!response.ok) {
    throw new Error("Backend is not available.");
  }

  return response.json();
}