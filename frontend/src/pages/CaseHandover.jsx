import { useEffect, useState } from "react";
import {
  UserRound,
  ShieldCheck,
  AlertTriangle,
  Lock,
  CheckCircle,
  ClipboardList,
  Search,
  User,
  FileText,
} from "lucide-react";

import { getClients, getCase, getHandover } from "../api";

function CaseHandover() {
  const [clients, setClients] = useState([]);
  const [selectedClient, setSelectedClient] = useState("");
  const [caseData, setCaseData] = useState(null);
  const [handover, setHandover] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    loadClients();
  }, []);

  const loadClients = async () => {
    try {
      const result = await getClients();
      setClients(Array.isArray(result) ? result : result.clients || []);
    } catch (err) {
      console.error(err);
      setError("Unable to load clients.");
    }
  };

  const handleClientChange = async (event) => {
    const rawId = event.target.value;
    const clientId = rawId ? rawId.trim() : "";
    setSelectedClient(clientId);
    setCaseData(null);
    setHandover(null);
    setError("");

    if (!clientId) return;

    try {
      setLoading(true);
      const result = await getCase(clientId);
      setCaseData(result);
    } catch (err) {
      console.error(err);
      setError(`Unable to load case information for client ${clientId}.`);
    } finally {
      setLoading(false);
    }
  };

  const generateHandover = async () => {
    if (!selectedClient) return;

    try {
      setLoading(true);
      setError("");
      const result = await getHandover(selectedClient);
      setHandover(result);
    } catch (err) {
      console.error(err);
      if (err.code === "ECONNABORTED") {
        setError("Request timed out. Server took too long to generate handover.");
      } else {
        setError("Unable to generate handover.");
      }
    } finally {
      setLoading(false);
    }
  };

  const getRiskClass = () => {
    const rawRisk = handover?.risk_assessment?.level || handover?.risk;
    const risk = typeof rawRisk === "object" ? rawRisk?.level : rawRisk;
    return `risk-${String(risk || "low").toLowerCase()}`;
  };

  const getRiskDisplay = () => {
    const rawRisk = handover?.risk_assessment?.level || handover?.risk;
    const risk = typeof rawRisk === "object" ? rawRisk?.level : rawRisk;
    return String(risk || "low").toUpperCase();
  };

  return (
    <div className="content-page">
      {/* Page Title */}
      <div className="page-header-container">
        <div>
          <h1 className="page-header-title">Case Handover</h1>
          <p className="page-header-subtitle">
            Generate a consent-aware continuity handover for a client.
          </p>
        </div>
      </div>

      {/* Select Client Card */}
      <div className="case-selector-card">
        <label className="selector-label">Select Client</label>
        <div className="selector-row">
          <div className="select-input-wrapper">
            <Search size={18} className="search-input-icon" />
            <select value={selectedClient} onChange={handleClientChange}>
              <option value="">-- Select a client --</option>
              {clients.map((client, index) => {
                const id = typeof client === "string" ? client : client.client_id;
                return (
                  <option key={index} value={id}>
                    {id}
                  </option>
                );
              })}
            </select>
          </div>

          <button
            className={`primary-button generate-button ${
              !selectedClient ? "disabled" : ""
            }`}
            onClick={generateHandover}
            disabled={!selectedClient || loading}
          >
            <ClipboardList size={18} />
            Generate Handover
          </button>
        </div>
      </div>

      {error && <div className="error-box">⚠️ {error}</div>}

      {loading && <div className="loading-box">Processing...</div>}

      {/* Empty State when no client is selected */}
      {!selectedClient && !loading && (
        <div className="empty-state-card">
          <div className="empty-state-illustration">
            <div className="illustration-badge">
              <FileText size={42} color="#2563eb" />
              <div className="user-dot">
                <User size={16} color="#ffffff" />
              </div>
            </div>
          </div>

          <h2 className="empty-state-title">No Client Selected</h2>
          <p className="empty-state-description">
            Please select a client from the dropdown above to view session
            records and generate a consent-aware continuity handover summary.
          </p>

          <div className="empty-state-features">
            <div className="feature-item">
              <div className="feature-icon green">
                <ShieldCheck size={18} />
              </div>
              <div className="feature-text">
                <strong>Consent-Aware</strong>
                <span>Respects client consent preferences</span>
              </div>
            </div>

            <div className="feature-divider" />

            <div className="feature-item">
              <div className="feature-icon purple">
                <FileText size={18} />
              </div>
              <div className="feature-text">
                <strong>Structured Summary</strong>
                <span>Key insights, risks and next steps</span>
              </div>
            </div>

            <div className="feature-divider" />

            <div className="feature-item">
              <div className="feature-icon blue">
                <Lock size={18} />
              </div>
              <div className="feature-text">
                <strong>Confidential</strong>
                <span>Sensitive information is protected</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* CASE INFORMATION */}
      {caseData && !handover && (
        <div className="case-section">
          <div className="section-title">
            <UserRound size={22} />
            Case Information
          </div>

          <div className="case-info-grid">
            <div className="info-card">
              <h3>Session Summary</h3>
              <p>
                {caseData.session?.session_summary ||
                  caseData.session_summary ||
                  "No session summary available."}
              </p>
            </div>

            <div className="info-card">
              <h3>Client Goals</h3>
              <ul>
                {(caseData.goals || caseData.client_goals || []).map(
                  (goal, index) => (
                    <li key={index}>{goal}</li>
                  )
                )}
              </ul>
            </div>
          </div>

          <div className="info-card">
            <div className="section-title small">
              <ShieldCheck size={20} />
              Consent Choices
            </div>
            <div className="consent-list">
              {(caseData.consent_choices || caseData.consent || []).map(
                (choice, index) => (
                  <div className="consent-row" key={index}>
                    <span>{choice.category}</span>
                    <span
                      className={`consent-badge ${String(
                        choice.status
                      ).toLowerCase()}`}
                    >
                      {choice.status}
                    </span>
                  </div>
                )
              )}
            </div>
          </div>
        </div>
      )}

      {/* HANDOVER RESULTS */}
      {handover && (
        <div className="handover-section">
          <div className="section-title">
            <CheckCircle size={22} />
            Generated Continuity Handover
          </div>

          {handover.human_review_required && (
            <div className="review-alert">
              <AlertTriangle size={24} />
              <div>
                <strong>Human Review Required</strong>
                <p>
                  A qualified professional must review the original session
                  information before relying on this handover.
                </p>
              </div>
            </div>
          )}

          <div className="handover-grid">
            <div className="handover-card">
              <h3>Risk Assessment</h3>
              <div className={`risk-badge ${getRiskClass()}`}>
                {getRiskDisplay()}
              </div>
              {handover.risk_assessment?.reason && (
                <p>{handover.risk_assessment.reason}</p>
              )}
            </div>

            <div className="handover-card">
              <h3>Current Concern</h3>
              <p>{handover.current_concern || "No information available."}</p>
            </div>
          </div>

          <div className="handover-card">
            <h3>✓ Relevant Information</h3>
            {(handover.relevant_information || []).length === 0 ? (
              <p>No information available under current consent settings.</p>
            ) : (
              <ul className="safe-list">
                {handover.relevant_information.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            )}
          </div>

          <div className="handover-card restricted-card">
            <h3>
              <Lock size={18} />
              Restricted Information
            </h3>
            {(handover.restricted_information || []).length === 0 ? (
              <p>None</p>
            ) : (
              <ul>
                {handover.restricted_information.map((item, index) => (
                  <li key={index}>🔒 {item}</li>
                ))}
              </ul>
            )}
          </div>

          <div className="handover-card">
            <h3>Client Goals</h3>
            <ul>
              {(handover.client_goals || handover.goals || []).map(
                (goal, index) => (
                  <li key={index}>{goal}</li>
                )
              )}
            </ul>
          </div>

          <div className="handover-card">
            <h3>Pending Actions</h3>
            <ul>
              {(handover.pending_actions || []).map((action, index) => (
                <li key={index}>{action}</li>
              ))}
            </ul>
          </div>

          <div className="escalation-card">
            <h3>Escalation Guidance</h3>
            <p>
              {handover.escalation_message ||
                handover.escalation_guidance ||
                "No escalation indicated."}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default CaseHandover;