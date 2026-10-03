import { Routes, Route, Navigate } from "react-router-dom";

import Sidebar from "./components/Sidebar";

import Dashboard from "./pages/Dashboard";
import CaseHandover from "./pages/CaseHandover";
import AuditHistory from "./pages/AuditHistory";

function App() {
  return (
    <div className="app-container">
      <Sidebar />

      <main className="main-content">
        <Routes>
          <Route
            path="/"
            element={<Navigate to="/dashboard" replace />}
          />

          <Route
            path="/dashboard"
            element={<Dashboard />}
          />

          <Route
            path="/handover"
            element={<CaseHandover />}
          />

          <Route
            path="/audit"
            element={<AuditHistory />}
          />
        </Routes>
      </main>
    </div>
  );
}

export default App;