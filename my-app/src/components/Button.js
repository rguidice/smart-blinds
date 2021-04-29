import './Button.css'
//File that implements the button to enable or disable autocontrol
function Button ({autoControl, onAutoControl}){
  //Function to change the state of the autoControl variable using the onAutoControl
  //function. Both are passed from the App. In addition, a funciton autocontrol() is
  //called to request the backend to run the autoControl Python function in the Flask webserver
  const toggleClass = () => {
    autocontrol()
    onAutoControl(!autoControl);
  };
  function autocontrol(){
    //requests the running of the autoControl Python function in the Flask webserver
    fetch('/autocontrol').then(res => res.json());
  };
  return(
    //The apperance of the button changes on click, depending on the current state of the
    //button. In addition, the toggleClass function is run
    <div className={autoControl ? 'autocontrolon':'autocontroloff'} onClick={toggleClass}>
        {autoControl ? "Disable Autocontrol":"Enable Autocontrol"}
    </div>
  );
}
export default Button
