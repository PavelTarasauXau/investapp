const analyticsPage = document.querySelector(".page");
const portfolioId = analyticsPage?.dataset.portfolioId;

const analyticsSubtitle = document.querySelector("#analytics-subtitle");
const positionsCount = document.querySelector("#positions-count");
const transactionsCount = document.querySelector("#transactions-count");
const dividendsTotal = document.querySelector("#dividends-total");
const profitTotal = document.querySelector("#profit-total");

const analyticsPositions = document.querySelector("#analytics-positions");
const allocationTypes = document.querySelector("#allocation-types");
const allocationSectors = document.querySelector("#allocation-sectors");
const upcomingPayments = document.querySelector("#upcoming-payments");

function requireAuth() {
  if (!API.getToken()) {
    window.location.href = "/";
  }
}

function formatNumber(value) {
  return Number(value || 0).toFixed(2);
}

function renderPositions(positions) {
  if (!positions.length) {
    analyticsPositions.innerHTML = `<p class="muted">Позиции отсутствуют.</p>`;
    return;
  }

  analyticsPositions.innerHTML = positions
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

function renderAllocation(container, allocation) {
  const entries = Object.entries(allocation || {}).filter(
    ([, value]) => Number(value) > 0,
  );

  if (!entries.length) {
    container.innerHTML = `<p class="muted">Данных пока нет.</p>`;
    return;
  }

  const max = Math.max(...entries.map(([, value]) => Number(value)));

  container.innerHTML = entries
    .map(([key, value]) => {
      const width = max > 0 ? (Number(value) / max) * 100 : 0;

      return `
            <div class="allocation-item">
                <div class="mini-item" style="border: none; padding: 0;">
                    <strong>${key}</strong>
                    <span>${value}</span>
                </div>
                <div class="allocation-line">
                    <div style="width: ${width}%"></div>
                </div>
            </div>
        `;
    })
    .join("");
}

function renderUpcomingPayments(data) {
  const dividends = data?.upcoming_dividends || [];
  const coupons = data?.upcoming_coupons || [];

  const all = [
    ...dividends.map((item) => ({
      type: "Дивиденд",
      ticker: item.ticker,
      date: item.payment_date,
      amount: item.estimated_amount,
    })),
    ...coupons.map((item) => ({
      type: "Купон",
      ticker: item.ticker,
      date: item.payment_date,
      amount: item.estimated_amount,
    })),
  ];

  if (!all.length) {
    upcomingPayments.innerHTML = `<p class="muted">Будущих выплат пока нет.</p>`;
    return;
  }

  upcomingPayments.innerHTML = all
    .map(
      (item) => `
        <div class="payment-item">
            <strong>${item.type} • ${item.ticker}</strong>
            <span>Дата выплаты: ${item.date}</span>
            <span>Оценка суммы: ${formatNumber(item.amount)}</span>
        </div>
    `,
    )
    .join("");
}

async function loadAnalytics() {
  const summary = await API.request(
    `/analytics/portfolio/${portfolioId}/summary`,
  );

  analyticsSubtitle.textContent = `Портфель ID: ${summary.portfolio_id}`;

  positionsCount.textContent = summary.positions_count;
  transactionsCount.textContent = summary.transactions_count;
  dividendsTotal.textContent = formatNumber(summary.received_dividends_total);
  profitTotal.textContent = formatNumber(summary.simple_realized_profit);

  renderPositions(summary.positions || []);
  renderAllocation(allocationTypes, summary.allocation_by_asset_type || {});
  renderAllocation(allocationSectors, summary.allocation_by_sector || {});
  renderUpcomingPayments(summary.upcoming_payments || {});
}

async function initAnalyticsPage() {
  try {
    requireAuth();
    await loadAnalytics();
  } catch (error) {
    console.error(error);
    analyticsSubtitle.textContent = error.message;
  }
}

initAnalyticsPage();
