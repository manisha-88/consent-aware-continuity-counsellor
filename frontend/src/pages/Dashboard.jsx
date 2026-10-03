import React, { useEffect, useState } from "react";
import {
  Users,
  CheckCircle2,
  UserCheck,
  Siren,
  ArrowRight,
  ShieldAlert,
} from "lucide-react";
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
} from "recharts";
import { useNavigate } from "react-router-dom";
import { getDashboard } from "../api";

// Palette matching original dashboard design
const RISK_COLORS = ["#52b788", "#ffb703", "#e63946"];
const CONSENT_COLORS = ["#52b788", "#ffb703", "#e63946"];
const REVIEW_COLORS = ["#52b788", "#ffb703"];

// Custom label rendered around donut slices
const renderCustomLabel = ({
  cx,
  cy,
  midAngle,
  outerRadius,
  value,
}) => {
  if (!value) return null;
  const RADIAN = Math.PI / 180;
  const radius = outerRadius + 14;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);

  return (
    <text
      x={x}
      y={y}
      fill="#64748b"
      textAnchor={x > cx ? "start" : "end"}
      dominantBaseline="central"
      fontSize="12"
      fontWeight="600"
    >
      {value}
    </text>
  );
};

function Dashboard() {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const dashboardResult = await getDashboard();
      setData(dashboardResult);
    } catch (err) {
      console.error(err);
      setError("Unable to load dashboard information.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard-state">
        <div className="spinner"></div>
        <p>Loading Counselling Continuity Dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-state error">
        <ShieldAlert size={36} />
        <div>
          <h3>Dashboard Unavailable</h3>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  // Dynamic Metrics Parsing
  const totalClients = data?.total_clients ?? 0;

  const lowRisk = data?.risk_distribution?.low ?? 0;
  const ambiguous = data?.risk_distribution?.ambiguous ?? 0;
  const urgentCases = data?.risk_distribution?.urgent ?? 0;
  const totalRiskCases = lowRisk + ambiguous + urgentCases;

  const allowed = data?.allowed_information ?? 0;
  const restricted = data?.restricted_information ?? 0;
  const unknown = data?.unknown_information ?? 0;
  const totalConsentRecords = allowed + restricted + unknown;

  const reviewRequired = data?.review_required ?? 0;
  const noReview = data?.no_review_required ?? 0;
  const totalHandovers = noReview + reviewRequired;

  // Chart structures
  const riskData = [
    { name: "Low Risk", value: lowRisk },
    { name: "Ambiguous", value: ambiguous },
    { name: "Urgent", value: urgentCases },
  ];

  const consentData = [
    { name: "Allowed", value: allowed },
    { name: "Restricted", value: restricted },
    { name: "Unknown", value: unknown },
  ];

  const reviewData = [
    { name: "No Review", value: noReview },
    { name: "Human Review", value: reviewRequired },
  ];

  return (
    <div className="dashboard-page">
      {/* Top Header */}
      <header className="dashboard-header">
        <div>
          <div className="dashboard-title-row">
            <div>
              <h1 className="dashboard-title">
                Counselling Continuity Dashboard
              </h1>
              <p className="dashboard-subtitle">
                An overview of the consent-aware counselling handover system.
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Top Metric Cards */}
      <section className="stats-grid">
        <div className="stat-card blue">
          <div className="stat-icon">
            <Users size={22} />
          </div>
          <div className="stat-card-content">
            <div className="stat-value">{totalClients}</div>
            <div className="stat-label">Total Clients</div>
            <div className="stat-description">Synthetic cases available</div>
          </div>
        </div>

        <div className="stat-card green">
          <div className="stat-icon">
            <CheckCircle2 size={22} />
          </div>
          <div className="stat-card-content">
            <div className="stat-value">{lowRisk}</div>
            <div className="stat-label">Low Risk Cases</div>
            <div className="stat-description">No escalation required</div>
          </div>
        </div>

        <div className="stat-card orange">
          <div className="stat-icon">
            <UserCheck size={22} />
          </div>
          <div className="stat-card-content">
            <div className="stat-value">{reviewRequired}</div>
            <div className="stat-label">Review Required</div>
            <div className="stat-description">Human review needed</div>
          </div>
        </div>

        <div className="stat-card red">
          <div className="stat-icon">
            <Siren size={22} />
          </div>
          <div className="stat-card-content">
            <div className="stat-value">{urgentCases}</div>
            <div className="stat-label">Urgent Cases</div>
            <div className="stat-description">Immediate attention</div>
          </div>
        </div>
      </section>

      {/* Donut Charts Section */}
      <section className="charts-grid">
        {/* Risk Level Distribution */}
        <div className="chart-card">
          <div className="chart-card-header">
            <div>
              <h2>Risk Level Distribution</h2>
              <p>Distribution of cases by risk level</p>
            </div>
            <button
              className="view-details-link"
              onClick={() => navigate("/handover")}
            >
              View Details <ArrowRight size={13} />
            </button>
          </div>

          <div className="donut-wrapper">
            <div className="chart-container">
              <ResponsiveContainer width="100%" height={210}>
                <PieChart>
                  <Pie
                    data={riskData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    innerRadius={52}
                    outerRadius={75}
                    paddingAngle={3}
                    label={renderCustomLabel}
                    labelLine={false}
                  >
                    {riskData.map((entry, index) => (
                      <Cell key={entry.name} fill={RISK_COLORS[index]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>

              <div className="donut-center-overlay">
                <span className="donut-center-value">{totalRiskCases}</span>
                <span className="donut-center-label">Total Cases</span>
              </div>
            </div>

            <div className="horizontal-legend">
              <div className="legend-item">
                <span className="legend-dot green"></span>
                <span className="legend-text">Low Risk</span>
                <span className="legend-val">{lowRisk}</span>
              </div>
              <div className="legend-item">
                <span className="legend-dot orange"></span>
                <span className="legend-text">Ambiguous</span>
                <span className="legend-val">{ambiguous}</span>
              </div>
              <div className="legend-item">
                <span className="legend-dot red"></span>
                <span className="legend-text">Urgent</span>
                <span className="legend-val">{urgentCases}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Consent Status Overview */}
        <div className="chart-card">
          <div className="chart-card-header">
            <div>
              <h2>Consent Status Overview</h2>
              <p>Client consent for information sharing</p>
            </div>
            <button
              className="view-details-link"
              onClick={() => navigate("/handover")}
            >
              View Details <ArrowRight size={13} />
            </button>
          </div>

          <div className="donut-wrapper">
            <div className="chart-container">
              <ResponsiveContainer width="100%" height={210}>
                <PieChart>
                  <Pie
                    data={consentData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    innerRadius={52}
                    outerRadius={75}
                    paddingAngle={3}
                    label={renderCustomLabel}
                    labelLine={false}
                  >
                    {consentData.map((entry, index) => (
                      <Cell key={entry.name} fill={CONSENT_COLORS[index]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>

              <div className="donut-center-overlay">
                <span className="donut-center-value">
                  {totalConsentRecords}
                </span>
                <span className="donut-center-label">Total Records</span>
              </div>
            </div>

            <div className="horizontal-legend">
              <div className="legend-item">
                <span className="legend-dot green"></span>
                <span className="legend-text">Allowed</span>
                <span className="legend-val">{allowed}</span>
              </div>
              <div className="legend-item">
                <span className="legend-dot orange"></span>
                <span className="legend-text">Restricted</span>
                <span className="legend-val">{restricted}</span>
              </div>
              <div className="legend-item">
                <span className="legend-dot red"></span>
                <span className="legend-text">Unknown</span>
                <span className="legend-val">{unknown}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Handover Review Status */}
        <div className="chart-card">
          <div className="chart-card-header">
            <div>
              <h2>Handover Review Status</h2>
              <p>Status of generated handovers</p>
            </div>
            <button
              className="view-details-link"
              onClick={() => navigate("/handover")}
            >
              View Details <ArrowRight size={13} />
            </button>
          </div>

          <div className="donut-wrapper">
            <div className="chart-container">
              <ResponsiveContainer width="100%" height={210}>
                <PieChart>
                  <Pie
                    data={reviewData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    innerRadius={52}
                    outerRadius={75}
                    paddingAngle={3}
                    label={renderCustomLabel}
                    labelLine={false}
                  >
                    {reviewData.map((entry, index) => (
                      <Cell key={entry.name} fill={REVIEW_COLORS[index]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>

              <div className="donut-center-overlay">
                <span className="donut-center-value">{totalHandovers}</span>
                <span className="donut-center-label">Total Handovers</span>
              </div>
            </div>

            <div className="horizontal-legend">
              <div className="legend-item">
                <span className="legend-dot green"></span>
                <span className="legend-text">No Review</span>
                <span className="legend-val">{noReview}</span>
              </div>
              <div className="legend-item">
                <span className="legend-dot orange"></span>
                <span className="legend-text">Human Review</span>
                <span className="legend-val">{reviewRequired}</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Dashboard;