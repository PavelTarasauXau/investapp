const registerForm = document.querySelector("#register-form");
const loginForm = document.querySelector("#login-form");
const authMessage = document.querySelector("#auth-message");

function showMessage(text, type = "success") {
  authMessage.textContent = text;
  authMessage.className = `message ${type}`;
}

registerForm?.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(registerForm);

  const payload = {
    email: formData.get("email"),
    full_name: formData.get("full_name"),
    password: formData.get("password"),
  };

  try {
    await API.request("/auth/register", {
      method: "POST",
      body: JSON.stringify(payload),
    });

    showMessage("Аккаунт создан. Теперь можно выполнить вход.");
    registerForm.reset();
  } catch (error) {
    showMessage(error.message, "error");
  }
});

loginForm?.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(loginForm);

  const payload = {
    email: formData.get("email"),
    password: formData.get("password"),
  };

  try {
    const data = await API.request("/auth/login", {
      method: "POST",
      body: JSON.stringify(payload),
    });

    API.setToken(data.access_token);
    showMessage("Вход выполнен. Переходим в dashboard...");

    setTimeout(() => {
      window.location.href = "/dashboard";
    }, 700);
  } catch (error) {
    showMessage(error.message, "error");
  }
});
