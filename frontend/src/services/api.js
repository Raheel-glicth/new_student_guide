const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  (import.meta.env.PROD ? "" : "http://localhost:5000");

const REQUEST_TIMEOUT_MS = 12000;

export class ApiError extends Error {
  constructor(message, details = {}) {
    super(message);
    this.name = "ApiError";
    this.status = details.status;
    this.code = details.code;
    this.requestId = details.requestId;
  }
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function request(path, options = {}, attempt = 0) {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
      signal: controller.signal,
      ...options,
    });

    if (!response.ok) {
      const errorBody = await response.json().catch(() => ({}));
      throw new ApiError(errorBody.error || `Request failed: ${response.status}`, {
        status: response.status,
        code: errorBody.code,
        requestId: response.headers.get("X-Request-ID"),
      });
    }

    return response.json();
  } catch (error) {
    const canRetry =
      !options.method &&
      attempt < 2 &&
      (error.name === "AbortError" || error.status >= 500 || !error.status);

    if (canRetry) {
      await sleep(300 * (attempt + 1));
      return request(path, options, attempt + 1);
    }

    if (error.name === "AbortError") {
      throw new ApiError("The server took too long to respond.", {
        code: "request_timeout",
      });
    }

    throw error;
  } finally {
    window.clearTimeout(timeoutId);
  }
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
