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