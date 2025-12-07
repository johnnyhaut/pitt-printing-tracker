function applyFilters(){
        const type = document.getElementById("printer_type_selector").value;
        const status = document.getElementById("printer_status_selector").value;

        const printers = document.querySelectorAll(".printer-card");

        printers.forEach(card => {
            let matchesType = true;
            let matchesStatus = true;

            //Color Filter
            if(type == "black and white"){
                matchesType = card.classList.contains("bnw");
            }
            else if (type == "color"){
                matchesType = card.classList.contains("color");
            }
            //Status Filter
            if(status == "online"){
                matchesStatus = card.classList.contains("online");
            }
            else if (status == "offline"){
                matchesStatus = card.classList.contains("offline");
            }
            //Add more filters here

            //Show if filters match
            if(matchesType && matchesStatus){
                card.style.display = "block";
            }
            else{
                card.style.display = "none";
            }
        });
    
    }