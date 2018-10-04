function isNumeric(str){
   var allowedChars = "+0123456789";     //  For Checking Decimal , allowedChars = "0123456789.";
   var isDigit=true;
   var char;
   for (i = 0; i  < str.length && isDigit == true; i++){
      char = str.charAt(i);
      if (allowedChars.indexOf(char) == -1)  isDigit = false;
      }
   return isDigit;
}

function isAlpha(str){
   str = str.toLowerCase();
   var allowedChars = "-: abcdefghijklmnopqrstuvwxyz";     //  For Checking
   var isal=true;
   var char;
   for (i = 0; i  < str.length && isal == true; i++){
      char = str.charAt(i);
      if (allowedChars.indexOf(char) == -1){
        isal = false;}
      }
   return isal;
}

function validateForm(){
  var phone = document.getElementById("phone").value;
  var zip = document.getElementById("zip").value;
  var address = document.getElementsByClassName("address");
  var place = document.getElementsByClassName("place");

  if (((phone.length<8)||(phone.length>12))||(!isNumeric(phone)))
  {
    alert("Invalid Phone Number!");
    return false;
  }

  for(var i=0; i<address.length; i++){
    if(address[i].value.length<2){
      alert("Invalid "+address[i].name+"!");
      return false;}
  }

  for(i=0; i<place.length; i++){
    if((isAlpha(place[i].value)==false)||(place[i].value.length<2)){
      alert("Invalid "+place[i].name+"!");
      return false;}
  }

  if(isNumeric(zip)==false){
    alert("Invalid Zipcode!");
    return false;}
}

function checkEqual(){
  var zip = document.getElementsByName("zip")[0].value;
  var pass = document.getElementsByName("password")[0].value;
  var cnfrm_pass = document.getElementsByName("cnfrm_psswd")[0].value;

  if(isNumeric(zip)==false){
    alert("Invalid Zipcode!");
    return false;}

  if(pass!==cnfrm_pass){
    alert("Password and Confirm Password fields don't match");
    return false;
  }
}

function checkSelect(){
  var radio = document.getElementsByName("search method")
  var byKeyword = radio[0].checked
  var byCategory = radio[1].checked
  var both = radio[2].checked
  var select = document.getElementsByTagName("select").category.value
  if((byCategory||both)&&(select=="")){
    alert("Please Select Category")
    return false;}
}
