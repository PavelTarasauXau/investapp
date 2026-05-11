const page = document.querySelector(".page");
const portfolioId = page?.dataset.portfolioId;

const portfolioTitle = document.querySelector("#portfolio-title");
const portfolioDescription = document.querySelector("#portfolio-description");
const assetSelect = document.querySelector("#asset-select");
const transactionForm = document.querySelector("#transaction-form");
const portfolioMessage = document.querySelector("#portfolio-message");
const positionsList = document.querySelector("#positions-list");
const transactionsList = document.querySelector("#transactions-list");
const newAssetForm = document.querySelector("#new-asset-form");
const newAssetSubmit = document.querySelector("#new-asset-submit");

const assetTypeSelect = document.querySelector(
  '#new-asset-form select[name="asset_type"]',
);
const stockFields = document.querySelector(".stock-fields");
const bondFields = document.querySelector(".bond-fields");
const etfFields = document.querySelector(".etf-fields");
const currencyFields = document.querySelector(".currency-fields");

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

function buildAssetPayload(formData) {
  const assetType = formData.get("asset_type");
  const ticker = String(formData.get("ticker")).trim().toUpperCase();

  const baseAsset = {
    ticker,
    name: formData.get("name"),
    asset_type: assetType,
    isin: null,
    description: "Created from portfolio page",
  };

  if (assetType === "stock") {
    return {
      endpoint: "/assets/stocks",
      payload: {
        asset: baseAsset,
        stock: {
          sector: formData.get("sector") || "Unknown",
          shares_outstanding: null,
          dividend_policy: formData.get("dividend_policy") || null,
        },
      },
    };
  }

  if (assetType === "bond") {
    return {
      endpoint: "/assets/bonds",
      payload: {
        asset: baseAsset,
        bond: {
          nominal_value: formData.get("nominal_value") || "1000",
          coupon_rate: formData.get("coupon_rate") || "0",
          coupon_frequency: 1,
          maturity_date: formData.get("maturity_date") || "2030-01-01",
        },
      },
    };
  }

  if (assetType === "etf") {
    return {
      endpoint: "/assets/etfs",
      payload: {
        asset: baseAsset,
        etf: {
          provider: formData.get("provider") || "Unknown",
          expense_ratio: formData.get("expense_ratio") || null,
          benchmark_index: formData.get("benchmark_index") || null,
          trading_currency: "USD",
        },
      },
    };
  }

  const iso = (formData.get("iso4217") || ticker).toUpperCase().slice(0, 3);

  return {
    endpoint: "/assets/currencies",
    payload: {
      asset: baseAsset,
      currency: {
        iso4217: iso,
        country: formData.get("country") || "Unknown",
        symbol: formData.get("symbol") || iso,
      },
    },
  };
}

newAssetSubmit?.addEventListener("click", async () => {
  if (!newAssetForm.reportValidity()) {
    return;
  }

  const formData = new FormData(newAssetForm);

  try {
    const { endpoint, payload } = buildAssetPayload(formData);

    console.log("CREATE ASSET ENDPOINT:", endpoint);
    console.log("CREATE ASSET PAYLOAD:", payload);

    const asset = await API.request(endpoint, {
      method: "POST",
      body: JSON.stringify(payload),
    });

    console.log("CREATED ASSET:", asset);

    const transactionPayload = {
      portfolio_id: Number(portfolioId),
      asset_id: asset.id,
      transaction_type: "buy",
      quantity: formData.get("quantity"),
      price: formData.get("price"),
      commission: formData.get("commission") || "0",
    };

    console.log("CREATE TRANSACTION PAYLOAD:", transactionPayload);

    const transaction = await API.request("/transactions/", {
      method: "POST",
      body: JSON.stringify(transactionPayload),
    });

    console.log("CREATED TRANSACTION:", transaction);

    showPortfolioMessage("Новый актив добавлен и куплен.");
    newAssetForm.reset();

    await loadAssets();
    await loadPositions();
    await loadTransactions();
  } catch (error) {
    console.error("NEW ASSET ERROR:", error);
    showPortfolioMessage(error.message, "error");
  }
});

function updateAssetExtraFields() {
  const type = assetTypeSelect?.value;

  stockFields?.classList.toggle("hidden", type !== "stock");
  bondFields?.classList.toggle("hidden", type !== "bond");
  etfFields?.classList.toggle("hidden", type !== "etf");
  currencyFields?.classList.toggle("hidden", type !== "currency");
}

assetTypeSelect?.addEventListener("change", updateAssetExtraFields);
updateAssetExtraFields();

initPortfolioPage();
