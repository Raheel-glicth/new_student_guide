import os
import tempfile
import unittest

from app import create_app
from app.services.career_service import score_student_profile
from app.services.intake_service import validate_student_intake


VALID_PAYLOAD = {
    "fullName": "Demo Student",
    "educationLevel": "Undergraduate",
    "interestAreas": ["AI/ML", "Full Stack Development"],
    "goals": "Build one strong AI portfolio project.",
    "answers": {
        "workStyle": "intelligent_products",
        "energySource": "solving_logic",
        "toolPreference": "python_models",
        "learningStyle": "project_based",
        "collaborationStyle": "small_team",
        "weeklyCommitment": "7-10",
        "preferredOutcome": "portfolio",
    },
}


class CareerContractTests(unittest.TestCase):
    def test_intake_validation_accepts_known_answers(self):
        self.assertEqual(validate_student_intake(VALID_PAYLOAD), "")

    def test_intake_validation_rejects_unknown_interest(self):
        payload = {**VALID_PAYLOAD, "interestAreas": ["Quantum Surfing"]}
        self.assertIn("interest", validate_student_intake(payload))

    def test_scoring_returns_primary_track_and_breakdown(self):
        recommendation = score_student_profile(VALID_PAYLOAD)

        self.assertEqual(recommendation["primaryTrack"]["key"], "ai_ml")
        self.assertGreaterEqual(len(recommendation["scoreBreakdown"]), 3)


class ApiContractTests(unittest.TestCase):
    def setUp(self):
        self.database = tempfile.NamedTemporaryFile(delete=False)
        self.database.close()
        os.environ["DATABASE_PATH"] = self.database.name
        os.environ["ENABLE_RATE_LIMITING"] = "false"
        self.app = create_app()
        self.client = self.app.test_client()

    def tearDown(self):
        os.unlink(self.database.name)
        os.environ.pop("DATABASE_PATH", None)
        os.environ.pop("ENABLE_RATE_LIMITING", None)

    def test_intake_creates_dashboard_contract(self):
        response = self.client.post("/api/intake", json=VALID_PAYLOAD)
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertIn("dashboard", data)
        self.assertEqual(data["dashboard"]["roadmap"]["title"], "AI/ML Engineer Career Roadmap")

    def test_progress_update_is_idempotent_by_task_key(self):
        intake_response = self.client.post("/api/intake", json=VALID_PAYLOAD).get_json()
        roadmap = intake_response["dashboard"]["roadmap"]
        task = roadmap["weeks"][0]["tasks"][0]

        payload = {
            "roadmapId": roadmap["id"],
            "weekNumber": 1,
            "taskKey": task["key"],
            "taskTitle": task["title"],
            "status": "in_progress",
            "notes": "Started during a test run.",
        }

        first = self.client.post("/api/progress", json=payload)
        second = self.client.post("/api/progress", json={**payload, "status": "done"})

        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 201)

        dashboard = self.client.get("/api/roadmap").get_json()
        updated_task = dashboard["roadmap"]["weeks"][0]["tasks"][0]
        self.assertEqual(updated_task["status"], "done")


if __name__ == "__main__":
    unittest.main()
