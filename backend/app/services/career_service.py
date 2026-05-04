TRACKS = {
    "ai_ml": {
        "name": "AI/ML Engineer",
        "summary": "Build intelligent systems, automation, and model-powered products.",
        "tools": ["Python", "Jupyter", "scikit-learn", "GitHub"],
        "project": "Train a simple model and wrap it in a student-friendly mini app.",
        "focus_skills": ["Python", "data handling", "model basics", "deployment thinking"],
    },
    "cybersecurity": {
        "name": "Cybersecurity Analyst",
        "summary": "Protect systems, investigate threats, and improve digital safety.",
        "tools": ["Linux", "Wireshark", "Burp Suite", "TryHackMe"],
        "project": "Document a home-lab security audit and common vulnerability fixes.",
        "focus_skills": ["networking", "threat analysis", "defensive tooling", "reporting"],
    },
    "video_editing": {
        "name": "Video Editor",
        "summary": "Tell strong visual stories through editing, pacing, and post-production.",
        "tools": ["Premiere Pro or DaVinci Resolve", "After Effects basics", "Frame.io"],
        "project": "Edit a short story-driven reel with captions, pacing, and transitions.",
        "focus_skills": ["storytelling", "editing rhythm", "audio polish", "portfolio packaging"],
    },
    "data_science": {
        "name": "Data Scientist",
        "summary": "Turn messy data into insights, experiments, and decision support.",
        "tools": ["Python", "Pandas", "SQL", "Matplotlib"],
        "project": "Analyze a public dataset and present the findings in a clean report.",
        "focus_skills": ["data cleaning", "analysis", "visualization", "business thinking"],
    },
    "ui_ux": {
        "name": "UI/UX Designer",
        "summary": "Design interfaces and user journeys that feel clear, useful, and polished.",
        "tools": ["Figma", "Notion", "Whimsical", "Maze"],
        "project": "Redesign a student-facing app flow with wireframes and prototype screens.",
        "focus_skills": ["user research", "wireframing", "visual systems", "interaction design"],
    },
    "full_stack": {
        "name": "Full Stack Developer",
        "summary": "Build end-to-end products across frontend, backend, and data.",
        "tools": ["JavaScript", "React", "Node or Flask", "SQLite"],
        "project": "Ship a simple web app that solves one real student problem.",
        "focus_skills": ["frontend", "backend", "APIs", "shipping fast"],
    },
    "digital_marketing": {
        "name": "Digital Marketing Strategist",
        "summary": "Grow products and brands through campaigns, content, and audience insight.",
        "tools": ["Canva", "Google Analytics", "Meta Ads concepts", "Notion"],
        "project": "Build a campaign concept with content pillars and measurable goals.",
        "focus_skills": ["messaging", "audience research", "content systems", "analytics"],
    },
}


INTEREST_TO_TRACK = {
    "AI/ML": "ai_ml",
    "Cybersecurity": "cybersecurity",
    "Video Editing": "video_editing",
    "Data Science": "data_science",
    "UI/UX Design": "ui_ux",
    "Full Stack Development": "full_stack",
    "Digital Marketing": "digital_marketing",
}


QUESTION_SCORING = {
    "workStyle": {
        "intelligent_products": {"ai_ml": 4, "full_stack": 2, "data_science": 1},
        "protect_systems": {"cybersecurity": 4, "full_stack": 1},
        "visual_storytelling": {"video_editing": 4, "digital_marketing": 1},
        "analyze_patterns": {"data_science": 4, "ai_ml": 2},
        "design_experiences": {"ui_ux": 4, "digital_marketing": 1},
        "ship_products_fast": {"full_stack": 4, "digital_marketing": 1},
    },
    "energySource": {
        "solving_logic": {"ai_ml": 3, "full_stack": 2, "cybersecurity": 2},
        "finding_risks": {"cybersecurity": 4, "data_science": 1},
        "creative_expression": {"video_editing": 4, "ui_ux": 2, "digital_marketing": 2},
        "discovering_insights": {"data_science": 4, "ai_ml": 1},
        "helping_users": {"ui_ux": 4, "digital_marketing": 2, "full_stack": 1},
        "building_public_work": {"full_stack": 2, "video_editing": 2, "digital_marketing": 3},
    },
    "toolPreference": {
        "python_models": {"ai_ml": 4, "data_science": 3},
        "networks_security": {"cybersecurity": 4},
        "editing_timeline": {"video_editing": 4},
        "dashboards_spreadsheets": {"data_science": 4, "digital_marketing": 1},
        "wireframes_prototypes": {"ui_ux": 4},
        "frontend_backend": {"full_stack": 4, "ai_ml": 1},
    },
    "learningStyle": {
        "project_based": {"full_stack": 2, "ai_ml": 2, "video_editing": 2},
        "challenge_based": {"cybersecurity": 3, "full_stack": 1},
        "visual_examples": {"video_editing": 2, "ui_ux": 2, "digital_marketing": 1},
        "structured_curriculum": {"data_science": 2, "ai_ml": 1, "cybersecurity": 1},
        "feedback_loops": {"ui_ux": 2, "video_editing": 1, "digital_marketing": 1},
    },
    "collaborationStyle": {
        "independent_focus": {"ai_ml": 1, "cybersecurity": 2, "video_editing": 1},
        "small_team": {"full_stack": 2, "ui_ux": 2, "data_science": 1},
        "client_facing": {"digital_marketing": 3, "video_editing": 1, "ui_ux": 1},
        "cross_functional": {"full_stack": 2, "ui_ux": 2, "digital_marketing": 2},
    },
    "preferredOutcome": {
        "job_ready": {"full_stack": 2, "data_science": 2, "cybersecurity": 2},
        "portfolio": {"video_editing": 3, "ui_ux": 3, "full_stack": 2},
        "freelance": {"video_editing": 3, "digital_marketing": 3, "ui_ux": 2},
        "research_depth": {"ai_ml": 3, "data_science": 2},
        "startup_building": {"full_stack": 3, "digital_marketing": 1, "ui_ux": 1},
    },
}


