const monthLookup = {
    "January": "00",
    "February": "01",
    "March": "02",
    "April": "03",
    "May": "04",
    "June": "05",
    "July": "06",
    "August": "07",
    "September": "08",
    "October": "09",
    "November": "10",
    "December": "11"
}

function getDayFromHeader() {
    var day = document.getElementById("date").innerHTML.split(" ");
    day[1] = parseInt(day[1]) < 10 ? "0" + day[1][0] : day[1][0] + day[1][1];
    const date = day[2] + "-" + monthLookup[day[0]] + "-" + day[1];

    return date;
}

function changeDate() {
    var form = document.createElement("form");
    form.setAttribute("method", "GET");

    var text = document.createTextNode("New Date: ");

    var inputElement = document.createElement("input");
    inputElement.setAttribute("type", "date");
    inputElement.setAttribute("id", "date");
    inputElement.setAttribute("name", "date");
    inputElement.value = getDayFromHeader();

    var submitButton = document.createElement("input");
    submitButton.setAttribute("type", "submit");

    form.appendChild(text);
    form.appendChild(inputElement);
    form.appendChild(submitButton);

    var h3Element = document.getElementById("date-header");
    h3Element.innerHTML = "";
    
    h3Element.appendChild(form);
}