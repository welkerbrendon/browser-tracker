window.onload = setUp;

var tableRow;

function setUp() {
    if (document.getElementsByName("table-row").length > 0) {
        var rowList = document.getElementsByName("table-row")
        tableRow = rowList[rowList.length - 1].cloneNode(true);
    }
}

function addRow() {
    var table = document.getElementById("day-input").children[0];
    table.appendChild(tableRow.cloneNode(true));
}

function deleteRow() {
    var tableRows = document.getElementById("day-input").children[0];
    if (tableRows.children.length > document.getElementById("row-num").value) {
        var i = tableRow.children.length - 1;
        var rowToDelete = tableRows.children[i];
        var keepGoing = rowToDelete ? (rowToDelete.nodeName == "TR" ? false : true) : true;
        while (keepGoing) {
            i--;
            rowToDelete = tableRows.children[i];
            keepGoing = rowToDelete ? (rowToDelete.nodeName == "TR" ? false : true) : true;
        }
        tableRows.removeChild(rowToDelete);
    }
}

function makeEditable(id, button) {
    var tableRow = document.getElementById(id);
    var startTimeString = tableRow.children[1].innerHTML;
    var endTimeString = tableRow.children[2].innerHTML;
    var startTime = extractTime(startTimeString);
    var endTime = extractTime(endTimeString);
    var startAmPm = startTimeString.includes("a") ? "AM" : "PM";
    var endAmPm = endTimeString.includes("a") ? "AM" : "PM";
    tableRow.children[1].innerHTML = `<input type="text" value="${startTime}" style="text-align: center" maxlength="5" size="5" oninput="handleCharacter(this)" onchange="handleInput(this)" placeholder="- - : - -" name="start_time">
                        <select class="am/pm" name="start_time_am/pm" value=${startAmPm}>
                            <option value='AM'>AM</option>
                            <option value='PM'>PM</option>
                        </select>`;
    tableRow.children[2].innerHTML = `<input type="text" value="${endTime}" style="text-align: center" maxlength="5" size="5" oninput="handleCharacter(this)" onchange="handleInput(this)" placeholder="- - : - -" name="end_time">
                        <select class="am/pm" name="end_time_am/pm" value=${endAmPm}>
                            <option value='AM'>AM</option>
                            <option value='PM'>PM</option>
                        </select>`;
    button.setAttribute("onclick", `submitEditedSiteVisit(${id}, this)`);
    button.innerHTML = "Submit";
}

function submitEditedSiteVisit(id, button) {
    var tableRow = document.getElementById(id);

    const startTime = tableRow.children[1].children[0].value + " " + tableRow.children[1].children[1].value;
    const startAmPm = startTime.split(" ")[1];
    const startHour = parseInt(startTime.split(":")[0]);
    const startMinutes = startTime.split(" ")[0].split(":")[1];
    const startTimeMilitary = startAmPm.toUpperCase().includes("A") || startHour == 12 ? startHour.toString() + ":" + startMinutes : 
                              startHour.toString() + ":" + startMinutes;

    const endTime = tableRow.children[2].children[0].value + " " + tableRow.children[2].children[1].value;
    const endAmPm = endTime.split(" ")[1];
    const endHour = parseInt(endTime.split(":")[0]);
    const endMinutes = endTime.split(" ")[0].split(":")[1];
    const endTimeMilitary = endAmPm.toUpperCase().includes("A") || endHour == 12 ? endHour.toString() + ":" + endMinutes : 
                            endHour.toString() + ":" + endMinutes;
    const jsonPostData = {
        start_time: startTimeMilitary,
        end_time: endTimeMilitary,
        id: id
    };
    $.post("site-visits/", jsonPostData, function (response, textStatus) {
        console.log(`Response: ${JSON.stringify(response)}`);
        if (textStatus == "success") {
            resetTableRow(id, startTime, endTime);
            button.innerHTML = Edit;
            button.setAttribute("onclick", `makeEditable(${id}, this)`);
        }
    });
}

function resetTableRow(id, startTime, endTime) {
    var tableRow = document.getElementById(id);

    tableRow.children[1].innerHTML = startTime;
    tableRow.children[2].innerHTML = endTime;
}

function extractTime(timeString) {
    var time_am_pm = timeString.split(" ");
    var military_time = "";
    if (time_am_pm.includes(":")) {
        var hour_min = time.split(":");
        military_time = time_am_pm[1].toUpperCase().includes("A") || parseInt(hour_min[0]) == 12 ? time_am_pm[0] :
        (parseInt(hour_min[0]) + 12).toString() + ":" + hour_min[1];
    }
    else {
        military_time = time_am_pm[1].toUpperCase().includes("A") || parseInt(time_am_pm[0]) == 12 ? time_am_pm[0] :
        (parseInt(time_am_pm[0]) + 12).toString();
        military_time += ":00";
    }
    return military_time;
}