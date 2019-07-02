const monthLookup = {
    "January": "01",
    "February": "02",
    "March": "03",
    "April": "04",
    "May": "05",
    "June": "06",
    "July": "07",
    "August": "08",
    "September": "09",
    "October": "10",
    "November": "11",
    "December": "12"
}

function getDayFromHeader() {
    var day = document.getElementById("date").innerHTML;
    if (day.includes("-")) {
        return day;
    }
    else {
        day = day.split(" ");
        day[1] = parseInt(day[1]) < 10 ? "0" + day[1][0] : day[1][0] + day[1][1];
        const date = day[2] + "-" + monthLookup[day[0]] + "-" + day[1];

        return date;
    }
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