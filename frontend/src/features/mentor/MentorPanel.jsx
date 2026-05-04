import { useState } from "react";

function MentorPanel({ dashboard, mentorState, onSendMessage, loading }) {
  const [message, setMessage] = useState("");
  const hasRoadmap = Boolean(dashboard?.roadmap);
  const conversation = mentorState?.conversation || [];

  async function handleSubmit(event) {
    event.preventDefault();
    if (!message.trim()) {
      return;
    }

    await onSendMessage(message);
    setMessage("");
  }

  return (
    <section className="panel mentor-panel">
      <div className="panel-header split-header">
        <div>
          <p className="panel-label">Guidance Layer</p>
          <h2>AI Mentor</h2>
        </div>
        <span className={`mentor-state ${hasRoadmap ? "mentor-state-active" : ""}`}>
          {hasRoadmap ? "Ready" : "Locked"}
        </span>
      </div>

      <div className="mentor-topbar">
        <span className="match-badge">
          Focus: {mentorState?.focusArea || "Career Guidance"}
        </span>
      </div>

      <div className="mentor-conversation">
        {conversation.length === 0 ? (
          <div className="message-bubble assistant-bubble">
            Generate a roadmap first. Then I will turn uncertainty into one concrete
            move using the student profile, roadmap, and current progress.
          </div>
        ) : (
          conversation.map((entry, index) => (
            <div
              key={`${entry.role}-${index}`}
              className={`message-bubble ${
                entry.role === "assistant" ? "assistant-bubble" : "user-bubble"
              }`}
            >
              {entry.message}
            </div>
          ))
        )}
      </div>

      {mentorState?.actionItems?.length ? (
        <div className="action-list-card">
          <p className="panel-label">Mentor Action Plan</p>
          <ul className="simple-list">
            {mentorState.actionItems.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      ) : null}

      <form className="mentor-form" onSubmit={handleSubmit}>
        <textarea
          className="text-area"
          rows="4"
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          disabled={!hasRoadmap || loading}
          placeholder={
            hasRoadmap
              ? "Ask for clarity, motivation, next steps, portfolio advice, or time management."
              : "Generate a roadmap first to activate the mentor."
          }
        />
        <button
          type="submit"
          className="primary-button"
          disabled={!hasRoadmap || loading || !message.trim()}
        >
          {loading ? "Thinking..." : "Ask mentor"}
        </button>
      </form>
    </section>
  );
}

export default MentorPanel;
