import { Link } from "react-router-dom";

import { MaterialIcon } from "../chat/MaterialIcon";

type PageBackLinkProps = {
  to: string;
  label: string;
  testId?: string;
};

export function PageBackLink({
  to,
  label,
  testId = "page-back-link",
}: PageBackLinkProps) {
  return (
    <Link to={to} className="dashboard-page__back" data-testid={testId}>
      <MaterialIcon name="arrow_back" size={20} />
      <span>{label}</span>
    </Link>
  );
}
