var dropdown = document.getElementsByClassName("dropdown-btn");
var i;

for (i = 0; i < dropdown.length; i++) {
  dropdown[i].addEventListener("click", function () {
    this.classList.toggle("active");
    var dropdownContent = this.nextElementSibling;

    if (dropdownContent.style.display === "block") {
      dropdownContent.style.display = "none";
    } else {
      dropdownContent.style.display = "block";
    }
  });
}
// var s;
function toggle2() {
  var temp1 = document.getElementById("mySidenav");
  var temp2 = document.getElementById("flexArea");
  (style = window.getComputedStyle(temp1)),
    (width = style.getPropertyValue("width"));
  (style = window.getComputedStyle(temp2)),
    (ml = style.getPropertyValue("margin-left"));
  // console.log(ml);
  // console.log(width);
  if (width == "0px") {
    temp1.style.width = "250px";
  } else {
    temp1.style.width = "0px";
  }
  if (ml == "0px") {
    temp2.style.marginLeft = "250px";
  } else {
    temp2.style.marginLeft = "0px";
  }

  // if (s == 0) {
  //   openNav();
  //   s = 1;
  // } else {
  //   closeNav();
  //   s = 0;
  // }
}
// function openNav() {
//   document.getElementById("mySidenav").style.width = "250px";
//   document.getElementById("flexArea").style.marginLeft = "250px";
// }

// function closeNav() {
//   document.getElementById("mySidenav").style.width = "0";
//   document.getElementById("flexArea").style.marginLeft = "0";
// }
function toggleF() {
  try {
    var temp3 = document.getElementsByClassName("openbtn")[0];
    temp3.className = "openbtnhide";
  } catch {
    var temp3 = document.getElementsByClassName("openbtnhide")[0];
    temp3.className = "openbtn";
  }
  var temp1 = document.getElementById("mySidenav");
  var temp2 = document.getElementById("flexArea");
  (style = window.getComputedStyle(temp1)),
    (width = style.getPropertyValue("width"));
  (style = window.getComputedStyle(temp2)),
    (ml = style.getPropertyValue("margin-left"));
  // console.log(ml);
  // console.log(width);
  if (width == "0px") {
    temp1.style.width = "250px";
  } else {
    temp1.style.width = "0px";
  }
  if (ml == "0px") {
    temp2.style.marginLeft = "250px";
  } else {
    temp2.style.marginLeft = "0px";
  }
  var UserNav = document.getElementById("usernav");
  UserNav.classList.toggle("usernavhide");
  // if (s == 0) {
  //   openNav();
  //   s = 1;
  // } else {
  //   closeNav();
  //   s = 0;
  // }
}

