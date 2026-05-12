const userInfo = document.querySelector("#user-info");
const summaryUser = document.querySelector("#summary-user");
const summaryPortfolios = document.querySelector("#summary-portfolios");
const summaryActive = document.querySelector("#summary-active");
const portfoliosList = document.querySelector("#portfolios-list");
const portfolioForm = document.querySelector("#portfolio-form");
const dashboardMessage = document.querySelector("#dashboard-message");
const logoutBtn = document.querySelector("#logout-btn");

let currentUser = null;

function showDashboardMessage(text, type = "success") {
  dashboardMessage.textContent = text;
  dashboardMessage.className = `message ${type}`;
}

function requireAuth() {
  if (!API.getToken()) {
    window.location.href = "/";
  }
}

async function loadCurrentUser() {
  currentUser = await API.request("/auth/me");

  userInfo.textContent = `${currentUser.full_name} • ${currentUser.email}`;
  summaryUser.textContent = currentUser.full_name;
}

function renderPortfolios(portfolios) {
  if (!portfolios.length) {
    portfoliosList.innerHTML = `<p class="muted">Портфели пока не созданы.</p>`;
    return;
  }

  portfoliosList.innerHTML = portfolios
    .map(
      (portfolio) => `
        <article class="portfolio-card">
            <div>
                <h3>${portfolio.name}</h3>
                <p>${portfolio.description || "Без описания"}</p>

                <div class="portfolio-meta">
                    <span>${portfolio.currency}</span>
                    <span>${portfolio.is_active ? "Активен" : "Неактивен"}</span>
                    <span>ID: ${portfolio.id}</span>
                </div>
            </div>

            <div class="card-actions">
              <a class="btn btn-outline" href="/portfolio/${portfolio.id}">ОТКРЫТЬ</a>
              <a class="btn btn-primary" href="/analytics/${portfolio.id}">АНАЛИТИКА</a>

              <button class="btn btn-outline btn-small" data-action="rename" data-id="${portfolio.id}">
                ИМЯ
              </button>

              <button class="btn btn-outline btn-small" data-action="description" data-id="${portfolio.id}">
                ОПИСАНИЕ
              </button>

              <button class="btn btn-outline btn-small" data-action="${portfolio.is_active ? "deactivate" : "activate"}" data-id="${portfolio.id}">
                ${portfolio.is_active ? "В АРХИВ" : "АКТИВИРОВАТЬ"}
              </button>

              <button class="btn btn-danger btn-small" data-action="delete" data-id="${portfolio.id}">
                УДАЛИТЬ
              </button>
            </div>
        </article>
    `,
    )
    .join("");
}

async function loadPortfolios() {
  const portfolios = await API.request(`/portfolios/user/${currentUser.id}`);

  const active = portfolios.filter((item) => item.is_active);

  summaryPortfolios.textContent = portfolios.length;
  summaryActive.textContent = active.length;

  renderPortfolios(portfolios);
}

portfolioForm?.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(portfolioForm);

  const payload = {
    name: formData.get("name"),
    currency: formData.get("currency"),
    description: formData.get("description") || null,
  };

  try {
    await API.request(`/portfolios/?user_id=${currentUser.id}`, {
      method: "POST",
      body: JSON.stringify(payload),
    });

    showDashboardMessage("Портфель создан.");
    portfolioForm.reset();

    await loadPortfolios();
  } catch (error) {
    showDashboardMessage(error.message, "error");
  }
});

logoutBtn?.addEventListener("click", () => {
  API.clearToken();
  window.location.href = "/";
});

async function initDashboard() {
  try {
    requireAuth();
    await loadCurrentUser();
    await loadPortfolios();
  } catch (error) {
    console.error(error);
    API.clearToken();
    window.location.href = "/";
  }
}

portfoliosList?.addEventListener("click", async (event) => {
  const button = event.target.closest("button[data-action]");

  if (!button) {
    return;
  }

  const action = button.dataset.action;
  const portfolioId = button.dataset.id;

  try {
    if (action === "rename") {
      const newName = prompt("Введите новое название портфеля:");

      if (!newName || !newName.trim()) {
        return;
      }

      await API.request(
        `/portfolios/${portfolioId}/rename?new_name=${encodeURIComponent(newName.trim())}`,
        {
          method: "PATCH",
        },
      );

      showDashboardMessage("Название портфеля обновлено.");
    }

    if (action === "description") {
      const description = prompt("Введите новое описание портфеля:");

      if (description === null) {
        return;
      }

      await API.request(
        `/portfolios/${portfolioId}/description?description=${encodeURIComponent(description.trim())}`,
        {
          method: "PATCH",
        },
      );

      showDashboardMessage("Описание портфеля обновлено.");
    }

    if (action === "deactivate") {
      await API.request(`/portfolios/${portfolioId}/deactivate`, {
        method: "PATCH",
      });

      showDashboardMessage("Портфель деактивирован.");
    }

    if (action === "activate") {
      await API.request(`/portfolios/${portfolioId}/activate`, {
        method: "PATCH",
      });

      showDashboardMessage("Портфель активирован.");
    }

    if (action === "delete") {
      const confirmed = confirm(
        "Удалить портфель? Все связанные операции тоже будут удалены.",
      );

      if (!confirmed) {
        return;
      }

      await API.request(`/portfolios/${portfolioId}`, {
        method: "DELETE",
      });

      showDashboardMessage("Портфель удалён.");
    }

    await loadPortfolios();
  } catch (error) {
    showDashboardMessage(error.message, "error");
  }
});

initDashboard();
