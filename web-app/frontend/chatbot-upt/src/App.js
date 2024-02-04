import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route, Switch, Link } from "react-router-dom";
import Home from "./pages/Home"

function App() {
  return (
    <div className="App">
      <Home/>
    </div>
  );
}

export default App;
