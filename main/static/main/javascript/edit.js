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
    var endTime = extractTime(endTimeString)
    tableRow.children[1].innerHTML = `<input type="text" value="${startTime}" style="text-align: center" maxlength="5" size="5" oninput="handleCharacter(this)" onchange="handleInput(this)" placeholder="- - : - -" name="start_time">
                        <select class="am/pm" name="start_time_am/pm">
                            <option value='AM'>AM</option>
                            <option value='PM'>PM</option>
                        </select>`;
    tableRow.children[2].innerHTML = `<input type="text" value="${endTime}" style="text-align: center" maxlength="5" size="5" oninput="handleCharacter(this)" onchange="handleInput(this)" placeholder="- - : - -" name="end_time">
                        <select class="am/pm" name="end_time_am/pm">
                            <option value='AM'>AM</option>
                            <option value='PM'>PM</option>
                        </select>`;
    button.setAttribute("onclick", `submitEditedSiteVisit(${id}, this)`);
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