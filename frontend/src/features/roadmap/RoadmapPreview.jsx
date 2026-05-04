import { statusOptions } from "../../data/questionnaire";
import { useEffect, useState } from "react";

function RoadmapPreview({ id, dashboard, onTaskStatusChange, savingTaskKey }) {
  const roadmap = dashboard?.roadmap;
  const recommendation = dashboard?.recommendation;
  const [taskNotes, setTaskNotes] = useState({});

  useEffect(() => {
    if (!roadmap) {
      return;
    }

    const nextNotes = {};
    roadmap.weeks.forEach((week) => {
      week.tasks.forEach((task) => {
        nextNotes[task.key] = task.notes || "";
      });
    });
    setTaskNotes(nextNotes);
  }, [roadmap]);

  if (!roadmap) {
    return (
      <section id={id} className="panel empty-panel">
        <div className="panel-header">
          <p className="panel-label">Roadmap Generator</p>
          <h2>Roadmap Generator</h2>
        </div>
        <p className="muted-text">
          Complete the intake flow and the product will generate a six-week roadmap
          with weekly outcomes and trackable tasks.
        </p>
      </section>
    );
  }

  return (
    <section id={id} className="panel roadmap-panel">
      <div className="panel-header roadmap-header">
        <div>
          <p className="panel-label">Personalized Sprint</p>
          <h2>{roadmap.title}</h2>
        </div>
        <span className="match-badge">
          Best Match: {recommendation?.primaryTrack?.name || "Career Match"}
        </span>
      </div>

      <p className="muted-text">{roadmap.summary}</p>

      {recommendation?.primaryTrack ? (
        <div className="recommendation-card">
          <p className="panel-label">Why this direction works</p>
          <h3>{recommendation.primaryTrack.name}</h3>
          <p className="muted-text">{recommendation.primaryTrack.summary}</p>
          <div className="mini-chip-row">
            {recommendation.primaryTrack.tools.map((tool) => (
              <span key={tool} className="mini-chip">
                {tool}
              </span>
            ))}
          </div>
        </div>
      ) : null}

      <div className="timeline-list">
        {roadmap.weeks.map((week) => (
          <article key={week.week} className="timeline-item week-card">
            <div className="week-header">
              <div>
                <span className="timeline-week">Week {week.week}</span>
                <h3>{week.theme}</h3>
              </div>
              <p className="week-outcome">{week.outcome}</p>
            </div>

            <div className="task-list">
              {week.tasks.map((task) => (
                <div key={task.key} className="task-card">
                  <div className="task-main">
                    <div>
                      <p className="task-title">{task.title}</p>
                      <p className="muted-text task-description">{task.description}</p>
                    </div>
                    <span className={`task-status status-${task.status}`}>
                      {task.status.replace("_", " ")}
                    </span>
                  </div>

                  <div className="status-actions">
                    {statusOptions.map((status) => (
                      <button
                        key={status.value}
                        type="button"
                        className={`status-button ${
                          task.status === status.value ? "status-button-active" : ""
                        }`}
                        disabled={savingTaskKey === task.key}
                        onClick={() =>
                          onTaskStatusChange({
                            roadmapId: roadmap.id,
                            weekNumber: week.week,
                            taskKey: task.key,
                            taskTitle: task.title,
                            status: status.value,
                            notes: taskNotes[task.key] || "",
                          })
                        }
                      >
                        {savingTaskKey === task.key && task.status !== status.value
                          ? "Saving..."
                          : status.label}
                      </button>
                    ))}
                  </div>

                  <label className="task-note-field">
                    <span>Progress note</span>
                    <textarea
                      className="text-area compact-text-area"
                      rows="2"
                      value={taskNotes[task.key] || ""}
                      onChange={(event) =>
                        setTaskNotes((current) => ({
                          ...current,
                          [task.key]: event.target.value,
                        }))
                      }
                      placeholder="Add blockers, proof links, or what changed."
                    />
                  </label>
                </div>
              ))}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

export default RoadmapPreview;
