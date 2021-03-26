import './App.css';
import React, { useState } from "react";
import SlidingButton from './components/SlidingButton.js'
import Button from './components/Button.js'

function App() {
  const [autoControl, setAutoControl] = useState(false);
  
  return (
    <div className="App">
      <header className="Header">
          What would you like to do?
      </header>
      <SlidingButton autoControl={autoControl}/>
      <Button autoControl={autoControl} onAutoControl={setAutoControl}/>
    </div>
  );
}

export default App;
