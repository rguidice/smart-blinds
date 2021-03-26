import './SlidingButton.css'
import React, { useState } from "react";

  function get_state(){
    var ret = fetch('/get_state').then(res => res.json()).then(data => {
        inside=data.state
        //Line below has correct state. cannot view outside of promise though, research about promises
        console.log("hi from inside", inside);
        return inside;
      });
      console.log("go home from outside", ret);
      console.log("FRICK", inside);
    return inside;
  };
  function open(){
    fetch('/open').then(res => res.json());
  };
  function closee(){
    fetch('/close').then(res => res.json());
  };



var inside = false;
function SlidingButton({autoControl}) {
  const [isActive, setActive] = useState(get_state());
  const toggleClass = () => {
    isActive ? open() : closee();
    setActive(!isActive);
  };


  
  return (
    <div className={  autoControl ? 'containerdisable' : (isActive ? 'containernight':'containerday')}>
    {console.log(isActive, "ADSFADSFASDFASDFADSFA")}
      <div className={autoControl ? 'disablebutton'    : (isActive ? 'nightbutton':'daybutton')  }
           onClick={autoControl ? null : toggleClass }>
          {autoControl ? 'Under Autocontrol': isActive ? "Open Blinds":"Close Blinds"}
      </div>
    </div>
  );
}

export default SlidingButton
