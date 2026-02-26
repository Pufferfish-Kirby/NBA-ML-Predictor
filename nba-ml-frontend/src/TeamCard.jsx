import './TeamCard.css'; /// the div names correspond in the css, and then

// Component receives team data as props and displays it in a card
function TeamCard({ team }) {
  // Format win percentage as percentage string
  const formatWinPct = (pct) => `${(pct * 100).toFixed(1)}%`;
  
  // Get color based on predicted wins (higher = better)
  const getTeamColor = () => {
    if (team.predicted_final_wins >= 55) return '#1a7f37'; // Dark green for top teams
    if (team.predicted_final_wins >= 45) return '#4a7c3f'; // Green for good teams
    if (team.predicted_final_wins >= 35) return '#8b6914'; // Gold for average teams
    return '#7f1a1a'; // Red for struggling teams
  };

  return (
    <div className="team-card" >
      <div className="team-header" >
        <div className="team-logo-placeholder">
          {/* Placeholder for team logo - replace with actual logo image */}
          <span className="team-initials">
            {team.team_name.substring(0, 2).toUpperCase()}
          </span>
        </div>
        <div className="team-name-section">
          <h2 className="team-name">{team.team_name}</h2>
          <p className="team-current-record">
            {team.current_wins} - {team.current_losses}
          </p>
        </div>
      </div>

      <div className="team-stats">
        <div className="stat-row">
          <span className="stat-label">Predicted Final Record:</span>
          <span className="stat-value highlight">
            {team.predicted_final_wins} - {team.predicted_final_losses}
          </span>
        </div>
        <div className="stat-row"> 
          <span className="stat-label">Predicted Win %:</span>
          <span className="stat-value"  style={{ color: getTeamColor() }}>{formatWinPct(team.predicted_final_win_pct)}</span>
        </div>
      </div>
    </div>
  );
}

export default TeamCard;
