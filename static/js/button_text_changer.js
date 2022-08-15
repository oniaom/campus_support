// Gets button with text "show solution" and changes it to "hide solution" upon click
window.addEventListener('load', function () {
    let buttons = document.getElementsByClassName("btn");

    for (let i = 0; i < buttons.length; i++) {
        buttons[i].addEventListener("click", function () {

            if (buttons[i].innerHTML == "Hide Solution") {
                buttons[i].innerHTML = "Show Solution";
            }
            else {
                buttons[i].innerHTML = "Hide Solution";
            }

        });
    }
});
