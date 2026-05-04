function findNextTask(roadmap) {
  if (!roadmap) {
    return null;
  }

  for (const week of roadmap.weeks) {
    for (const task of week.tasks) {
      if (task.status !== "done") {
        return { week, task };
      }
    }
  }

  return null;
}

function ProgressPanel({ dashboard }) {
  const summary = dashboard?.progressSummary;
  const roadmap = dashboard?.roadmap;
  const nextTask = findNextTask(roadmap);

  if (!summary || !roadmap) {
    return (
      <section className="panel empty-panel">
        <div className="panel-header">
          <p className="panel-label">Momentum System</p>
          <h2>Progress Tracking</h2>
        </div>
        <p className="muted-text">
          Once the roadmap is generated, this section will show completion,
          in-progress tasks, and the highest-leverage next step.
        </p>
      </section>
    );
  }

  return (
    <section className="panel">
      <div className="panel-header split-header">
        <div>
          <p className="panel-label">Momentum System</p>
          <h2>Progress Tracking</h2>
        </div>
        <div className="completion-ring" style={{ "--completion": `${summary.completionRate}%` }}>
          <span>{summary.completionRate}%</span>
        </div>
      </div>

      <div className="progress-rail progress-rail-large" aria-hidden="true">
        <span style={{ width: `${summary.completionRate}%` }} />
      </div>

      <div className="metric-grid">
        <article className="metric-card">
          <span>Completion</span>
          <strong>{summary.completionRate}%</strong>
        </article>
        <article className="metric-card">
          <span>Done</span>
          <strong>{summary.completedTasks}</strong>
        </article>
        <article className="metric-card">
          <span>In Progress</span>
          <strong>{summary.inProgressTasks}</strong>
        </article>
        <article className="metric-card">
          <span>Pending</span>
          <strong>{summary.pendingTasks}</strong>
        </article>
      </div>

      {nextTask ? (
        <div className="next-task-card">
          <p className="panel-label">Highest-Leverage Next Task</p>
          <h3>
            Week {nextTask.week.week}: {nextTask.task.title}
          </h3>
          <p className="muted-text">{nextTask.task.description}</p>
        </div>
      ) : (
        <div className="next-task-card">
          <p className="panel-label">Roadmap Status</p>
          <h3>Current roadmap completed</h3>
          <p className="muted-text">
            You have finished every tracked task in the roadmap. The next phase is
            extending the system with a stronger project or career sprint.
          </p>
        </div>
      )}
    </section>
  );
}

export default ProgressPanel;
