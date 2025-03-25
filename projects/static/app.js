function uploadFile() {
    let fileInput = document.getElementById("csvFile");
    let file = fileInput.files[0];

    if (!file) {
        alert("Please select a CSV file first.");
        return;
    }

    let formData = new FormData();
    formData.append("file", file);

    fetch("http://localhost:8000/upload-api/", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("message").innerHTML = `<span style="color:green;">File stored: ${file.name}</span>`;

        if (data.csv_data && data.csv_data.length > 0) {
            displayCSV(data.csv_data);
        } else {
            document.getElementById("message").innerHTML += `<br><span style="color:red;">No CSV data found!</span>`;
        }
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("message").innerHTML = `<span style="color:red;">File upload failed!</span>`;
    });
}

function displayCSV(csvData) {
    let tableContainer = document.getElementById("table-container");
    let table = document.getElementById("csvTable");
    let thead = table.querySelector("thead");
    let tbody = table.querySelector("tbody");

    // Clear old content
    thead.innerHTML = "";
    tbody.innerHTML = "";

    // Show Table
    tableContainer.style.display = "block";

    // Check if data is valid
    if (csvData.length === 0) {
        document.getElementById("message").innerHTML += `<br><span style="color:red;">Empty CSV file!</span>`;
        return;
    }

    // Table Headers
    let headerRow = document.createElement("tr");
    Object.keys(csvData[0]).forEach(key => {
        let th = document.createElement("th");
        th.innerText = key;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);

    // Table Data
    csvData.forEach(row => {
        let tr = document.createElement("tr");
        Object.values(row).forEach(value => {
            let td = document.createElement("td");
            td.innerText = value;
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
}
