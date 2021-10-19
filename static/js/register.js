var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function showTab(n) {
  // This function will display the specified tab of the form...
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "block";
  //... and fix the Previous/Next buttons:
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == x.length - 1) {
    document.getElementById("nextBtn").innerHTML = "Submit";
  } else {
    document.getElementById("nextBtn").innerHTML = "Next";
  }
  //... and run a function that will display the correct step indicator:
  fixStepIndicator(n);
}

function nextPrev(n) {
  // This function will figure out which tab to display
  var x = document.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && !validateForm()) return false;
  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form...
  if (currentTab >= x.length) {
    // ... the form gets submitted:
    document.getElementById("regForm").submit();
    return false;
  }
  // Otherwise, display the correct tab:
  showTab(currentTab);
}

function validateForm() {
  // This function deals with validation of the form fields
  var x,
    y,
    i,
    valid = true;
  var Emailreg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
  var nameReg = /^[a-zA-Z\s]*$/;
  var StudentIdReg = /^[0-9]{12}/;
  var ContactReg = /^[0-9]{10}/;
  var passwordReg = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");
  // A loop that checks every input field in the current tab:
  for (i = 0; i < y.length; i++) {
    // If a field is empty...

    if (y[i].value == "") {
      // add an "invalid" class to the field:
      y[i].className += " invalid";
      ShowError(String(y[i].placeholder) + " cannot be empty");
      return;
      // and set the current valid status to false
      valid = false;
    }
    if (y[i].name == "StudentID") {
      if (!StudentIdReg.test(y[i].value.trim())) {
        y[i].className += " invalid";
        valid = false;
        ShowError(
          String(y[i].placeholder) + " has to be Numeric and of the length 12"
        );
        return;
      }
    }
    if (y[i].name == "lname") {
      if (!nameReg.test(y[i].value.trim())) {
        y[i].className += " invalid";
        valid = false;
        ShowError(String(y[i].placeholder) + " must contain only alphabets");
        return;
      }
    }
    if (y[i].name == "fname") {
      if (!nameReg.test(y[i].value.trim())) {
        y[i].className += " invalid";
        valid = false;
        ShowError(String(y[i].placeholder) + " must contain only alphabets");
        return;
      }
    }
    if (y[i].name == "phoneNo") {
      if (!ContactReg.test(y[i].value.trim())) {
        y[i].className += " invalid";
        valid = false;
        ShowError(
          String(y[i].placeholder) +
            " must contain only numbers and be of the lenght 10"
        );
        return;
      }
    }
    if (y[i].name == "email") {
      if (!Emailreg.test(y[i].value.trim())) {
        y[i].className += " invalid";
        valid = false;
      }
    }
    if (y[i].name == "pswd") {
      if (!passwordReg.test(y[i].value.trim())) {
        y[i].className += " invalid";
        valid = false;
        ShowError(
          String(y[i].placeholder) +
            " must be atleast of the length 8 and have atleast one number or alphabet"
        );
        return;
      }
      if (y[i].value != document.getElementsByName("pswd2")[0].value) {
        ShowError("Password do not match");
        valid = false;
        return;
      }
    }
  }
  // If the valid status is true, mark the step as finished and valid:
  if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
  }
  return valid; // return the valid status
}

function ShowError(error) {
  var errorCard = `    <div class="ErrorCard">


<i class="fa fa-exclamation-circle"></i>
<p>${error}</p>

</div>`;
  clearErrors();
  var Body = document.getElementsByClassName("errors")[0];

  Body.innerHTML += errorCard;
}

function clearErrors() {
  var Body = document.getElementsByClassName("errors")[0];
  Body.innerHTML = "";
}

function fixStepIndicator(n) {
  clearErrors();
  // This function removes the "active" class of all steps...
  var i,
    x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  //... and adds the "active" class on the current step:
  x[n].className += " active";
}
