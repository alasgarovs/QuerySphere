var selectedRowNumber = null;

function addRow() {
    var declareName = document.getElementById('declare_name').value;
    var variableType = document.getElementById('variable_type').value;

    var table = document.getElementById('variables-table').getElementsByTagName('tbody')[0];

    // Check if declareName or variableType is empty
    if (declareName.trim() === '' || variableType.trim() === '') {
        // Display an error message or take appropriate action
        alert("Declare Name and Variable Type cannot be empty");
        return;
    }

    if (selectedRowNumber !== null) {
        // Update the values in the selected row
        var selectedRow = table.rows[selectedRowNumber - 1];
        selectedRow.cells[1].innerHTML = declareName;
        selectedRow.cells[2].innerHTML = variableType;

        // Clear the selected row number
        selectedRowNumber = null;

        // Enable all "Edit" buttons
        enableAllEditButtons();
    } else {
        var newRow = table.insertRow(table.rows.length);
        var cell1 = newRow.insertCell(0);
        var cell2 = newRow.insertCell(1);
        var cell3 = newRow.insertCell(2);
        var cell4 = newRow.insertCell(3);

        cell1.innerHTML = table.rows.length;
        cell2.innerHTML = declareName;
        cell3.innerHTML = variableType;

        cell4.innerHTML = '<svg width="16" height="16" fill="currentColor" class="bi bi-pencil-fill" viewBox="0 0 16 16" onclick="editRow(this)">' +
                          '<path d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.5.5 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11z"/>' +
                          '</svg>';
    }


    enableAllEditButtons();
}

function editRow(button) {
    var row = button.parentNode.parentNode;
    selectedRowNumber = row.cells[0].innerHTML;
    var name = row.cells[1].innerHTML;
    var variableType = row.cells[2].innerHTML;

    document.getElementById('declare_name').value = name;
    document.getElementById('variable_type').value = variableType;

    
    disableAllEditButtons();
}


function removeRow() {
    if (selectedRowNumber !== null) {
        // Remove the selected row
        var table = document.getElementById('variables-table').getElementsByTagName('tbody')[0];
        table.deleteRow(selectedRowNumber - 1);

        // Clear the selected row number
        selectedRowNumber = null;

        // Update row numbers
        updateRowNumbers();

        // Enable all "Edit" buttons
        enableAllEditButtons();
    }
}


function cancelEdit() {
    // Clear the selected row number
    selectedRowNumber = null;

    // Enable all "Edit" buttons
    enableAllEditButtons();
}


// Function to update row numbers after a row is removed
function updateRowNumbers() {
    var table = document.getElementById('variables-table').getElementsByTagName('tbody')[0];
    var rows = table.getElementsByTagName('tr');

    for (var i = 0; i < rows.length; i++) {
        rows[i].cells[0].innerHTML = i + 1;
    }
}



function disableAllEditButtons() {
    var table = document.getElementById('variables-table').getElementsByTagName('tbody')[0];
    var rows = table.getElementsByTagName('tr');

    for (var i = 0; i < rows.length; i++) {
        var cell4 = rows[i].cells[3];
        cell4.style.pointerEvents = 'none';
        cell4.style.color = 'grey';
    }
    document.getElementById('removeButton').style.display = 'block';
    document.getElementById('cancelButton').style.display = 'block';
    document.getElementById('addButton').innerText = 'Save';
}

function enableAllEditButtons() {
    var table = document.getElementById('variables-table').getElementsByTagName('tbody')[0];
    var rows = table.getElementsByTagName('tr');

    for (var i = 0; i < rows.length; i++) {
        var cell4 = rows[i].cells[3];
        cell4.style.pointerEvents = 'auto';
        cell4.style.color = '#007bff';
    }
    document.getElementById('declare_name').value = '';
    document.getElementById('variable_type').value = '';
    document.getElementById('removeButton').style.display = 'none';
    document.getElementById('cancelButton').style.display = 'none';
    document.getElementById('addButton').innerText = 'Add';
}

function collectTableValues() {
    var table = document.getElementById('variables-table').getElementsByTagName('tbody')[0];
    var rows = table.getElementsByTagName('tr');
    var tableData = [];

    for (var i = 0; i < rows.length; i++) {
        var rowData = {
            name: rows[i].cells[1].innerHTML,
            variable: rows[i].cells[2].innerHTML
        };

        tableData.push(rowData);
    }

    // Include tableData in the form submission
    document.getElementById('tableDataInput').value = JSON.stringify(tableData);
}

function collectTableValues() {
      var tableData = collectTableData();
      document.getElementById('tableDataInput').value = JSON.stringify(tableData);
    }

    function collectTableData() {
      var tableData = [];
      var tableRows = document.getElementById('variables-table').getElementsByTagName('tbody')[0].getElementsByTagName('tr');

      for (var i = 0; i < tableRows.length; i++) {
        var rowData = {};
        rowData['Name'] = tableRows[i].getElementsByTagName('td')[1].innerText;
        rowData['Type'] = tableRows[i].getElementsByTagName('td')[2].innerText;

        tableData.push(rowData);
      }

      return tableData;
    }



function deleteUser(button) {
    const userId = $(button).data('user-id');

    $.ajax({
        url: `/users/user/${userId}`,
        type: 'DELETE',
        success: function(url) {
            window.location.href = url;
        }
    });
}