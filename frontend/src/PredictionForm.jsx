import { useState } from "react";
import { predictHeartDisease } from "./api";

export default function PredictionForm() {
  const [form, setForm] = useState({
    age: 50,
    sex: "M",
    chest_pain_type: "ASY",
    resting_bp: 120,
    cholesterol: 200,
    fasting_bs: 0,
    resting_ecg: "Normal",
    max_hr: 150,
    exercise_angina: "N",
    oldpeak: 0,
    st_slope: "Up",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((oldForm) => ({
      ...oldForm,
      [name]: value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setLoading(true);
    setError("");

    const payload = {
      age: Number(form.age),
      sex: form.sex,
      chest_pain_type: form.chest_pain_type,
      resting_bp: Number(form.resting_bp),
      cholesterol: Number(form.cholesterol),
      fasting_bs: Number(form.fasting_bs),
      resting_ecg: form.resting_ecg,
      max_hr: Number(form.max_hr),
      exercise_angina: form.exercise_angina,
      oldpeak: Number(form.oldpeak),
      st_slope: form.st_slope,
    };

    try {
      const data = await predictHeartDisease(payload);
      setResult(data);
    } catch (error) {
      console.error(error);
      setError("Prediction failed. Please check that the backend is running.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <section className="prediction-card">
        <div className="card-heading">
          <div>
            <span className="section-label">Prediction Tool</span>
            <h2>Heart Disease Prediction</h2>
          </div>

          <p>
            Enter the patient's information below to estimate heart disease
            probability.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="form-grid">
          <label>
            Age
            <input
              type="number"
              name="age"
              value={form.age}
              onChange={handleChange}
              min="1"
              max="120"
              required
            />
          </label>

          <label>
            Sex
            <select name="sex" value={form.sex} onChange={handleChange}>
              <option value="M">Male</option>
              <option value="F">Female</option>
            </select>
          </label>

          <label>
            Chest Pain Type
            <select
              name="chest_pain_type"
              value={form.chest_pain_type}
              onChange={handleChange}
            >
              <option value="ATA">ATA</option>
              <option value="NAP">NAP</option>
              <option value="ASY">ASY</option>
              <option value="TA">TA</option>
            </select>
          </label>

          <label>
            Resting Blood Pressure
            <input
              type="number"
              name="resting_bp"
              value={form.resting_bp}
              onChange={handleChange}
              required
            />
          </label>

          <label>
            Cholesterol
            <input
              type="number"
              name="cholesterol"
              value={form.cholesterol}
              onChange={handleChange}
              required
            />
          </label>

          <label>
            Fasting Blood Sugar
            <select
              name="fasting_bs"
              value={form.fasting_bs}
              onChange={handleChange}
            >
              <option value="0">0</option>
              <option value="1">1</option>
            </select>
          </label>

          <label>
            Resting ECG
            <select
              name="resting_ecg"
              value={form.resting_ecg}
              onChange={handleChange}
            >
              <option value="Normal">Normal</option>
              <option value="ST">ST</option>
              <option value="LVH">LVH</option>
            </select>
          </label>

          <label>
            Maximum Heart Rate
            <input
              type="number"
              name="max_hr"
              value={form.max_hr}
              onChange={handleChange}
              required
            />
          </label>

          <label>
            Exercise Angina
            <select
              name="exercise_angina"
              value={form.exercise_angina}
              onChange={handleChange}
            >
              <option value="N">No</option>
              <option value="Y">Yes</option>
            </select>
          </label>

          <label>
            Oldpeak
            <input
              type="number"
              name="oldpeak"
              value={form.oldpeak}
              onChange={handleChange}
              step="0.1"
              required
            />
          </label>

          <label>
            ST Slope
            <select
              name="st_slope"
              value={form.st_slope}
              onChange={handleChange}
            >
              <option value="Up">Up</option>
              <option value="Flat">Flat</option>
              <option value="Down">Down</option>
            </select>
          </label>

          <button className="predict-button" type="submit" disabled={loading}>
            {loading ? "Calculating..." : "Predict Heart Disease"}
          </button>
        </form>

        {error && <p className="error-message">{error}</p>}
      </section>

      {result && (
        <div className="modal-overlay">
          <div className="result-modal">
            <button
              className="modal-close"
              onClick={() => setResult(null)}
              type="button"
            >
              ×
            </button>

            <span className="modal-label">
              Estimated heart disease probability
            </span>

            <h2 className="result-percentage">
              {(result.probability * 100).toFixed(1)}%
            </h2>

            <p
              className={
                result.prediction === 1
                  ? "risk-status higher-risk"
                  : "risk-status lower-risk"
              }
            >
              {result.prediction === 1 ? "Higher Risk" : "Lower Risk"}
            </p>

            <p className="result-note">
              This result is generated by a machine learning model and is for
              educational purposes only. It is not a medical diagnosis.
            </p>

            <button
              className="modal-button"
              onClick={() => setResult(null)}
              type="button"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </>
  );
}