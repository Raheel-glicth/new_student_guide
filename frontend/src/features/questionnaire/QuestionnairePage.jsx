import { useEffect, useState } from "react";
import {
  educationOptions,
  initialIntakeForm,
  interestOptions,
  questionnaireSteps,
} from "../../data/questionnaire";

function QuestionnairePage({ id, onSubmit, submitting, existingProfile, recommendation }) {
  const [stepIndex, setStepIndex] = useState(0);
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

  const currentStep = questionnaireSteps[stepIndex];
  const isLastStep = stepIndex === questionnaireSteps.length - 1;
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

  function updateAnswer(questionId, value) {
    setForm((current) => ({
      ...current,
      answers: {
        ...current.answers,
        [questionId]: value,
      },
    }));
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

  function validateStep() {
    if (currentStep.id === "profile") {
      if (!form.fullName.trim()) {
        return "Enter the student name.";
      }
      if (!form.educationLevel) {
        return "Choose the current education level.";
      }
      if (form.interestAreas.length === 0) {
        return "Select at least one interest area.";
      }
    }

    if (currentStep.questions) {
      const unanswered = currentStep.questions.find(
        (question) => !form.answers[question.id],
      );
      if (unanswered) {
        return `Answer: ${unanswered.label}`;
      }
    }

    if (isLastStep && !form.goals.trim()) {
      return "Write one short career goal so the roadmap has direction.";
    }

    return "";
  }

  function handleNextStep() {
    const validationError = validateStep();
    if (validationError) {
      setError(validationError);
      return;
    }

    setError("");
    setStepIndex((current) => Math.min(current + 1, questionnaireSteps.length - 1));
  }

  function handlePreviousStep() {
    setError("");
    setStepIndex((current) => Math.max(current - 1, 0));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    const validationError = validateStep();
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
        {questionnaireSteps.map((step, index) => (
          <button
            key={step.id}
            type="button"
            className={`step-pill ${index === stepIndex ? "step-pill-active" : ""}`}
            onClick={() => setStepIndex(index)}
          >
            <span>{index + 1}</span>
            {step.title}
          </button>
        ))}
      </div>

      <form className="questionnaire-form" onSubmit={handleSubmit}>
        <div className="step-card">
          <p className="step-heading">{currentStep.title}</p>
          <p className="muted-text">{currentStep.description}</p>

          {currentStep.id === "profile" && (
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

              <label className="field-block">
                <span>Education level</span>
                <select
                  className="text-input"
                  value={form.educationLevel}
                  onChange={(event) =>
                    setForm((current) => ({
                      ...current,
                      educationLevel: event.target.value,
                    }))
                  }
                >
                  <option value="">Select one</option>
                  {educationOptions.map((option) => (
                    <option key={option} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              </label>

              <div className="field-block field-block-full">
                <span>Interest areas</span>
                <div className="chip-grid">
                  {interestOptions.map((option) => (
                    <button
                      key={option}
                      type="button"
                      className={`choice-chip ${
                        form.interestAreas.includes(option) ? "choice-chip-active" : ""
                      }`}
                      onClick={() => toggleInterest(option)}
                    >
                      {option}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {currentStep.questions?.map((question) => (
            <div key={question.id} className="question-block">
              <p className="question-title">{question.label}</p>
              <div className="option-grid">
                {question.options.map((option) => (
                  <button
                    key={option.value}
                    type="button"
                    className={`option-card ${
                      form.answers[question.id] === option.value ? "option-card-active" : ""
                      }`}
                      onClick={() => updateAnswer(question.id, option.value)}
                    >
                      <span className="option-marker" aria-hidden="true" />
                      <strong>{option.label}</strong>
                      <span>{option.description}</span>
                    </button>
                ))}
              </div>
            </div>
          ))}

          {isLastStep && (
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
            disabled={stepIndex === 0 || submitting}
          >
            Back
          </button>

          {!isLastStep ? (
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
