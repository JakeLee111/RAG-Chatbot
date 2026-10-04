import PredictionForm from "./PredictionForm";
import Chatbot from "./Chatbot";
import "./index.css";

export default function App() {
  return (
    <main className="page">
      <section className="hero">
        <span className="badge">Heart Health Assistant</span>

        <h1>Understand your heart health more clearly.</h1>

        <p>
          Use the prediction tool to estimate heart disease probability,
          then ask the chatbot questions about heart health.
        </p>
      </section>

      <section className="content">
        <PredictionForm />
      </section>

      <footer>
        This project is for educational purposes only and is not medical advice.
      </footer>

      <Chatbot />
    </main>
  );
}