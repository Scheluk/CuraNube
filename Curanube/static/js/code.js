function getMessage() {
    const url = new URL("http://127.0.0.1:5000/msg")
    const searchText = document.getElementById("search-box").value

    data = {"user":searchText}

    for (let k in data) {url.searchParams.append(k, data[k])}
    fetch(url, {method: "GET"})
        .then(response => response.json())
        .then((data) => {
            const msgBoard = document.getElementById("msg")
            const text = document.createTextNode(JSON.stringify(data))
            msgBoard.append(text)
        })
}

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
    const url = new URL("http://worldclockapi.com/api/json/utc/now")
    fetch(url, {method: "GET"})
        .then(response => response.json())
        .then((data) => {
            const msgBoard = document.getElementById("display_time")
            const text = document.createTextNode(JSON.stringify(data.currentDateTime))
            msgBoard.append(text)
        })
}

/*async function submitLogin(username, password) {
    const response = await fetch.
    const formData = new FormData(e.target)
    const formProps = Object
}*/





