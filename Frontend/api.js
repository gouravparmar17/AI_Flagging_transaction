const API_URL = "http://127.0.0.1:8000/api";

const tokenStore = {
  getAccess: () => localStorage.getItem("access_token"),
  getRefresh: () => localStorage.getItem("refresh_token"),
  setTokens: (access, refresh) => {
    if (access) localStorage.setItem("access_token", access);
    if (refresh) localStorage.setItem("refresh_token", refresh);
  },
  clear: () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  },
};

async function refreshAccessToken() {
  const refresh_token = tokenStore.getRefresh();
  if (!refresh_token) return null;
  const response = await fetch(`${API_URL}/auth/refresh/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh: refresh_token }),
  });

  if (!response.ok) {
    tokenStore.clear();
    return null;
  }

  const data = await response.json();
  tokenStore.setTokens(data.access, data.refresh || refresh_token);
  return data.access;
}

async function apiRequest(path, options = {}, retry = true) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  const token = tokenStore.getAccess();
  if (token) headers.Authorization = "Bear" + "er " + token;

  const response = await fetch(`${API_URL}${path}`, { ...options, headers });

  if (response.status === 401 && retry && tokenStore.getRefresh()) {
    const newToken = await refreshAccessToken();
    if (newToken) return apiRequest(path, options, false);
  }

  if (!response.ok) {
    let error = "Request failed";
    try {
      const payload = await response.json();
      error = payload.detail || payload.message || JSON.stringify(payload);
    } catch (_) {}
    throw new Error(error);
  }

  const contentType = response.headers.get("content-type") || "";
  if (contentType.includes("application/json")) return response.json();
  return response.blob();
}

async function login(email, password) {
  const data = await apiRequest("/auth/login/", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  tokenStore.setTokens(data.access_token, data.refresh_token);
  return data;
}

async function register(fullname, email, password) {
  return apiRequest("/auth/register/", {
    method: "POST",
    body: JSON.stringify({ full_name: fullname, email, password }),
  });
}

async function logout() {
  const refresh_token = tokenStore.getRefresh();
  try {
    if (refresh_token) {
      await apiRequest("/auth/logout/", {
        method: "POST",
        body: JSON.stringify({ refresh_token }),
      });
    }
  } finally {
    tokenStore.clear();
  }
}

async function getDashboard() {
  return apiRequest("/dashboard/summary/");
}

async function getTransactions() {
  return apiRequest("/transactions/");
}

async function submitTransaction(data) {
  return apiRequest("/transactions/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

async function predictFraud(transaction) {
  return apiRequest("/fraud/predict/", {
    method: "POST",
    body: JSON.stringify(transaction),
  });
}

async function getAlerts() {
  return apiRequest("/alerts/");
}

async function getReports(type = "csv") {
  return apiRequest(`/reports/${type}/`);
}

window.APIService = {
  login,
  register,
  logout,
  getDashboard,
  getTransactions,
  submitTransaction,
  predictFraud,
  getAlerts,
  getReports,
};
