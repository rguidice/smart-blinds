import './Button.css'

function Button ({autoControl, onAutoControl}){
  const toggleClass = () => {
    //kachow()
    autocontrol()
    onAutoControl(!autoControl);
  };
  function autocontrol(){
    console.log("HI FROM AUTOCONTROL")
    fetch('/autocontrol').then(res => res.json());
  };
  return(
    <div className={autoControl ? 'autocontrolon':'autocontroloff'} onClick={toggleClass}>
        {autoControl ? "Disable Autocontrol":"Enable Autocontrol"}
    </div>
  );
}
export default Button
