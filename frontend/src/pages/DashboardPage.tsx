import { PageBackLink } from "../components/layout/PageBackLink";
import { MaterialIcon } from "../components/chat/MaterialIcon";
import { ROUTES } from "../config/routes";

export default function DashboardPage() {
  return (
    <div className="dashboard-page" data-testid="dashboard-page">
      <div className="dashboard-page__orb dashboard-page__orb--top" aria-hidden="true" />
      <div className="dashboard-page__orb dashboard-page__orb--bottom" aria-hidden="true" />

      <header className="dashboard-page__header">
        <PageBackLink to={ROUTES.home} label="Voltar ao início" testId="dashboard-back-link" />
      </header>

      <main className="dashboard-page__main">
        <div className="dashboard-page__hero">
          <div className="dashboard-page__icon-wrap">
            <MaterialIcon name="dashboard" size={40} className="dashboard-page__icon" />
          </div>
          <h1 className="dashboard-page__title">Painel de KPIs</h1>
          <p className="dashboard-page__description">
            Gráficos e indicadores do PDV atualizados em tempo real.
          </p>
        </div>

        <section className="dashboard-page__placeholder" aria-label="Área de gráficos">
          <MaterialIcon name="bar_chart" size={32} className="dashboard-page__placeholder-icon" />
          <p className="dashboard-page__placeholder-text">
            Os gráficos do painel serão exibidos aqui em breve.
          </p>
        </section>
      </main>
    </div>
  );
}
