async function uploadCSV() {
    const fileInput = document.getElementById("csvFileInput").files[0];
    if (!fileInput) {
        alert("Please select a CSV file to upload.");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput);

    try {
        let response = await fetch("http://localhost:8000/upload-api/", {
            method: "POST",
            body: formData
        });

        let data = await response.json();
        if (data.csv_data) {
            alert("File uploaded successfully!");
            displayCSVData(data.csv_data);
        } else {
            alert("Error uploading file.");
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

function displayCSVData(csvData) {
    let table = document.getElementById("csvTable");
    let thead = table.querySelector("thead");
    let tbody = table.querySelector("tbody");
    thead.innerHTML = "";
    tbody.innerHTML = "";

    if (csvData.length === 0) return;

    // Table Header
    let headers = Object.keys(csvData[0]);
    let headerRow = document.createElement("tr");
    headers.forEach(header => {
        let th = document.createElement("th");
        th.textContent = header;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);

    // Table Body
    csvData.forEach((row, index) => {
        let tr = document.createElement("tr");
        headers.forEach(header => {
            let td = document.createElement("td");
            td.textContent = row[header];
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
}

async function updateRow() {
    let rowId = document.getElementById("rowId").value;
    let columnName = document.getElementById("columnName").value;
    let newValue = document.getElementById("newValue").value;

    if (!rowId || !columnName || !newValue) {
        alert("Please fill all fields.");
        return;
    }

    let updateData = {};
    updateData[columnName] = newValue;

    try {
        let response = await fetch(`http://localhost:8000/update-csv-row/${rowId}/`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(updateData)
        });

        let result = await response.json();
        alert(result.message || "Update successful!");
    } catch (error) {
        console.error("Error updating:", error);
    }
}