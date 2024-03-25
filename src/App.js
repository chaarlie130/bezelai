import React from 'react';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import BestSellers from './components/BestSellers';
import Niches from './components/Niches';
import './App.css'; // Make sure your App.css sets up a layout that accommodates the sidebar

function App() {
  return (
    <div className="app-layout">
      <Navbar />
      <div className="content">
        <Sidebar />
        <div>
          <BestSellers />
          <Niches />
        </div>
      </div>
    </div>
  );
}

export default App;
