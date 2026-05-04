export const interestOptions = [
  "AI/ML",
  "Cybersecurity",
  "Video Editing",
  "Data Science",
  "UI/UX Design",
  "Full Stack Development",
  "Digital Marketing",
];

export const educationOptions = [
  "School Student",
  "Diploma",
  "Undergraduate",
  "Postgraduate",
  "Self-Learner",
];

export const questionnaireSteps = [
  {
    id: "profile",
    title: "Student Profile",
    description: "Capture the foundation before we score direction and generate a roadmap.",
    fields: ["fullName", "educationLevel", "interestAreas"],
  },
  {
    id: "behavior",
    title: "Behavior Mapping",
    description: "These questions identify the work patterns that genuinely match your energy.",
    questions: [
      {
        id: "workStyle",
        label: "Which type of work feels the most natural to you?",
        options: [
          {
            value: "intelligent_products",
            label: "Build intelligent products",
            description: "Apps, automation, or smart systems that solve hard problems.",
          },
          {
            value: "protect_systems",
            label: "Protect systems",
            description: "Security thinking, investigation, and fixing vulnerabilities.",
          },
          {
            value: "visual_storytelling",
            label: "Create visual stories",
            description: "Editing, pacing, and polishing content people want to watch.",
          },
          {
            value: "analyze_patterns",
            label: "Analyze patterns",
            description: "Turning data into insight, trends, and decision-making.",
          },
          {
            value: "design_experiences",
            label: "Design experiences",
            description: "Improving how products look, feel, and guide users.",
          },
          {
            value: "ship_products_fast",
            label: "Ship practical products",
            description: "Turn ideas into working web products quickly.",
          },
        ],
      },
      {
        id: "energySource",
        label: "What gives you energy when a project gets difficult?",
        options: [
          {
            value: "solving_logic",
            label: "Solving hard logic problems",
            description: "You enjoy structured thinking and technical puzzles.",
          },
          {
            value: "finding_risks",
            label: "Finding what could break",
            description: "You naturally spot weaknesses, edge cases, and threats.",
          },
          {
            value: "creative_expression",
            label: "Creative expression",
            description: "You stay motivated when the output feels visual or expressive.",
          },
          {
            value: "discovering_insights",
            label: "Discovering insights",
            description: "You like making sense of information and hidden patterns.",
          },
          {
            value: "helping_users",
            label: "Helping users succeed",
            description: "You care deeply about clarity, ease, and usefulness.",
          },
          {
            value: "building_public_work",
            label: "Publishing real work",
            description: "Momentum comes from creating things the world can see.",
          },
        ],
      },
      {
        id: "toolPreference",
        label: "Which tool universe are you most curious to master first?",
        options: [
          {
            value: "python_models",
            label: "Python and model tools",
            description: "Coding, experiments, automation, and intelligent systems.",
          },
          {
            value: "networks_security",
            label: "Networks and security tools",
            description: "Monitoring, testing, and protecting digital systems.",
          },
          {
            value: "editing_timeline",
            label: "Editing timeline and motion tools",
            description: "Video cutting, transitions, sound, and story flow.",
          },
          {
            value: "dashboards_spreadsheets",
            label: "Dashboards and analysis tools",
            description: "Data organization, visualization, and decision support.",
          },
          {
            value: "wireframes_prototypes",
            label: "Wireframes and prototypes",
            description: "Interface systems, user flows, and polished product thinking.",
          },
          {
            value: "frontend_backend",
            label: "Frontend and backend app tools",
            description: "You want to build working products end-to-end.",
          },
        ],
      },
    ],
  },
  {
    id: "operating-system",
    title: "Execution Style",
    description: "We use this to choose roadmap pace, task shape, and mentor advice.",
    questions: [
      {
        id: "learningStyle",
        label: "How do you learn fastest?",
        options: [
          {
            value: "project_based",
            label: "By building projects",
            description: "You understand things better when you create something real.",
          },
          {
            value: "challenge_based",
            label: "By solving challenges",
            description: "You like gamified problems and direct testing.",
          },
          {
            value: "visual_examples",
            label: "By seeing examples",
            description: "You absorb patterns through references and demonstrations.",
          },
          {
            value: "structured_curriculum",
            label: "By following a clear curriculum",
            description: "You prefer clean progression and organized lessons.",
          },
          {
            value: "feedback_loops",
            label: "By getting feedback quickly",
            description: "You improve fastest when you can iterate with input.",
          },
        ],
      },
      {
        id: "collaborationStyle",
        label: "What kind of working environment sounds best right now?",
        options: [
          {
            value: "independent_focus",
            label: "Deep independent focus",
            description: "You prefer to learn quietly and build on your own first.",
          },
          {
            value: "small_team",
            label: "A small focused team",
            description: "You like collaboration without too much noise.",
          },
          {
            value: "client_facing",
            label: "Direct client or audience work",
            description: "You want feedback from real people and visible outcomes.",
          },
          {
            value: "cross_functional",
            label: "Cross-functional product work",
            description: "You enjoy multiple roles working toward one launch.",
          },
        ],
      },
      {
        id: "weeklyCommitment",
        label: "How many focused hours can you realistically protect each week?",
        options: [
          {
            value: "4-6",
            label: "4 to 6 hours",
            description: "Light but sustainable momentum.",
          },
          {
            value: "7-10",
            label: "7 to 10 hours",
            description: "A strong balanced student pace.",
          },
          {
            value: "11-15",
            label: "11 to 15 hours",
            description: "An accelerated path with deeper weekly output.",
          },
          {
            value: "16+",
            label: "16+ hours",
            description: "An immersive sprint toward visible progress.",
          },
        ],
      },
      {
        id: "preferredOutcome",
        label: "What would feel like a win over the next 2-3 months?",
        options: [
          {
            value: "job_ready",
            label: "Job or internship readiness",
            description: "You want to move toward real opportunities quickly.",
          },
          {
            value: "portfolio",
            label: "A strong portfolio",
            description: "You want impressive proof-of-work and visible output.",
          },
          {
            value: "freelance",
            label: "Freelance readiness",
            description: "You want work that can become income or clients.",
          },
          {
            value: "research_depth",
            label: "Deep knowledge",
            description: "You care about understanding the field properly.",
          },
          {
            value: "startup_building",
            label: "Build my own product",
            description: "You want to turn ideas into something real and launchable.",
          },
        ],
      },
    ],
  },
];

export const initialIntakeForm = {
  fullName: "",
  educationLevel: "",
  interestAreas: [],
  goals: "",
  answers: {
    workStyle: "",
    energySource: "",
    toolPreference: "",
    learningStyle: "",
    collaborationStyle: "",
    weeklyCommitment: "",
    preferredOutcome: "",
  },
};

export const statusOptions = [
  { value: "pending", label: "Pending" },
  { value: "in_progress", label: "In Progress" },
  { value: "done", label: "Done" },
];

