import { useState } from "react";
import { askChatbot } from "./api";

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  const [messages, setMessages] = useState([
    {
      role: "bot",
      text: "Hi, I can answer questions about heart disease.",
    },
  ]);

  async function sendMessage(event) {
    event.preventDefault();

    if (!question.trim() || loading) {
      return;
    }

    const currentQuestion = question.trim();

    setQuestion("");

    setMessages((oldMessages) => [
      ...oldMessages,
      {
        role: "user",
        text: currentQuestion,
      },
    ]);

    setLoading(true);

    try {
      const data = await askChatbot(currentQuestion);

      setMessages((oldMessages) => [
        ...oldMessages,
        {
          role: "bot",
          text: data.answer,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((oldMessages) => [
        ...oldMessages,
        {
          role: "bot",
          text: "I could not connect to the chatbot backend. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function formatBotAnswer(text) {
    if (!text) {
      return null;
    }

    const lines = text
      .replace(/\*\*/g, "")
      .split("\n")
      .map((line) => line.trim())
      .filter(Boolean);

    return lines.map((line, index) => {
      if (line.startsWith("- ")) {
        return <li key={index}>{line.substring(2)}</li>;
      }

      return <p key={index}>{line}</p>;
    });
  }

  return (
    <>
      {isOpen && (
        <section className="chat-widget">
          <div className="chat-header">
            <div className="chat-header-info">
              <div className="assistant-icon">♥</div>

              <div>
                <h3>Heart Assistant</h3>
                <span>AI health education assistant</span>
              </div>
            </div>

            <button
              className="chat-close"
              type="button"
              onClick={() => setIsOpen(false)}
            >
              ×
            </button>
          </div>

          <div className="chat-messages">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`message-row ${
                  message.role === "user" ? "user-row" : "bot-row"
                }`}
              >
                <div
                  className={`message-bubble ${
                    message.role === "user"
                      ? "user-bubble"
                      : "bot-bubble"
                  }`}
                >
                  {message.role === "bot" ? (
                    <div className="bot-answer">
                      {formatBotAnswer(message.text)}
                    </div>
                  ) : (
                    <p>{message.text}</p>
                  )}
                </div>
              </div>
            ))}

            {loading && (
              <div className="message-row bot-row">
                <div className="message-bubble bot-bubble">
                  <div className="typing">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
          </div>

          <form onSubmit={sendMessage} className="chat-input-area">
            <input
              type="text"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="Ask about heart disease..."
              disabled={loading}
            />

            <button type="submit" disabled={loading || !question.trim()}>
              Send
            </button>
          </form>
        </section>
      )}

      <button
        className="chat-toggle"
        type="button"
        onClick={() => setIsOpen((oldValue) => !oldValue)}
        aria-label="Open heart assistant"
      >
        {isOpen ? "×" : "♥"}
      </button>
    </>
  );
}