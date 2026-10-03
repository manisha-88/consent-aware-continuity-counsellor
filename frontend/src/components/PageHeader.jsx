function PageHeader({
  icon,
  title,
  subtitle,
}) {

  return (
    <div className="page-header">

      <div className="page-header-title">

        <span className="page-header-icon">
          {icon}
        </span>

        <h1>{title}</h1>

      </div>

      <p>
        {subtitle}
      </p>

    </div>
  );
}

export default PageHeader;