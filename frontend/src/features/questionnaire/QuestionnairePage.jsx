import { useEffect, useState } from "react";
import {
  educationOptions,
  initialIntakeForm,
  interestOptions,
  questionnaireSteps,
} from "../../data/questionnaire";

const discoveryQuestions = questionnaireSteps.flatMap((step) =>
  (step.questions || []).map((question) => ({
    ...question,
    phaseTitle: step.title,
  })),
);

const discoveryDeck = [
  {
    id: "profile-basics",
    kind: "profile",
    title: "First, who are we guiding?",
    description: "Keep this simple. The roadmap should feel personal, not like a generic quiz.",
  },
  {
    id: "interest-fit",
    kind: "interests",
    title: "What naturally pulls your attention?",
    description: "Pick the fields you would actually explore when no one is forcing you.",
  },
  ...discoveryQuestions.map((question) => ({
    id: question.id,
    kind: "question",
    question,
    title: question.label,
    description: question.phaseTitle,
  })),
  {
    id: "career-goal",
    kind: "goal",
    title: "What should this plan help you become?",
    description: "One honest sentence is enough. Specific beats impressive.",
  },
];

function QuestionnairePage({ id, onSubmit, submitting, existingProfile, recommendation }) {
  const [deckIndex, setDeckIndex] = useState(0);
  const [form, setForm] = useState(initialIntakeForm);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!existingProfile) {
      return;
    }

    setForm((current) => ({
      ...current,
      fullName: existingProfile.fullName || current.fullName,
      educationLevel: existingProfile.educationLevel || current.educationLevel,
      interestAreas:
        existingProfile.interestAreas?.length > 0
          ? existingProfile.interestAreas
          : current.interestAreas,
      goals: existingProfile.goals || current.goals,
      answers: {
        ...current.answers,
        ...existingProfile.answers,
      },
    }));
  }, [existingProfile]);

  const currentCard = discoveryDeck[deckIndex];
  const isLastCard = deckIndex === discoveryDeck.length - 1;
  const answeredCount = Object.values(form.answers).filter(Boolean).length;
  const totalAnswerCount = Object.keys(form.answers).length;
  const profileComplete =
    Boolean(form.fullName.trim()) &&
    Boolean(form.educationLevel) &&
    form.interestAreas.length > 0;
  const completionPercent = Math.round(
    ((answeredCount + (profileComplete ? 1 : 0) + (form.goals.trim() ? 1 : 0)) /
      (totalAnswerCount + 2)) *
      100,
  );
  const currentAnswer =
    currentCard.kind === "question" ? form.answers[currentCard.question.id] : "";
  const phaseName =
    currentCard.kind === "question" ? currentCard.description : "Student Signal";

  function moveToNextCard() {
    setDeckIndex((current) => Math.min(current + 1, discoveryDeck.length - 1));
  }

  function updateAnswer(questionId, value, shouldAdvance = false) {
    setForm((current) => ({
      ...current,
      answers: {
        ...current.answers,
        [questionId]: value,
      },
    }));
    setError("");

    if (shouldAdvance && deckIndex < discoveryDeck.length - 1) {
      window.setTimeout(moveToNextCard, 140);
    }
  }

  function toggleInterest(value) {
    setForm((current) => {
      const alreadySelected = current.interestAreas.includes(value);
      return {
        ...current,
        interestAreas: alreadySelected
          ? current.interestAreas.filter((item) => item !== value)
          : [...current.interestAreas, value],
      };
    });
  }

  function validateCurrentCard() {
    if (currentCard.kind === "profile") {
      if (!form.fullName.trim()) {
        return "Enter the student name.";
      }
      if (!form.educationLevel) {
        return "Choose the current education level.";
      }
    }

    if (currentCard.kind === "interests" && form.interestAreas.length === 0) {
      return "Select at least one interest area.";
    }

    if (currentCard.kind === "question" && !form.answers[currentCard.question.id]) {
      return "Choose the option that feels closest.";
    }

    if (currentCard.kind === "goal" && !form.goals.trim()) {
      return "Write one short career goal so the roadmap has direction.";
    }

    return "";
  }

  function handleNextStep() {
    const validationError = validateCurrentCard();
    if (validationError) {
      setError(validationError);
      return;
    }

    setError("");
    moveToNextCard();
  }

  function handlePreviousStep() {
    setError("");
    setDeckIndex((current) => Math.max(current - 1, 0));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    const validationError = validateCurrentCard();
    if (validationError) {
      setError(validationError);
      return;
    }

    setError("");
    await onSubmit(form);
  }

  return (
    <section id={id} className="panel questionnaire-panel">
      <div className="panel-header split-header">
        <div>
          <p className="panel-label">Decision Engine</p>
          <h2>Student Discovery Flow</h2>
        </div>
        <div className="completion-chip">{completionPercent}% complete</div>
      </div>

      <div className="progress-rail" aria-hidden="true">
        <span style={{ width: `${completionPercent}%` }} />
      </div>

      <div className="stepper">
        {discoveryDeck.map((card, index) => (
          <button
            key={card.id}
            type="button"
            className={`step-pill ${index === deckIndex ? "step-pill-active" : ""}`}
            onClick={() => setDeckIndex(index)}
            aria-label={`Go to discovery card ${index + 1}: ${card.title}`}
          >
            <span>{index + 1}</span>
            {card.kind === "question" ? card.question.phaseTitle : card.title}
          </button>
        ))}
      </div>

      <form className="questionnaire-form" onSubmit={handleSubmit}>
        <div className="step-card decision-card">
          <div className="decision-card-header">
            <p className="panel-label">{phaseName}</p>
            <h3>{currentCard.title}</h3>
            <p className="muted-text">{currentCard.description}</p>
          </div>

          {currentCard.kind === "profile" && (
            <div className="form-grid">
              <label className="field-block">
                <span>Student name</span>
                <input
                  className="text-input"
                  value={form.fullName}
                  onChange={(event) =>
                    setForm((current) => ({
                      ...current,
                      fullName: event.target.value,
                    }))
                  }
                  placeholder="Aarav Sharma"
                />
              </label>

              <div className="field-block">
                <span>Education level</span>
                <div className="selectable-list">
                  {educationOptions.map((option) => (
                    <button
                      key={option}
                      type="button"
                      className={`choice-chip ${
                        form.educationLevel === option ? "choice-chip-active" : ""
                      }`}
                      onClick={() => {
                        setError("");
                        setForm((current) => ({
                          ...current,
                          educationLevel: option,
                        }));
                      }}
                    >
                      {option}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {currentCard.kind === "interests" && (
            <div className="interest-stage">
              <div className="option-grid interest-grid">
                {interestOptions.map((option) => (
                  <button
                    key={option}
                    type="button"
                    className={`option-card interest-option ${
                      form.interestAreas.includes(option) ? "option-card-active" : ""
                      }`}
                    onClick={() => {
                      setError("");
                      toggleInterest(option);
                    }}
                  >
                      <span className="option-marker" aria-hidden="true" />
                    <strong>{option}</strong>
                    <span>
                      {form.interestAreas.includes(option)
                        ? "Selected for your recommendation signal."
                        : "Tap to include this in your career fit map."}
                    </span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {currentCard.kind === "question" && (
            <div className="question-block question-focus">
              <div className="option-grid question-option-grid">
                {currentCard.question.options.map((option) => (
                  <button
                    key={option.value}
                    type="button"
                    className={`option-card ${
                      currentAnswer === option.value ? "option-card-active" : ""
                    }`}
                    onClick={() => updateAnswer(currentCard.question.id, option.value, true)}
                  >
                    <span className="option-marker" aria-hidden="true" />
                    <strong>{option.label}</strong>
                    <span>{option.description}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {currentCard.kind === "goal" && (
            <label className="field-block field-block-full">
              <span>Career goal</span>
              <textarea
                className="text-area"
                rows="5"
                value={form.goals}
                onChange={(event) =>
                  setForm((current) => ({
                    ...current,
                    goals: event.target.value,
                  }))
                }
                placeholder="Example: I want a practical roadmap that helps me build one strong project and become internship-ready."
              />
            </label>
          )}

          {recommendation?.primaryTrack && (
            <div className="inline-recommendation">
              <p className="panel-label">Current Match</p>
              <h3>{recommendation.primaryTrack.name}</h3>
              <p className="muted-text">{recommendation.primaryTrack.summary}</p>
            </div>
          )}

          {error ? <p className="form-error">{error}</p> : null}
        </div>

        <div className="form-actions">
          <button
            type="button"
            className="secondary-button"
            onClick={handlePreviousStep}
            disabled={deckIndex === 0 || submitting}
          >
            Back
          </button>

          {!isLastCard ? (
            <button
              type="button"
              className="primary-button"
              onClick={handleNextStep}
              disabled={submitting}
            >
              Continue
            </button>
          ) : (
            <button type="submit" className="primary-button" disabled={submitting}>
              {submitting ? "Generating roadmap..." : "Generate roadmap"}
            </button>
          )}
        </div>
      </form>
    </section>
  );
}

export default QuestionnairePage;
