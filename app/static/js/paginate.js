function previous() {
    var previousform=document.getElementById("previousform");
        previousform.action="/log";
        previousform.submit();
}
function next() {
    var nextform=document.getElementById("nextform");
        nextform.action="/log";
        nextform.submit();
}