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
const transactionFilter = document.querySelector("#transaction-filter");
const assetTypeFilter = document.querySelector("#asset-type-filter");

const dividendForm = document.querySelector("#dividend-form");
const couponForm = document.querySelector("#coupon-form");
const dividendStockSelect = document.querySelector("#dividend-stock-select");
const couponBondSelect = document.querySelector("#coupon-bond-select");
const paymentsList = document.querySelector("#payments-list");

let portfolioTransactions = [];
let assetsCache = [];
let positionsCache = [];

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
  assetsCache = assets;

  if (!assets.length) {
    assetSelect.innerHTML = `<option value="">Нет доступных активов</option>`;
    dividendStockSelect.innerHTML = `<option value="">Нет акций</option>`;
    couponBondSelect.innerHTML = `<option value="">Нет облигаций</option>`;
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

  const stocks = assets.filter((asset) => asset.asset_type === "stock");
  const bonds = assets.filter((asset) => asset.asset_type === "bond");

  dividendStockSelect.innerHTML = stocks.length
    ? stocks
        .map(
          (asset) => `
            <option value="${asset.id}">
              ${asset.ticker} — ${asset.name}
            </option>
          `,
        )
        .join("")
    : `<option value="">Нет акций</option>`;

  couponBondSelect.innerHTML = bonds.length
    ? bonds
        .map(
          (asset) => `
            <option value="${asset.id}">
              ${asset.ticker} — ${asset.name}
            </option>
          `,
        )
        .join("")
    : `<option value="">Нет облигаций</option>`;
}

async function loadPositions() {
  const positions = await API.request(
    `/analytics/portfolio/${portfolioId}/positions`,
  );

  positionsCache = positions;

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

async function loadPayments() {
  const stocks = positionsCache.filter(
    (position) => position.asset_type === "stock",
  );

  const bonds = positionsCache.filter(
    (position) => position.asset_type === "bond",
  );

  const dividendRequests = stocks.map(async (stock) => {
    const dividends = await API.request(`/dividends/stock/${stock.asset_id}`);

    return dividends.map((dividend) => ({
      type: "Дивиденд",
      ticker: stock.ticker,
      date: dividend.payment_date,
      amount: dividend.dividend_per_share,
    }));
  });

  const couponRequests = bonds.map(async (bond) => {
    const coupons = await API.request(`/coupons/bond/${bond.asset_id}`);

    return coupons.map((coupon) => ({
      type: "Купон",
      ticker: bond.ticker,
      date: coupon.payment_date,
      amount: coupon.coupon_amount,
    }));
  });

  const results = await Promise.all([...dividendRequests, ...couponRequests]);
  const payments = results.flat();

  if (!payments.length) {
    paymentsList.innerHTML = `<p class="muted">Выплат пока нет.</p>`;
    return;
  }

  paymentsList.innerHTML = payments
    .map(
      (payment) => `
        <div class="mini-item">
          <div>
            <strong>${payment.type}</strong>
            <span>${payment.ticker} • ${payment.date}</span>
          </div>
          <strong>${formatMoney(payment.amount)}</strong>
        </div>
      `,
    )
    .join("");
}

function renderTransactions(transactions) {
  if (!transactions.length) {
    transactionsList.innerHTML = `<p class="muted">Операций по выбранному фильтру нет.</p>`;
    return;
  }

  transactionsList.innerHTML = `
    <div class="table-row header">
      <div>Тип</div>
      <div>Актив</div>
      <div>Количество</div>
      <div>Цена</div>
      <div>Сумма</div>
    </div>
    ${transactions
      .map(
        (tx) => `
          <div class="table-row">
            <div class="tx-type ${tx.transaction_type}">${tx.transaction_type}</div>
            <div>${getAssetLabel(tx.asset_id)}</div>
            <div>${tx.quantity}</div>
            <div>${formatMoney(tx.price)}</div>
            <div>${formatMoney(Number(tx.quantity) * Number(tx.price))}</div>
          </div>
        `,
      )
      .join("")}
  `;
}

function getAssetLabel(assetId) {
  const asset = assetsCache.find((item) => item.id === assetId);

  if (!asset) {
    return `ID ${assetId}`;
  }

  return `${asset.ticker} • ${asset.asset_type}`;
}

async function loadTransactions() {
  const transactionType = transactionFilter?.value || "all";
  const assetType = assetTypeFilter?.value || "all";

  const params = new URLSearchParams();

  if (transactionType !== "all") {
    params.append("transaction_type", transactionType);
  }

  if (assetType !== "all") {
    params.append("asset_type", assetType);
  }

  const queryString = params.toString();

  const url = queryString
    ? `/transactions/portfolio/${portfolioId}/filter?${queryString}`
    : `/transactions/portfolio/${portfolioId}/filter`;

  portfolioTransactions = await API.request(url);

  renderTransactions(portfolioTransactions);
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
    await loadPayments();
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

transactionFilter?.addEventListener("change", async () => {
  await loadTransactions();
});

transactionFilter?.addEventListener("change", async () => {
  await loadTransactions();
});

assetTypeFilter?.addEventListener("change", async () => {
  await loadTransactions();
});

dividendForm?.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(dividendForm);

  const payload = {
    stock_id: Number(formData.get("stock_id")),
    record_date: formData.get("record_date"),
    payment_date: formData.get("payment_date"),
    dividend_per_share: formData.get("dividend_per_share"),
  };

  try {
    await API.request("/dividends/", {
      method: "POST",
      body: JSON.stringify(payload),
    });

    showPortfolioMessage("Дивидендная выплата добавлена.");
    dividendForm.reset();
    await loadPayments();
  } catch (error) {
    showPortfolioMessage(error.message, "error");
  }
});

couponForm?.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(couponForm);

  const payload = {
    bond_id: Number(formData.get("bond_id")),
    coupon_number: Number(formData.get("coupon_number")),
    payment_date: formData.get("payment_date"),
    coupon_amount: formData.get("coupon_amount"),
  };

  try {
    await API.request("/coupons/", {
      method: "POST",
      body: JSON.stringify(payload),
    });

    showPortfolioMessage("Купонная выплата добавлена.");
    couponForm.reset();
    await loadPayments();
  } catch (error) {
    showPortfolioMessage(error.message, "error");
  }
});

initPortfolioPage();
