import './SlidingButton.css'
import React, { useState, useEffect } from "react";

  async function get_state(){
    const response = await fetch('/get_state')
    const lol = await response.json();
    console.log(lol, "HIHIHIHIH")
    return lol;
  };
  function open(){
    fetch('/open').then(res => res.json());
  };
  function closee(){
    fetch('/close').then(res => res.json());
  };


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
  //const [isActive, setActive] = useState(get_state);
  const state = useFetch();
  console.log(state)
  const [isActive, setActive] = useState(state);
  useEffect(
    () => {
      console.log("inside effect");
      setActive(state);
    },
    [state]
  );
  const onChange = event => {
    setActive(event.target.value);
  };
  console.log(isActive, "adskfl")
  const toggleClass = () => {
    isActive ? open() : closee();
    setActive(!isActive);
  };

  
  return (
    <div className={  autoControl ? 'containerdisable' : (isActive ? 'containernight':'containerday')}>
      <div className={autoControl ? 'disablebutton'    : (isActive ? 'nightbutton':'daybutton')  }
           onClick={autoControl ? null : toggleClass }>
          {autoControl ? 'Under Autocontrol': isActive ? "Open Blinds":"Close Blinds"}
      </div>
    </div>
  );
}

export default SlidingButton
