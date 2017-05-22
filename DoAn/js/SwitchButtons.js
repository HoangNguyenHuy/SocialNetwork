function SwitchButtons(buttonId) {
  var hideBtn, hideBt, showBtn, showBtn1;
  if (buttonId == 'button1') {
    showBtn = 'button2';
    showBtn1 = 'button3';
    hideBtn = 'button1';
	$("#inputUser").prop("readonly", false);
	$("#inputFullname").prop("readonly", false);
	$("#inputPhone").prop("readonly", false);
	$("#inputPassword").prop("readonly", false);
  }
  if (buttonId == 'button2') {
    showBtn = 'button1';
    document.getElementById('button3').style.display = 'none';
    hideBtn = 'button2';
    
  }
  //I don't have your menus, so this is commented out.  just uncomment for your usage
  // document.getElementById(menuToggle).toggle(); //step 1: toggle menu
  document.getElementById(hideBtn).style.display = 'none'; //step 2 :additional feature hide button
  
  document.getElementById(showBtn).style.display = ''; 
  document.getElementById(showBtn1).style.display = ''; //step 3:additional feature show button
  
}