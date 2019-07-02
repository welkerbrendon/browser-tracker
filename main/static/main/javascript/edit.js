window.onload = setUp;

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

function setUp() {
    fixDateValues();
    if (document.getElementsByName("start_time_td").length > 0) {
        formatDefaultTimeValues();
    }
}

function formatDefaultTimeValues() {
    var startTimeTdElements = document.getElementsByName("start_time_td");
    var endTimeTdElements = document.getElementsByName("end_time_td");

    for (var i = 0; i < startTimeTdElements.length && i < endTimeTdElements.length; i++) {
        var startTime = startTimeTdElements[i].getAttribute("value").split(" ");
        startTimeTdElements[i].children[0].value = startTime[0];
        startTimeTdElements[i].children[1].value = startTime[1];

        var endTime = endTimeTdElements[i].getAttribute("value").split(" ");
        endTimeTdElements[i].children[0].value = endTime[0];
        endTimeTdElements[i].children[1].value = endTime[1];
    }
}

function fixDateValues() {
    var dateElements = document.getElementsByName("date");
    for (var i = 0; i < dateElements.length; i++) {
        dateElements[i].value = formatDay(dateElements[i].value);
    }
}

function formatDay(day) {
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
    inputElement.setAttribute("id", "start_date");
    inputElement.setAttribute("name", "start_date");
    inputElement.setAttribute("onchange", "setMaxDate(this)");
    inputElement.value = formatDay(document.getElementById("date").innerHTML);

    var secondInput = inputElement.cloneNode(true);
    secondInput.setAttribute("name", "end_date");
    secondInput.setAttribute("id", "end_date");
    secondInput.setAttribute("onchange", "setMinDate(this)");

    var submitButton = document.createElement("input");
    submitButton.setAttribute("type", "submit");

    form.appendChild(text);
    form.appendChild(inputElement);
    form.appendChild(secondInput);
    form.appendChild(submitButton);

    buttonElement = document.createElement("button");

    var h3Element = document.getElementById("date-header");
    h3Element.innerHTML = "";
    
    h3Element.appendChild(form);
}

function setMaxDate(element) {
    element.max = document.getElementById("end_date").value;
}

function setMinDate(element) {
    element.min = document.getElementById("start_date").value;

}