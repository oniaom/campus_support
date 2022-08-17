window.addEventListener('load', function () {
    let input = document.querySelector("input");
    document.getElementById("q").addEventListener("input", async function () {
        let response = await fetch("/search?q=" + input.value + "&plain=true");
        let database_results = await response.text();
        document.querySelector("tbody").innerHTML = database_results;
    });

});