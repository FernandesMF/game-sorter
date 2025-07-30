import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Sidebar.css';

function Sidebar({ isCollapsed }) {
  const location = useLocation();

  return (
    <div className={`sidebar ${isCollapsed ? 'collapsed' : ''}`}>
      <div className="sidebar-content">
        <div className="menu-section">
          <div className="menu-header">Game Library</div>
          <div className="menu-items">
            <Link 
              to="/" 
              className={`menu-item ${location.pathname === '/' ? 'active' : ''}`}
            >
              <i className="fas fa-gamepad me-2"></i>
              All Games
            </Link>
          </div>
        </div>
        <div className="menu-section">
          <div className="menu-header">Tools</div>
          <div className="menu-items">
            <Link 
              to="/analytics" 
              className={`menu-item ${location.pathname === '/analytics' ? 'active' : ''}`}
            >
              <i className="fas fa-chart-bar me-2"></i>
              Analytics
            </Link>
          </div>
        </div>
        <div className="menu-section">
          <div className="menu-header">Management</div>
          <div className="menu-items">
            <Link 
              to="/settings" 
              className={`menu-item ${location.pathname === '/settings' ? 'active' : ''}`}
            >
              <i className="fas fa-cog me-2"></i>
              Settings
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Sidebar; 