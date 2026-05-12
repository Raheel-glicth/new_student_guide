import { useEffect, useState } from "react";
import QuestionnairePage from "../features/questionnaire/QuestionnairePage";
import RoadmapPreview from "../features/roadmap/RoadmapPreview";
import ProgressPanel from "../features/progress/ProgressPanel";
import MentorPanel from "../features/mentor/MentorPanel";
import StatusCard from "../components/StatusCard";
import LoadingSkeleton from "../components/LoadingSkeleton";
import { askMentor, getHealth, getRoadmap, submitIntake, updateProgress } from "../services/api";

const productSignals = [
  { label: "Decision confidence", value: "Career fit" },
  { label: "Learning sprint", value: "6 weeks" },
  { label: "Proof of work", value: "Portfolio" },
];

const activationSteps = [
  "Map behavior",
  "Reveal best-fit track",
  "Ship weekly proof",
];

function buildWelcomeMentorState(dashboard) {
  if (!dashboard?.roadmap || !dashboard?.recommendation?.primaryTrack) {
    return {
      focusArea: "Welcome",
      actionItems: [],
      conversation: [],
    };
  }

  return {
    focusArea: "Onboarding",
    actionItems: [
      "Generate the roadmap and start with the first unfinished task",
      "Use the progress buttons to keep the plan honest",
      "Ask the mentor whenever you need focus or next-step clarity",
    ],
    conversation: [
      {
        role: "assistant",
        message: `You are tracking toward ${dashboard.recommendation.primaryTrack.name}. I can now coach your next move using the roadmap and your progress.`,
      },
    ],
  };
}

