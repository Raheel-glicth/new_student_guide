function LoadingSkeleton({ title = "Loading workspace" }) {
  return (
    <section className="panel skeleton-panel" aria-busy="true">
      <div>
        <p className="panel-label">Preparing</p>
        <h2>{title}</h2>
      </div>
      <div className="skeleton-line skeleton-line-wide" />
      <div className="skeleton-grid">
        <span />
        <span />
        <span />
      </div>
    </section>
  );
}

export default LoadingSkeleton;
