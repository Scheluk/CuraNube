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






