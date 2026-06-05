import { Outlet, useLocation, useNavigationType } from "react-router-dom";

export function PageTransitionLayout() {
  const location = useLocation();
  const navigationType = useNavigationType();
  const direction = navigationType === "POP" ? "back" : "forward";

  return (
    <div
      key={location.pathname}
      className={`page-transition page-transition--${direction}`}
      data-testid="page-transition"
      data-transition-direction={direction}
    >
      <Outlet />
    </div>
  );
}
