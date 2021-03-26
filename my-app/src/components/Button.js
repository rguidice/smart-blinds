import './Button.css'

function Button ({autoControl, onAutoControl}){
  const toggleClass = () => {
    kachow();
    onAutoControl(!autoControl);
  };
  function kachow(){
    fetch('/time').then(res => res.json()).then(data => {
      console.log(data.text)
    });
  };
  return(
    <div className={autoControl ? 'autocontrolon':'autocontroloff'} onClick={toggleClass}>
        {autoControl ? "Disable Autocontrol":"Enable Autocontrol"}
    </div>
  );
}
export default Button
