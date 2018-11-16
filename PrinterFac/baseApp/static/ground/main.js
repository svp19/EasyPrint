// function printPDF(file_path) {
//     // window.open('file://file_path')
//     document.write('file://' + file_path)
// }
function checkChecked() {
    const vic = document.getElementById("vic_but");
    if(document.getElementById("id_is_confirmed").checked === true) {
        vic.classList.remove("amy-crisp-gradient");
        vic.classList.add("blue-gradient");
        vic.innerHTML = "Confirm";
    }
}

