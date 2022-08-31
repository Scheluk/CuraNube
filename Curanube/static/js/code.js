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
  formData.append("username", document.getElementById("newUsername").value);
  const data = Object.fromEntries(formData.entries())
  fetch("change_username", {
    method: "PUT",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(data),
  })
  .then((response) => response.json())
  .then((data) => {
    console.log("Success:", data);
  })
  .catch((error) => {
    console.log("Error:", error);
  })
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


