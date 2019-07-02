const monthLookup = {
    "January": "0",
    "February": "1",
    "March": "2",
    "April": "3",
    "May": "4",
    "June": "5",
    "July": "6",
    "August": "7",
    "September": "8",
    "October": "9",
    "November": "10",
    "December": "11"
}

function editRequest() {
    $.get("/main/edit?date=" + getDayFromHeader(), function (result, textStatus) {
        console.log(`result of edit request: ${textStatus} : ${JSON.stringify(result)}`);
    });
}

function getDayFromHeader() {
    var day = document.getElementById("date").innerHTML.split(" ");
    day[1].replace(",", "");
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