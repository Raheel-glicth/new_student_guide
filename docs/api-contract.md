# API Contract

## `GET /api/health`

Returns service health and database initialization status.

Example response:

```json
{
  "status": "ok",
  "service": "ai-career-os-backend",
  "database": "ready"
}
```

## `POST /api/intake`

Stores the student profile and questionnaire payload, then creates a starter roadmap.

Example request:

```json
{
  "fullName": "Aarav",
  "educationLevel": "Undergraduate",
  "interestAreas": ["AI/ML", "Data Science"],
  "goals": "I want a practical career path with portfolio projects.",
  "answers": {
    "learningStyle": "project-based",
    "weeklyCommitment": "8-10 hours"
  }
}
```

## `GET /api/roadmap`

Returns the latest generated roadmap for the current local user.

## `POST /api/progress`

Stores a progress update against a roadmap task.

Example request:

```json
{
  "roadmapId": 1,
  "weekNumber": 1,
  "taskTitle": "Complete Python basics refresh",
  "status": "done",
  "notes": "Finished variables, loops, and functions."
}
```

## `POST /api/mentor`

Accepts a student message and returns a placeholder mentor response for now. In Step 6 this route will call the selected AI provider.

