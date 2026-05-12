const periodSelect = document.querySelector("#period-select");

let profitChart = null;
let assetTypeChart = null;
let sectorChart = null;
let lastSummary = null;

const analyticsPage = document.querySelector(".page");
const portfolioId = analyticsPage?.dataset.portfolioId;

const analyticsSubtitle = document.querySelector("#analytics-subtitle");
const positionsCount = document.querySelector("#positions-count");
const transactionsCount = document.querySelector("#transactions-count");
const dividendsTotal = document.querySelector("#dividends-total");
const cashFlowTotal = document.querySelector("#cash-flow-total");
const realizedPnlTotal = document.querySelector("#realized-pnl-total");

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
  cashFlowTotal.textContent = formatNumber(summary.cash_flow);
  realizedPnlTotal.textContent = formatNumber(summary.realized_pnl);

  renderPositions(summary.positions || []);
  renderAllocation(allocationTypes, summary.allocation_by_asset_type || {});
  renderAllocation(allocationSectors, summary.allocation_by_sector || {});
  renderUpcomingPayments(summary.upcoming_payments || {});

  lastSummary = summary;

  const transactions = await API.request(
    `/analytics/portfolio/${portfolioId}/transactions`,
  );

  renderProfitChart(transactions, periodSelect?.value || "all");
  renderAllocationCharts(summary);
}

periodSelect?.addEventListener("change", async () => {
  if (!lastSummary) return;

  const transactions = await API.request(
    `/analytics/portfolio/${portfolioId}/transactions`,
  );
  renderProfitChart(transactions, periodSelect.value);
});

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

/*chart*/
function destroyChart(chart) {
  if (chart) {
    chart.destroy();
  }
}

function getPeriodStart(period) {
  const now = new Date();

  if (period === "day") {
    now.setDate(now.getDate() - 1);
    return now;
  }

  if (period === "week") {
    now.setDate(now.getDate() - 7);
    return now;
  }

  if (period === "month") {
    now.setMonth(now.getMonth() - 1);
    return now;
  }

  if (period === "year") {
    now.setFullYear(now.getFullYear() - 1);
    return now;
  }

  return null;
}

function filterTransactionsByPeriod(transactions, period) {
  const start = getPeriodStart(period);

  if (!start) {
    return transactions;
  }

  return transactions.filter((tx) => {
    const txDate = new Date(tx.transaction_date);
    return txDate >= start;
  });
}

function buildProfitSeries(transactions) {
  const sorted = [...transactions].sort(
    (a, b) => new Date(a.transaction_date) - new Date(b.transaction_date),
  );

  let cumulative = 0;

  return sorted.map((tx) => {
    const amount = Number(tx.quantity) * Number(tx.price);
    const commission = Number(tx.commission || 0);

    if (tx.transaction_type === "buy") {
      cumulative -= amount + commission;
    } else if (tx.transaction_type === "sell") {
      cumulative += amount - commission;
    }

    return {
      date: new Date(tx.transaction_date).toLocaleDateString("ru-RU"),
      value: cumulative,
    };
  });
}

function getChartOptions() {
  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          color: "#f5f5f5",
        },
      },
    },
    scales: {
      x: {
        ticks: {
          color: "#9ca3af",
        },
        grid: {
          color: "#262626",
        },
      },
      y: {
        ticks: {
          color: "#9ca3af",
        },
        grid: {
          color: "#262626",
        },
      },
    },
  };
}

function renderProfitChart(transactions, period = "all") {
  const ctx = document.querySelector("#profit-chart");

  if (!ctx) return;

  const filtered = filterTransactionsByPeriod(transactions, period);
  const series = buildProfitSeries(filtered);

  destroyChart(profitChart);

  profitChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: series.map((item) => item.date),
      datasets: [
        {
          label: "Условный результат",
          data: series.map((item) => item.value),
          borderColor: "#ffffff",
          backgroundColor: "rgba(255,255,255,0.08)",
          tension: 0.35,
          fill: true,
        },
      ],
    },
    options: getChartOptions(),
  });
}

function renderDoughnutChart(canvasId, allocation, label) {
  const ctx = document.querySelector(canvasId);

  if (!ctx) return null;

  const entries = Object.entries(allocation || {}).filter(
    ([, value]) => Number(value) > 0,
  );

  if (!entries.length) {
    return null;
  }

  return new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: entries.map(([key]) => key),
      datasets: [
        {
          label,
          data: entries.map(([, value]) => Number(value)),
          backgroundColor: [
            "#ffffff",
            "#9ca3af",
            "#6b7280",
            "#404040",
            "#262626",
          ],
          borderColor: "#050505",
          borderWidth: 2,
          hoverOffset: 8,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      cutout: "62%",
      plugins: {
        legend: {
          position: "bottom",
          labels: {
            color: "#f5f5f5",
            boxWidth: 14,
            boxHeight: 14,
            padding: 16,
            font: {
              size: 12,
            },
          },
        },
      },
    },
  });
}

function renderAllocationCharts(summary) {
  destroyChart(assetTypeChart);
  destroyChart(sectorChart);

  assetTypeChart = renderDoughnutChart(
    "#asset-type-chart",
    summary.allocation_by_asset_type,
    "Типы активов",
  );

  sectorChart = renderDoughnutChart(
    "#sector-chart",
    summary.allocation_by_sector,
    "Секторы",
  );
}
