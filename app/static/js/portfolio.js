const page = document.querySelector(".page");
const portfolioId = page?.dataset.portfolioId;

const portfolioTitle = document.querySelector("#portfolio-title");
const portfolioDescription = document.querySelector("#portfolio-description");
const assetSelect = document.querySelector("#asset-select");
const transactionForm = document.querySelector("#transaction-form");
const portfolioMessage = document.querySelector("#portfolio-message");
const positionsList = document.querySelector("#positions-list");
const transactionsList = document.querySelector("#transactions-list");

function showPortfolioMessage(text, type = "success") {
  portfolioMessage.textContent = text;
  portfolioMessage.className = `message ${type}`;
}

function requireAuth() {
  if (!API.getToken()) {
    window.location.href = "/";
  }
}

function formatMoney(value) {
  return Number(value).toFixed(2);
}

async function loadPortfolio() {
  const portfolio = await API.request(`/portfolios/${portfolioId}`);

  portfolioTitle.textContent = portfolio.name;
  portfolioDescription.textContent = `${portfolio.currency} • ${portfolio.is_active ? "Активен" : "Неактивен"} • ${portfolio.description || "Без описания"}`;
}

async function loadAssets() {
  const assets = await API.request("/assets/");

  if (!assets.length) {
    assetSelect.innerHTML = `<option value="">Нет доступных активов</option>`;
    return;
  }

  assetSelect.innerHTML = assets
    .map(
      (asset) => `
        <option value="${asset.id}">
            ${asset.ticker} — ${asset.name} (${asset.asset_type})
        </option>
    `,
    )
    .join("");
}

async function loadPositions() {
  const positions = await API.request(
    `/analytics/portfolio/${portfolioId}/positions`,
  );

  if (!positions.length) {
    positionsList.innerHTML = `<p class="muted">В портфеле пока нет активов.</p>`;
    return;
  }

  positionsList.innerHTML = positions
    .map(
      (item) => `
        <div class="mini-item">
            <div>
                <strong>${item.ticker}</strong>
                <span>${item.name} • ${item.asset_type}</span>
            </div>
            <strong>${item.quantity}</strong>
        </div>
    `,
    )
    .join("");
}

async function loadTransactions() {
  const transactions = await API.request(
    `/transactions/portfolio/${portfolioId}`,
  );

  if (!transactions.length) {
    transactionsList.innerHTML = `<p class="muted">Операций пока нет.</p>`;
    return;
  }

  transactionsList.innerHTML = `
        <div class="table-row header">
            <div>Тип</div>
            <div>Актив ID</div>
            <div>Количество</div>
            <div>Цена</div>
            <div>Сумма</div>
        </div>
        ${transactions
          .map(
            (tx) => `
            <div class="table-row">
                <div class="tx-type ${tx.transaction_type}">${tx.transaction_type}</div>
                <div>${tx.asset_id}</div>
                <div>${tx.quantity}</div>
                <div>${formatMoney(tx.price)}</div>
                <div>${formatMoney(Number(tx.quantity) * Number(tx.price))}</div>
            </div>
        `,
          )
          .join("")}
    `;
}

transactionForm?.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(transactionForm);

  const payload = {
    portfolio_id: Number(portfolioId),
    asset_id: Number(formData.get("asset_id")),
    transaction_type: formData.get("transaction_type"),
    quantity: formData.get("quantity"),
    price: formData.get("price"),
    commission: formData.get("commission") || "0",
  };

  try {
    await API.request("/transactions/", {
      method: "POST",
      body: JSON.stringify(payload),
    });

    showPortfolioMessage("Операция сохранена.");
    transactionForm.reset();

    await loadPositions();
    await loadTransactions();
  } catch (error) {
    showPortfolioMessage(error.message, "error");
  }
});

async function initPortfolioPage() {
  try {
    requireAuth();

    await loadPortfolio();
    await loadAssets();
    await loadPositions();
    await loadTransactions();
  } catch (error) {
    console.error(error);
    showPortfolioMessage(error.message, "error");
  }
}

initPortfolioPage();
