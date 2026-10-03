import { NavLink } from "react-router-dom";
import {
  Shield,
  Heart,
  Home,
  FileText,
  History,
  ChevronRight,
  ShieldAlert,
} from "lucide-react";

function Sidebar() {
  return (
    <aside className="sidebar">
      {/* ================= BRAND ================= */}
      <div className="sidebar-brand">
        <div className="sidebar-logo-container">
          <Shield className="sidebar-logo-shield" size={48} strokeWidth={1.8} />
          <Heart className="sidebar-logo-heart" size={20} strokeWidth={2.2} />
        </div>

        <div className="sidebar-brand-text">
          <h2 className="sidebar-title">
            Consent-Aware
            <br />
            Continuity Counsellor
          </h2>

          <div className="sidebar-blue-line"></div>

          <p className="sidebar-tagline">
            Respecting Consent.
            <br />
            Continuing Care Safely.
          </p>
        </div>
      </div>

      {/* ================= DIVIDER ================= */}
      <div className="sidebar-divider"></div>

      {/* ================= NAVIGATION ================= */}
      <nav className="sidebar-nav">
        <NavLink
          to="/"
          end
          className={({ isActive }) =>
            `sidebar-link ${isActive ? "active" : ""}`
          }
        >
          <div className="sidebar-link-content">
            <Home className="sidebar-link-icon" size={20} strokeWidth={2} />
            <span>Dashboard</span>
          </div>
          <ChevronRight className="sidebar-arrow" size={16} strokeWidth={2} />
        </NavLink>

        <NavLink
          to="/handover"
          className={({ isActive }) =>
            `sidebar-link ${isActive ? "active" : ""}`
          }
        >
          <div className="sidebar-link-content">
            <FileText className="sidebar-link-icon" size={20} strokeWidth={2} />
            <span>Case Handover</span>
          </div>
          <ChevronRight className="sidebar-arrow" size={16} strokeWidth={2} />
        </NavLink>

        <NavLink
          to="/audit"
          className={({ isActive }) =>
            `sidebar-link ${isActive ? "active" : ""}`
          }
        >
          <div className="sidebar-link-content">
            <History className="sidebar-link-icon" size={20} strokeWidth={2} />
            <span>Audit History</span>
          </div>
          <ChevronRight className="sidebar-arrow" size={16} strokeWidth={2} />
        </NavLink>
      </nav>

      {/* ================= FOOTER ================= */}
      <div className="sidebar-footer">
        <div className="sidebar-footer-card">
          <div className="sidebar-footer-icon-box">
            <ShieldAlert size={22} strokeWidth={2} />
          </div>
          <div className="sidebar-footer-text">
            <div className="sidebar-footer-title">
              Safe. Ethical. Confidential.
            </div>
            <div className="sidebar-footer-description">
              This platform uses AI for academic and research purposes only.
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;