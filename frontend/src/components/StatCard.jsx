function StatCard({
  icon,
  value,
  label,
  description,
  type = "blue",
}) {

  return (
    <div className={`stat-card ${type}`}>

      <div className="stat-icon">
        {icon}
      </div>

      <div className="stat-content">

        <div className="stat-value">
          {value}
        </div>

        <div className="stat-label">
          {label}
        </div>

        <div className="stat-description">
          {description}
        </div>

      </div>

    </div>
  );
}

export default StatCard;