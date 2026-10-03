import { useEffect, useState } from "react";
import {
  History,
  ShieldCheck,
  Lock,
  AlertTriangle,
  CheckCircle,
  Calendar,
  User,
} from "lucide-react";

function AuditHistory() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadAuditHistory = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await fetch("http://127.0.0.1:8000/api/audit");

      if (!response.ok) {
        throw new Error("Unable to load audit history.");
      }

      const data = await response.json();
      setRecords(data.records || []);
    } catch (err) {
      console.error(err);
      setError("Unable to connect to the audit service.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAuditHistory();
  }, []);

  return (
    <div className="content-page">
      {/* Top Header Widgets */}
      

      {/* Page Header */}
      <div className="page-header-container">

        <div>
          <h1 className="page-header-title">Audit History</h1>
          <p className="page-header-subtitle">
            Review system activity and consent-aware handover records.
          </p>
        </div>
      </div>

      {/* Security Banner Card */}
      <div className="audit-info-card">
        <div className="audit-info-icon-box">
          <ShieldCheck size={24} color="#2563eb" />
        </div>
        <div>
          <h2 className="audit-info-title">Secure Audit Records</h2>
          <p className="audit-info-desc">
            Audit records are maintained to support transparency, accountability,
            and consent-aware processing.
          </p>
        </div>
      </div>

      {/* Main Activity Card */}
      <div className="audit-card">
        <div className="audit-card-header">
          <div>
            <h2>Handover Activity</h2>
            <p>Recent consent-aware system activity and handover records.</p>
          </div>
          <Lock size={20} className="lock-icon" />
        </div>

        {/* LOADING STATE */}
        {loading && (
          <div className="empty-audit">
            <div className="empty-audit-icon-box">
              <History size={36} color="#2563eb" />
            </div>
            <h3>Loading Audit History...</h3>
            <p>Retrieving secure audit records.</p>
          </div>
        )}

        {/* ERROR STATE */}
        {!loading && error && (
          <div className="empty-audit">
            <div className="empty-audit-icon-box red">
              <AlertTriangle size={36} color="#ef4444" />
            </div>
            <h3>Audit Service Unavailable</h3>
            <p>{error}</p>
            <button onClick={loadAuditHistory} className="primary-button retry-btn">
              Try Again
            </button>
          </div>
        )}

        {/* NO RECORDS STATE */}
        {!loading && !error && records.length === 0 && (
          <div className="empty-audit">
            <div className="empty-audit-icon-box">
              <History size={36} color="#2563eb" />
            </div>
            <h3>No Handover Activity</h3>
            <p>
              Generate a safe handover from the Case Handover page to create an
              audit record.
            </p>
          </div>
        )}

        {/* AUDIT RECORDS LIST */}
        {!loading && !error && records.length > 0 && (
          <div className="audit-list">
            {records.map((record, index) => (
              <div className="audit-record" key={index}>
                <div className="audit-record-icon">
                  <ShieldCheck size={20} color="#2563eb" />
                </div>

                <div className="audit-record-content">
                  <div className="audit-record-title">
                    <h3>{record.action}</h3>
                    <span className="audit-time">
                      {new Date(record.timestamp).toLocaleString()}
                    </span>
                  </div>

                  <p className="audit-client-id">
                    Client: <strong>{record.client_id}</strong>
                  </p>

                  <p className="audit-desc">{record.description}</p>

                  <div className="audit-tags">
                    <span className="audit-tag">Risk: {record.risk_level}</span>
                    <span className="audit-tag">
                      {record.human_review_required
                        ? "Human Review Required"
                        : "No Human Review"}
                    </span>
                    {record.escalation_required && (
                      <span className="audit-tag warning">
                        Escalation Required
                      </span>
                    )}
                  </div>
                </div>

                <div className="audit-status">
                  {record.status === "completed" ? (
                    <CheckCircle size={22} color="#16a34a" />
                  ) : (
                    <AlertTriangle size={22} color="#f59e0b" />
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* PRIVACY FOOTER NOTE */}
      <div className="privacy-note">
        🔒 Audit information should only be accessible to authorized counselling
        professionals.
      </div>
    </div>
  );
}

export default AuditHistory;