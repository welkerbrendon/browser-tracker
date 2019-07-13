function submitNewTime(date) {
    $.get("/main?date=" + date, function (result, textStatus) {
        if (textStatus == "success") {
            document.write(result);
            document.close();
        }
    });
}

function handleInput(element) {
    if (element.value.length > 2) {
        if (isNaN(element.value)) {
            handlePreFormatted(element);
        }
        else {
            handleNumOnly(element);
        }
    }
    else {
        document.getElementById("error").innerHTML = "ERROR: invalid time. Too few numbers given.";
        var button = document.getElementById("submit-button");
        button.type = "hidden";
        button.style.display = "none";
    }
}

function handleCharacter(element) {
    var cleanValue = "";
    var count = 0;
    for (var i = 0; i < element.value.length; i++) {
        cleanValue += ((!isNaN(element.value[i]) && element.value[i] != " ")
                      || (element.value[i] == ":" && count < 1)) ? element.value[i] : "";
        if (element.value[i] == ":") {
            count++;
        }
    }
    element.value = cleanValue;
}

function handlePreFormatted(element) {
    var hours = parseInt(element.value.split(":")[0]);
    var minutes = parseInt(element.value.split(":")[1]);

    if (hours > 12 || minutes > 59 || hours < 1 || minutes < 0) {
        document.getElementById("error").innerHTML = "ERROR: Invalid time. Please follow format of (1-12):(00-59)";
        var button = document.getElementById("submit-button");
        button.type = "hidden";
        button.style.display = "none";
    }
}

function handleNumOnly(element) {
    const valueAsInt = parseInt(element.value);
    if (valueAsInt < 100 || valueAsInt > 1300 || (valueAsInt % 100 > 59) || (parseInt(valueAsInt / 100) > 12)) {
        document.getElementById("error").innerHTML = "ERROR: Invalid time. Please input at least 3 numbers representing the hours (1-12) and minutes (00-59).";
        var button = document.getElementById("submit-button");
        button.type = "hidden";
        button.style.display = "none";
    }
    else {
        if (element.value.length == 3) {
            element.value = `0${element.value[0]}:${element.value[1]}${element.value[2]}`;
            document.getElementById("error").innerHTML = "";
            var button = document.getElementById("submit-button");
            button.type = "submit";
            button.style.display = "";
        }
        else {
            element.value = `${element.value[0]}${element.value[1]}:${element.value[2]}${element.value[3]}`;
            document.getElementById("error").innerHTML = "";
            var button = document.getElementById("submit-button");
            button.type = "submit";
            button.style.display = "";
        }
    }
}