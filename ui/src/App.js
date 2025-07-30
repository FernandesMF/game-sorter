import React, { useState, useEffect, useCallback } from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import api from './api';
import Sidebar from './components/Sidebar';
import TopBar from './components/TopBar';
import ComingSoon from './components/ComingSoon';
import './App.css';

function GameSorter({ children }) {
  return (
    <>
      <nav className="nav-container mb-4">
        <div className="nav-wrapper">
          <Link 
            className={`nav-item ${window.location.pathname === '/' ? 'active' : ''}`} 
            to="/"
          >
            Game Library
          </Link>
        </div>
      </nav>
      {children}
    </>
  );
}

function App() {
  const [games, setGames] = useState([]); // State to hold the fetched games
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    sort_by: 'score',
    title: '',
    score: null,
    genre: [],
    labels: [],
    must_play: null,
    finished: null
  });
  const [availableGenres, setAvailableGenres] = useState([]);
  const [availableLabels, setAvailableLabels] = useState([]);
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);

  const fetchGames = useCallback(async () => {
    setLoading(true);
    try {
      // Build query parameters, filtering out empty values
      const params = {};
      Object.keys(filters).forEach(key => {
        if (filters[key] !== null && filters[key] !== '' && 
            !(Array.isArray(filters[key]) && filters[key].length === 0)) {
          params[key] = filters[key];
        }
      });

      const response = await api.get('/games', { params });
      setGames(response.data);
      
      // Extract unique genres and labels for filter options
      const genres = new Set();
      const labels = new Set();
      response.data.forEach(game => {
        if (game.genres) game.genres.forEach(genre => genres.add(genre));
        if (game.labels) game.labels.forEach(label => labels.add(label));
      });
      setAvailableGenres(Array.from(genres));
      setAvailableLabels(Array.from(labels));
      
      setLoading(false);
    } catch (error) {
      console.error("Error fetching games:", error);
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchGames();
  }, [fetchGames]);

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleGenreToggle = (genre) => {
    setFilters(prev => ({
      ...prev,
      genre: prev.genre.includes(genre) 
        ? prev.genre.filter(g => g !== genre)
        : [...prev.genre, genre]
    }));
  };

  const handleLabelToggle = (label) => {
    setFilters(prev => ({
      ...prev,
      labels: prev.labels.includes(label) 
        ? prev.labels.filter(l => l !== label)
        : [...prev.labels, label]
    }));
  };

  const clearFilters = () => {
    setFilters({
      sort_by: 'score',
      title: '',
      score: null,
      genre: [],
      labels: [],
      must_play: null,
      finished: null
    });
  };

  const renderGamesTable = () => (
    <div className="mb-5">
      <h2 className="mb-3">Games ({games.length})</h2>
      <div className="table-responsive">
        <table className="table table-hover">
          <thead>
            <tr>
              <th>Title</th>
              <th>Score</th>
              <th>Genres</th>
              <th>Labels</th>
              <th>Must Play</th>
              <th>Finished</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {games.map((game, index) => (
              <tr key={index}>
                <td><strong>{game.title}</strong></td>
                <td>
                  <span className={`badge ${
                    game.metacritic_score >= 80 ? 'bg-success' :
                    game.metacritic_score >= 60 ? 'bg-warning' :
                    game.metacritic_score ? 'bg-danger' : 'bg-secondary'
                  }`}>
                    {game.metacritic_score || 'N/A'}
                  </span>
                </td>
                <td>
                  {game.genres && game.genres.length > 0 ? (
                    <div className="d-flex flex-wrap gap-1">
                      {game.genres.map((genre, idx) => (
                        <span key={idx} className="badge bg-info">{genre}</span>
                      ))}
                    </div>
                  ) : '-'}
                </td>
                <td>
                  {game.labels && game.labels.length > 0 ? (
                    <div className="d-flex flex-wrap gap-1">
                      {game.labels.map((label, idx) => (
                        <span key={idx} className="badge bg-secondary">{label}</span>
                      ))}
                    </div>
                  ) : '-'}
                </td>
                <td>
                  <span className={`badge ${
                    game.must_play === true ? 'bg-success' :
                    game.must_play === false ? 'bg-light text-dark' : 'bg-secondary'
                  }`}>
                    {game.must_play === true ? 'Yes' : game.must_play === false ? 'No' : 'N/A'}
                  </span>
                </td>
                <td>
                  <span className={`badge ${
                    game.finished === true ? 'bg-success' :
                    game.finished === false ? 'bg-warning' : 'bg-secondary'
                  }`}>
                    {game.finished === true ? 'Done' : game.finished === false ? 'Pending' : 'N/A'}
                  </span>
                </td>
                <td>
                  {game.fetch_error ? (
                    <span className="badge bg-danger">Error</span>
                  ) : (
                    <span className="badge bg-success">OK</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  const toggleSidebar = () => {
    setIsSidebarCollapsed(!isSidebarCollapsed);
  };

  return (
    <div className="app">
      <TopBar onToggleSidebar={toggleSidebar} />
      <Sidebar isCollapsed={isSidebarCollapsed} />
      <div className={`main-content ${isSidebarCollapsed ? 'expanded' : ''}`}>
        <Routes>
          <Route path="/analytics" element={<ComingSoon />} />
          <Route path="/settings" element={<ComingSoon />} />
          <Route path="/" element={
            <GameSorter>
              <>
                {/* Filters Section */}
                <div className="row mb-4">
                  <div className="col-md-12">
                    <div className="card">
                      <div className="card-body">
                        <div className="d-flex justify-content-between align-items-center mb-3">
                          <h5 className="card-title mb-0">Game Filters</h5>
                          <button className="btn btn-outline-secondary btn-sm" onClick={clearFilters}>
                            Clear Filters
                          </button>
                        </div>
                        
                        <div className="row">
                          {/* Title Search */}
                          <div className="col-md-3 mb-3">
                            <label className="form-label">Search Title</label>
                            <input
                              type="text"
                              className="form-control"
                              placeholder="Enter game title..."
                              value={filters.title}
                              onChange={(e) => handleFilterChange('title', e.target.value)}
                            />
                          </div>
                          
                          {/* Sort By */}
                          <div className="col-md-2 mb-3">
                            <label className="form-label">Sort By</label>
                            <select 
                              className="form-select" 
                              value={filters.sort_by} 
                              onChange={(e) => handleFilterChange('sort_by', e.target.value)}
                            >
                              <option value="score">Score</option>
                              <option value="title">Title</option>
                            </select>
                          </div>
                          
                          {/* Min Score */}
                          <div className="col-md-2 mb-3">
                            <label className="form-label">Min Score</label>
                            <input
                              type="number"
                              className="form-control"
                              placeholder="0-100"
                              min="0"
                              max="100"
                              value={filters.score || ''}
                              onChange={(e) => handleFilterChange('score', e.target.value ? parseInt(e.target.value) : null)}
                            />
                          </div>
                          
                          {/* Must Play Filter */}
                          <div className="col-md-2 mb-3">
                            <label className="form-label">Must Play</label>
                            <select 
                              className="form-select" 
                              value={filters.must_play === null ? '' : filters.must_play.toString()} 
                              onChange={(e) => handleFilterChange('must_play', e.target.value === '' ? null : e.target.value === 'true')}
                            >
                              <option value="">All</option>
                              <option value="true">Yes</option>
                              <option value="false">No</option>
                            </select>
                          </div>
                          
                          {/* Finished Filter */}
                          <div className="col-md-2 mb-3">
                            <label className="form-label">Status</label>
                            <select 
                              className="form-select" 
                              value={filters.finished === null ? '' : filters.finished.toString()} 
                              onChange={(e) => handleFilterChange('finished', e.target.value === '' ? null : e.target.value === 'true')}
                            >
                              <option value="">All</option>
                              <option value="true">Finished</option>
                              <option value="false">Pending</option>
                            </select>
                          </div>
                        </div>
                        
                        {/* Genres Filter */}
                        {availableGenres.length > 0 && (
                          <div className="mb-3">
                            <label className="form-label">Genres</label>
                            <div className="d-flex flex-wrap gap-2">
                              {availableGenres.map((genre, index) => (
                                <div key={index} className="form-check">
                                  <input
                                    className="form-check-input"
                                    type="checkbox"
                                    id={`genre-${index}`}
                                    checked={filters.genre.includes(genre)}
                                    onChange={() => handleGenreToggle(genre)}
                                  />
                                  <label className="form-check-label" htmlFor={`genre-${index}`}>
                                    {genre}
                                  </label>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                        
                        {/* Labels Filter */}
                        {availableLabels.length > 0 && (
                          <div className="mb-3">
                            <label className="form-label">Labels</label>
                            <div className="d-flex flex-wrap gap-2">
                              {availableLabels.map((label, index) => (
                                <div key={index} className="form-check">
                                  <input
                                    className="form-check-input"
                                    type="checkbox"
                                    id={`label-${index}`}
                                    checked={filters.labels.includes(label)}
                                    onChange={() => handleLabelToggle(label)}
                                  />
                                  <label className="form-check-label" htmlFor={`label-${index}`}>
                                    {label}
                                  </label>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
                
                {/* Games Table */}
                {loading ? (
                  <div className="text-center py-5">
                    <div className="spinner-border" role="status">
                      <span className="visually-hidden">Loading...</span>
                    </div>
                    <p className="mt-2">Loading games...</p>
                  </div>
                ) : (
                  renderGamesTable()
                )}
              </>
            </GameSorter>
          } />
        </Routes>
      </div>
    </div>
  );
}

export default App;
