import { MaterialIcon } from "./MaterialIcon";

interface ChatDashboardCardProps {
  onOpenDashboard?: () => void;
}

export function ChatDashboardCard({ onOpenDashboard }: ChatDashboardCardProps) {
  return (
    <div className="chat-dashboard-card" data-testid="chat-dashboard-card">
      <div className="chat-dashboard-card__icon-wrap">
        <MaterialIcon name="dashboard" size={40} className="chat-dashboard-card__icon" />
      </div>
      <h2 className="chat-dashboard-card__title">Painel de KPIs</h2>
      <p className="chat-dashboard-card__description">
        Gráficos e indicadores do PDV atualizados em tempo real.
      </p>
      <button
        type="button"
        className="chat-dashboard-card__cta"
        data-testid="chat-dashboard-cta"
        aria-label="Abrir painel de KPIs"
        onClick={onOpenDashboard}
      >
        Abrir painel
      </button>
    </div>
  );
}