ANSWER_LABELS = {
    "workStyle": {
        "intelligent_products": "you like building intelligent products",
        "protect_systems": "you enjoy protecting systems and uncovering weaknesses",
        "visual_storytelling": "you enjoy visual storytelling",
        "analyze_patterns": "you are energized by analyzing patterns and insights",
        "design_experiences": "you care about user experience and design clarity",
        "ship_products_fast": "you like shipping practical products quickly",
    },
    "energySource": {
        "solving_logic": "logic-heavy problem solving motivates you",
        "finding_risks": "you naturally look for hidden risks and gaps",
        "creative_expression": "creative expression keeps your energy high",
        "discovering_insights": "you like turning information into insight",
        "helping_users": "you care about making things better for users",
        "building_public_work": "you want work that becomes visible in the real world",
    },
    "toolPreference": {
        "python_models": "you are curious about Python and model-based tools",
        "networks_security": "you are drawn to networks and security tooling",
        "editing_timeline": "editing software feels natural to you",
        "dashboards_spreadsheets": "data dashboards and structured analysis appeal to you",
        "wireframes_prototypes": "wireframes and prototypes match how you think",
        "frontend_backend": "you want to build products end-to-end",
    },
}


PACE_LABELS = {
    "4-6": "light",
    "7-10": "balanced",
    "11-15": "accelerated",
    "16+": "immersive",
}


def _blank_scores():
    return {track_key: 0 for track_key in TRACKS}


def score_student_profile(payload):
    answers = payload.get("answers", {})
    interest_areas = payload.get("interestAreas", [])
    scores = _blank_scores()

    for interest in interest_areas:
        track_key = INTEREST_TO_TRACK.get(interest)
        if track_key:
            scores[track_key] += 4

    for question_key, selected_value in answers.items():
        weighted_tracks = QUESTION_SCORING.get(question_key, {}).get(selected_value, {})
        for track_key, weight in weighted_tracks.items():
            scores[track_key] += weight

    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    primary_key, primary_score = ranked[0]
    primary_track = TRACKS[primary_key]

    alternatives = []
    for track_key, score in ranked[1:4]:
        alternatives.append(
            {
                "key": track_key,
                "name": TRACKS[track_key]["name"],
                "score": score,
            }
        )

    why_fit = []
    for question_key, label_map in ANSWER_LABELS.items():
        answer_value = answers.get(question_key)
        if answer_value and answer_value in label_map:
            why_fit.append(label_map[answer_value])

    if not why_fit:
        why_fit = [
            f"your selected interests point strongly toward {primary_track['name']}",
            "your answers show a clear direction instead of broad exploration",
            "the current pace and outcome preferences support this path well",
        ]

    weekly_commitment = answers.get("weeklyCommitment", "7-10")

    return {
        "primaryTrack": {
            "key": primary_key,
            "name": primary_track["name"],
            "summary": primary_track["summary"],
            "score": primary_score,
            "tools": primary_track["tools"],
            "projectIdea": primary_track["project"],
            "focusSkills": primary_track["focus_skills"],
            "whyFit": why_fit[:3],
        },
        "alternatives": alternatives,
        "scoreBreakdown": [
            {
                "key": track_key,
                "name": TRACKS[track_key]["name"],
                "score": score,
            }
            for track_key, score in ranked
        ],
        "weeklyCommitment": weekly_commitment,
        "paceLabel": PACE_LABELS.get(weekly_commitment, "balanced"),
    }

