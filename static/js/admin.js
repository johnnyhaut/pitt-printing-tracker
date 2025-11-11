window.addEventListener("load", setup); 

function setup(){
    retrieve_DOM_references(); 
    set_event_listeners(); 
}

// all the DOM references made on this page 
function retrieve_DOM_references(){
    newPrinterLocation_reference = document.getElementById("newPrinterLocation");
    newPrinterType_reference = document.getElementById("newPrinterType");
    newPrinterStatus_reference = document.getElementById("newPrinterStatus");
    addNewPrinter_reference = document.getElementById("submit_button"); 

}

// all the event listeners 
function set_event_listeners(){
    addNewPrinter_reference.addEventListener("click", addToDB); 
}

// used for adding a new printer to the database 
function addToDB(){
    // gets all the fields required
    console.log("INSIDE ADDTODB")
    console.log(newPrinterLocation_reference)
}