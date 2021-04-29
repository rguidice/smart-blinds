import './App.css';
//Imports useState from React, this allows use of the state hook
import React, { useState } from "react";
import SlidingButton from './components/SlidingButton.js'
import Button from './components/Button.js'

function App() {
  //A state to determine if autocontrol is on
  //Necessary at this level because both the sliding button as
  //well as the autocontrol button rely on the state of autocontrol
  const [autoControl, setAutoControl] = useState(false);

  return (
    <div className="App">
      <header className="Header">
          What would you like to do?
      </header>
      {/*Lines below add the button to open and close the blinds and the autocontrol button
      the autoControl variable is passed as a prop to the sliding button */}
      <SlidingButton autoControl={autoControl}/>
      {/* The autoControl variable and setAutoControl function are passed as props
      to the button */}
      <Button autoControl={autoControl} onAutoControl={setAutoControl}/>
    </div>
  );
}

export default App;
