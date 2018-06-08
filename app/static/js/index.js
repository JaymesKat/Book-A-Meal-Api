function viewForm(evt, userType) {
    var i, formHolder, tablinks;
    formHolder = document.getElementsByClassName("formContent");
    for (i = 0; i < formHolder.length; i++) {
        formHolder[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(userType).style.display = "block";
    evt.currentTarget.className += " active";
}
