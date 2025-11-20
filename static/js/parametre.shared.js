function onChangeSelect(idSelect, dataKey, keyToFilter, id_selectFilter) {

    var valueToFilter = parseInt(document.getElementById(id_selectFilter).value);
    var Selection = document.getElementById(idSelect);
    Selection.innerHTML = '';

    var filteredData = dataTable[dataKey].filter(function (item) {
        return item[keyToFilter] === valueToFilter;
    });

    filteredData.forEach(opt => {
        var SelectOption = document.createElement('option');
        SelectOption.textContent = opt.description;
        SelectOption.value = opt.id;
        Selection.appendChild(SelectOption);
    })
}

function addDataToSelect(idSelect, dataKey) {
    var Selection = document.getElementById(idSelect);
    dataTable[dataKey].forEach(opt => {
        var SelectOption = document.createElement('option');
        SelectOption.textContent = opt.description;
        SelectOption.value = opt.id;
        Selection.appendChild(SelectOption);
    })
}