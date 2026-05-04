const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:5000";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    throw new Error(errorBody.error || `Request failed: ${response.status}`);
  }

  return response.json();
}

export function getHealth() {
  return request("/api/health");
}

export function submitIntake(payload) {
  return request("/api/intake", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getRoadmap() {
  return request("/api/roadmap");
}

export function updateProgress(payload) {
  return request("/api/progress", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function askMentor(payload) {
  return request("/api/mentor", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

