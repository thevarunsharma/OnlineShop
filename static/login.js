function validateForm(){
  var email = document.getElementById("email").value;
  var pass = document.getElementById("pass").value;
  if (email.length<5){
    alert("Please enter a valid Email!");
    return false;}
  if (pass===""){
    alert("Password field cannot be empty!")
    return false;}
}