function AppShell() {
  const [health, setHealth] = useState({
    loading: true,
    status: "checking",
    message: "Connecting to backend...",
  });
  const [dashboard, setDashboard] = useState({
    profile: null,
    recommendation: null,
    roadmap: null,
    progressSummary: null,
  });
  const [pageState, setPageState] = useState({
    loading: true,
    submitting: false,
    savingTaskKey: "",
    mentorLoading: false,
    notice: "",
  });
  const [mentorState, setMentorState] = useState(buildWelcomeMentorState(null));
  const primaryTrack = dashboard.recommendation?.primaryTrack;
  const progressRate = dashboard.progressSummary?.completionRate || 0;

  useEffect(() => {
    let isMounted = true;

    async function loadApp() {
      try {
        const [healthData, roadmapData] = await Promise.all([getHealth(), getRoadmap()]);

        if (!isMounted) {
          return;
        }

        setHealth({
          loading: false,
          status: healthData.status,
          message: `${healthData.service} is ${healthData.database}`,
        });
        setDashboard({
          profile: roadmapData.profile || null,
          recommendation: roadmapData.recommendation || null,
          roadmap: roadmapData.roadmap || null,
          progressSummary: roadmapData.progressSummary || null,
        });
        setMentorState(buildWelcomeMentorState(roadmapData));
        setPageState((current) => ({ ...current, loading: false }));
      } catch (error) {
        if (!isMounted) {
          return;
        }

        setHealth({
          loading: false,
          status: "offline",
          message: "Backend not reachable yet. Start Flask on port 5000.",
        });
        setPageState((current) => ({
          ...current,
          loading: false,
          notice: error.message,
        }));
      }
    }

    loadApp();

    return () => {
      isMounted = false;
    };
  }, []);

  async function refreshDashboard() {
    const roadmapData = await getRoadmap();
    setDashboard({
      profile: roadmapData.profile || null,
      recommendation: roadmapData.recommendation || null,
      roadmap: roadmapData.roadmap || null,
      progressSummary: roadmapData.progressSummary || null,
    });
    return roadmapData;
  }

  async function handleIntakeSubmit(payload) {
    setPageState((current) => ({ ...current, submitting: true, notice: "" }));
    try {
      const response = await submitIntake(payload);
      setDashboard(response.dashboard);
      setMentorState(buildWelcomeMentorState(response.dashboard));
    } catch (error) {
      setPageState((current) => ({ ...current, notice: error.message }));
    } finally {
      setPageState((current) => ({ ...current, submitting: false }));
    }
  }

  async function handleTaskStatusChange(payload) {
    setPageState((current) => ({
      ...current,
      savingTaskKey: payload.taskKey,
      notice: "",
    }));
    try {
      await updateProgress(payload);
      const refreshed = await refreshDashboard();
      setMentorState((current) =>
        current.conversation.length > 0 ? current : buildWelcomeMentorState(refreshed),
      );
    } catch (error) {
      setPageState((current) => ({ ...current, notice: error.message }));
    } finally {
      setPageState((current) => ({ ...current, savingTaskKey: "" }));
    }
  }

  async function handleMentorMessage(message) {
    setPageState((current) => ({ ...current, mentorLoading: true, notice: "" }));
    try {
      const response = await askMentor({ message });
      setMentorState({
        focusArea: response.focusArea,
        actionItems: response.actionItems || [],
        conversation: response.conversation || [],
      });
    } catch (error) {
      setPageState((current) => ({ ...current, notice: error.message }));
    } finally {
      setPageState((current) => ({ ...current, mentorLoading: false }));
    }
  }

  return (
    <div className="page-shell">
      <header className="hero">
        <div className="hero-copy hero-visual">
          <div className="hero-content">
            <p className="eyebrow">Student Career Intelligence</p>
            <h1>Stop guessing. Build the career path that fits how you actually work.</h1>
            <p className="hero-text">
              A decision engine for students that turns behavior, interests, and weekly
              capacity into a clear track, a six-week roadmap, and mentor-guided momentum.
            </p>

            <div className="hero-actions">
              <a className="primary-button hero-link" href="#discovery">
                Start discovery
              </a>
              <a className="secondary-button hero-link" href="#roadmap">
                View roadmap
              </a>
            </div>

            <div className="signal-grid" aria-label="Product proof points">
              {productSignals.map((signal) => (
                <div key={signal.label} className="signal-card">
                  <span>{signal.label}</span>
                  <strong>{signal.value}</strong>
                </div>
              ))}
            </div>
          </div>

          <div className="hero-insight-card" aria-label="Current career signal">
            <span className="insight-kicker">Live match</span>
            <strong>{primaryTrack?.name || "Awaiting discovery"}</strong>
            <p>
              {primaryTrack?.summary ||
                "Answer the discovery flow to unlock a personalized career direction."}
            </p>
            <div className="confidence-meter">
              <span style={{ width: `${Math.max(progressRate, primaryTrack ? 18 : 6)}%` }} />
            </div>
          </div>
        </div>

        <div className="hero-stack">
          <div className="activation-card">
            <p className="panel-label">Activation Loop</p>
            {activationSteps.map((step, index) => (
              <div key={step} className="activation-step">
                <span>{index + 1}</span>
                <p>{step}</p>
              </div>
            ))}
          </div>
          <StatusCard
            title="Backend Connection"
            status={health.status}
            description={health.loading ? "Waiting for response..." : health.message}
          />
          <StatusCard
            title="Product State"
            status={dashboard.roadmap ? "ok" : "checking"}
            description={
              dashboard.roadmap
                ? `${dashboard.recommendation?.primaryTrack?.name || "Career plan"} roadmap active`
                : pageState.loading
                  ? "Loading saved dashboard..."
                  : "Waiting for intake to generate the first roadmap"
            }
          />
        </div>
      </header>

      <main className="dashboard-grid">
        {pageState.notice ? (
          <div className="app-notice" role="alert">
            {pageState.notice}
          </div>
        ) : null}
        <section className="strategy-strip" aria-label="Product strategy">
          <article>
            <span>Core problem</span>
            <p>Students do not need more generic career advice. They need a fast way to identify fit, reduce anxiety, and convert interest into proof.</p>
          </article>
          <article>
            <span>Psychology used</span>
            <p>Identity framing, visible progress, small commitments, feedback loops, and a clear next action after every decision.</p>
          </article>
          <article>
            <span>Retention loop</span>
            <p>Return each week, update tasks, ask the mentor, and watch ambiguity turn into visible career evidence.</p>
          </article>
        </section>
        {pageState.loading ? (
          <>
            <LoadingSkeleton title="Loading discovery workspace" />
            <LoadingSkeleton title="Loading roadmap state" />
          </>
        ) : (
          <>
            <QuestionnairePage
              id="discovery"
              onSubmit={handleIntakeSubmit}
              submitting={pageState.submitting}
              existingProfile={dashboard.profile}
              recommendation={dashboard.recommendation}
            />
            <RoadmapPreview
              id="roadmap"
              dashboard={dashboard}
              onTaskStatusChange={handleTaskStatusChange}
              savingTaskKey={pageState.savingTaskKey}
            />
            <ProgressPanel dashboard={dashboard} />
            <MentorPanel
              dashboard={dashboard}
              mentorState={mentorState}
              onSendMessage={handleMentorMessage}
              loading={pageState.mentorLoading}
            />
          </>
        )}
      </main>
    </div>
  );
}

export default AppShell;
