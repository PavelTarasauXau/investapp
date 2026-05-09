const API = {
  getToken() {
    return localStorage.getItem("access_token");
  },

  setToken(token) {
    localStorage.setItem("access_token", token);
  },

  clearToken() {
    localStorage.removeItem("access_token");
  },

  async request(path, options = {}) {
    const token = this.getToken();

    const headers = {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    };

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(path, {
      ...options,
      headers,
    });

    let data = null;

    try {
      data = await response.json();
    } catch {
      data = null;
    }

    if (!response.ok) {
      const message = data?.detail || data?.message || "Request failed";
      throw new Error(message);
    }

    return data;
  },
};
