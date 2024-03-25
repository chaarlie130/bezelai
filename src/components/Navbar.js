import React from 'react';
import '../styles/Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="logo">BEZEL</div>
      <div className="signin-button">
        Sign in
      </div>
    </nav>
  );
};

export default Navbar;