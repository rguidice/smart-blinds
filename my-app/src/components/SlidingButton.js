import './SlidingButton.css'
//Imports useState and useEffect from React, this allows use of the statem and effect hooks
import React, { useState, useEffect } from "react";

  //An asynchronous function to get the state of blinds; whether they are
  //open or closed
  async function get_state(){
    const response = await fetch('/get_state')
    const strResponse = await response.json();
    return strResponse;
  };
  //A function to request the backend to open the blinds
  function open(){
    fetch('/open').then(res => res.json());
  };
  //A function to request the backend to close the blinds
  function closee(){
    fetch('/close').then(res => res.json());
  };

  //A function to utilize useState and useEffect to update the local
  //state when the value of getState is received from the backend. This
  //allows for the Open/Close sliding button to render in the correct
  //location based on the position of the blinds
  const useFetch = () => {
    const [value, setValue] = useState("")
    useEffect(
      async () => {
        const response = await fetch('/get_state');
        const data = await response.json();
        setValue(data)
      },
      []
    );
    return value;
  }

function SlidingButton({autoControl}) {
  //sets the intial state to what is received by useFetch
  const state = useFetch();
  //Uses useState to determine whether to render the button as closed or open
  const [isActive, setActive] = useState(state);
  //updates the local state when the value from get_state is available
  useEffect(
    () => {
      setActive(state);
    },
    [state]
  );
  const onChange = event => {
    setActive(event.target.value);
  };
  //changes the appearance of the button when the button is pressed
  const toggleClass = () => {
    //if the blinds are open, closee is run, if the blinds are closed, open is run
    isActive ? open() : closee();
    setActive(!isActive);
  };


  return (
    //Both the container and Button appearance change based on if autoControl is active, as well as whether
    //the blinds are open or closed.
    <div className={  autoControl ? 'containerdisable' : (isActive ? 'containernight':'containerday')}>
      <div className={autoControl ? 'disablebutton'    : (isActive ? 'nightbutton':'daybutton')  }
           onClick={autoControl ? null : toggleClass }>
          {autoControl ? 'Under Autocontrol': isActive ? "Open Blinds":"Close Blinds"}
      </div>
    </div>
  );
}

export default SlidingButton
