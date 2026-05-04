function StatusCard({ title, status, description }) {
  return (
    <section className="panel status-panel">
      <div className="status-card-top">
        <p className="panel-label">{title}</p>
        <span className={`status-dot status-dot-${status}`} aria-hidden="true" />
      </div>
      <div className="status-row">
        <span className={`status-pill status-${status}`}>{status}</span>
      </div>
      <p className="muted-text">{description}</p>
    </section>
  );
}

export default StatusCard;
