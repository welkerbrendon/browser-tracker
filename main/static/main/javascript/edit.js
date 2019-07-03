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

    var div = document.createElement("div");
    div.setAttribute("id", "date_input");

    var inputElement = document.createElement("input");
    inputElement.setAttribute("type", "date");
    inputElement.setAttribute("id", "start_date");
    inputElement.setAttribute("name", "start_date");
    inputElement.setAttribute("onchange", "setMinDate(this)");
    inputElement.value = formatDay(document.getElementById("date").innerHTML);

    var secondInput = document.createElement("input");
    secondInput.setAttribute("type", "text");
    secondInput.setAttribute("placeholder", "--Optional End Date--");
    secondInput.setAttribute("onmouseover", "this.type = 'date'");
    secondInput.setAttribute("onmouseleave", "endDateOnBlurHandler(this)");
    secondInput.setAttribute("name", "end_date");
    secondInput.setAttribute("id", "end_date");
    secondInput.setAttribute("onchange", "setMaxDate(this)");
    secondInput.value = "";

    var submitButton = document.createElement("input");
    submitButton.setAttribute("type", "submit");
    submitButton.setAttribute("id", "date_submit");

    form.appendChild(document.createTextNode("New Date: "));
    form.appendChild(inputElement);
    form.appendChild(document.createTextNode(" to "));
    form.appendChild(secondInput);
    form.appendChild(document.createTextNode("(Optional)"));
    form.appendChild(document.createElement("br"));
    form.appendChild(submitButton);

    div.appendChild(form);

    buttonElement = document.createElement("button");

    var h3Element = document.getElementById("date-header");
    h3Element.innerHTML = "";
    
    h3Element.appendChild(div);
}

function endDateOnBlurHandler(element) {
    if (element.value == "") {
        element.type = "text";
    }
}

function setMaxDate(element) {
    document.getElementById("start_date").max = element.value;
}

function setMinDate(element) {
    document.getElementById("end_date").min = element.value;

}