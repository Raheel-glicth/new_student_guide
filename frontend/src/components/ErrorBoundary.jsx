import { Component } from "react";

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error, info) {
    console.error("ui_boundary_error", error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <main className="page-shell">
          <section className="panel failure-panel">
            <p className="panel-label">Recovery</p>
            <h1>Something in the interface crashed.</h1>
            <p className="muted-text">
              Refresh the page. If it happens again, the backend request ID in the
              failed call can help trace the issue.
            </p>
            <button
              type="button"
              className="primary-button"
              onClick={() => window.location.reload()}
            >
              Reload app
            </button>
          </section>
        </main>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
