import React from 'react';
import './TopBar.css';

function TopBar({ onToggleSidebar }) {
  return (
    <div className="top-bar">
      <button className="toggle-btn" onClick={onToggleSidebar}>
        <div className="hamburger">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </button>
      <h1 className="title">Game Sorter</h1>
    </div>
  );
}

export default TopBar; 