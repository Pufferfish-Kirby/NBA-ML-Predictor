import { useEffect, useState } from "react";
import TeamCard from "./TeamCard";
import "./App.css";

function App() {
  // useState hook: teams is the state variable, setTeams is the function to update it
  // Empty array [] is the initial state
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // useEffect runs after component renders
  // Empty dependency array [] means it only runs once on mount
  useEffect(() => {
    console.log("Fetching teams from http://127.0.0.1:8000/teams");
    fetch("http://127.0.0.1:8000/teams")
      .then(res => {
        console.log("Response status:", res.status);
        if (!res.ok) {
          throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        }
        return res.json(); // Parse JSON response
      })
      .then(data => {
        console.log("Teams data received:", data);
        if (!Array.isArray(data)) {
          throw new Error("Expected array but got: " + typeof data);
        }
        setTeams(data); // Update state with fetched data
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching teams:", err);
        setError(`Failed to load teams: ${err.message}. Make sure the backend is running on http://127.0.0.1:8000`);
        setLoading(false);
      });
  }, []); // Empty array = run once on mount

  if (loading) {
    return (
      <div className="app-container">
        <div className="loading">Loading team predictions...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app-container">
        <div className="error">Error: {error}</div>
      </div>
    );
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1 className="app-title">NBA Season Predictions</h1>
        <p className="app-subtitle">ML-Powered Win Predictions for 2025-26 Season</p>
      </header>
      
      <div className="teams-grid">
        {/* Map over teams array and render TeamCard for each team */}
        {teams.length === 0 ? (
          <div className="error">No teams data available</div>
        ) : (
          teams.map(team => (
            <TeamCard key={team.team_id} team={team} />
          ))
        )}
      </div>
    </div>
  );
}

export default App;
