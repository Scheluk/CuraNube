function loadImpressum() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
       document.getElementById("impressum").innerHTML = this.responseText;
      }
    };
    xhttp.open("GET", "../../static/img/impressum.txt", true);
    xhttp.send();
}

function getTime() {
    const url = new URL("http://worldtimeapi.org/api/ip")
    fetch(url, {method: "GET"})
        .then(response => response.json())
        .then((data) => {
            const msgBoard = document.getElementById("display_time")
            const text = document.createTextNode(JSON.stringify(data.datetime).replace("Z", " ").replace("T", " "))
            msgBoard.append(text)
        })
}

function getFact() {
    const url = new URL("https://catfact.ninja/fact")
    fetch(url, {method: "GET"})
        .then(response => response.json())
        .then((data) => {
            const msgBoard = document.getElementById("result")
            const text = document.createTextNode(JSON.stringify(data.fact))
            msgBoard.append(text)
            const breakl = document.createElement('br')
            msgBoard.append(breakl)
        })

}

function changeUsername() {
  const formData = new FormData();
  let newUsername = document.getElementById("newUsername").value
  formData.append("newUsername", newUsername);
  const data = Object.fromEntries(formData.entries())
  fetch("change_username", {
    method: "PUT",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(data),
  })
}

function changePassword() {
  const formData = new FormData();
  oldPWD = document.getElementById("old_password").value;
  newPWD = document.getElementById("new_password").value;
  confPWD = document.getElementById("confirm_password").value;
  formData.append("oldPassword", oldPWD);
  formData.append("newPassword", newPWD);
  formData.append("confPassword", confPWD);
  const data = Object.fromEntries(formData.entries())
  fetch("change_password", {
    method: "PUT",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(data),
  }).catch(response.status)
}

function deleteAccount() {
  fetch("delete_account", {
    method: "DELETE",
    headers: {"Content-Type": "application/json"},
  }).then(
    location.reload()
  );
}

/* Toggle between showing and hiding the navigation menu links when the user clicks on the hamburger menu / bar icon */
function myFunction() {
    var x = document.getElementById("meineBar");
    if (x.style.display === "block") {
      x.style.display = "none";
    } else {
      x.style.display = "block";
    }
  }


