//basic & sloppy vanilla JS to handle form submission and dynamic field generation
//KEEP IT SIMPLE STUPID

var extraction_options = {
    "gabor_extraction": null,
    "hamming_distance": null,
    "wavelength": null,
    "verbose": null,
    "threads": null,
    "batchSize": null,
    "bitShifts": null
};

document.getElementById('parameters_form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    var formData = new FormData(this);

    formData.forEach(function(value, key) {
        extraction_options[key] = value;
    });

    var json = JSON.stringify(extraction_options, null, 2);
    console.log(json);

    fetch('http://localhost:8000', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: json,
    })
    .then(response => response.text())
    .catch(error => console.error('Error:', error));

    alert("ANALYSIS CONTINUING IN YOUR TERMINAL! YOU MAY NOW CLOSE THIS WINDOW.");

});

document.getElementById('Analysis').addEventListener('change', function() {
    var extraFieldsDiv = document.getElementById('conditional_fields');
    extraFieldsDiv.innerHTML = '';

    var selectedOption = this.value;

    if (selectedOption === '1') {
        extraction_options["gabor_extraction"] = "True"
        extraction_options["hamming_distance"] = "False"
        feature_extraction(extraFieldsDiv, false);
    } else if (selectedOption === '2') {
        extraction_options["gabor_extraction"] = "False"
        extraction_options["hamming_distance"] = "True"
        hamming_distance(extraFieldsDiv);
    } else if (selectedOption === '3') {
        extraction_options["gabor_extraction"] = "True"
        extraction_options["hamming_distance"] = "True"
        feature_extraction(extraFieldsDiv, true);
    }
});

function feature_extraction(extraFieldsDiv, hamming) {
    var span_1 = document.createElement('span');
    span_1.setAttribute('class', 'space');
    span_1.textContent = 'Verbose:';
    extraFieldsDiv.appendChild(span_1);

    var inputVebose_true = document.createElement('input');
    inputVebose_true.type = 'radio';
    inputVebose_true.id = 'Verbose_true';
    inputVebose_true.name = 'verbose';
    inputVebose_true.checked = true; 
    inputVebose_true.value = "True";
    inputVebose_true.required = true;
    inputVebose_true.placeholder = 'Input for Option 1';
    extraFieldsDiv.appendChild(inputVebose_true);

    var labelVerbose_true = document.createElement('label');
    labelVerbose_true.setAttribute('for', 'Verbose_true');
    labelVerbose_true.textContent = 'True';
    extraFieldsDiv.appendChild(labelVerbose_true);

    var inputVerbose_false = document.createElement('input');
    inputVerbose_false.type = 'radio';
    inputVerbose_false.id = 'Verbose_false';
    inputVerbose_false.name = 'verbose';
    inputVerbose_false.value = "False";
    extraFieldsDiv.appendChild(inputVerbose_false);

    var labelVerbose_false = document.createElement('label');
    labelVerbose_false.setAttribute('for', 'Verbose_false');
    labelVerbose_false.textContent = 'False';
    extraFieldsDiv.appendChild(labelVerbose_false);

    extraFieldsDiv.appendChild(document.createElement('br'));
    
    var labelThreads = document.createElement('label');
    labelThreads.setAttribute('for', 'threads');
    labelThreads.setAttribute('class', 'space');
    labelThreads.textContent = 'Processing Threads:';
    labelThreads.required = true;
    extraFieldsDiv.appendChild(labelThreads);

    var inputThreads = document.createElement('input');
    inputThreads.type = 'number';
    inputThreads.id = 'threads';
    inputThreads.name = 'threads';
    inputThreads.value = '16';
    inputThreads.className = 'number-class';
    extraFieldsDiv.appendChild(inputThreads);
    extraFieldsDiv.appendChild(document.createElement('br'));

    var labelWavelength = document.createElement('label');
    labelWavelength.setAttribute('for', 'wavelength');
    labelWavelength.setAttribute('class', 'space');
    labelWavelength.textContent = 'Wavelength: ';
    extraFieldsDiv.appendChild(labelWavelength);

    var inputWavelength = document.createElement('input');
    inputWavelength.type = 'number';
    inputWavelength.id = 'wavelength';
    inputWavelength.name = 'wavelength';
    inputWavelength.value = '18';
    inputWavelength.className = 'number-class';
    extraFieldsDiv.appendChild(inputWavelength);

    extraFieldsDiv.appendChild(document.createElement('br'));
    extraFieldsDiv.appendChild(document.createElement('hr'));

    if (hamming === true){
        //extraFieldsDiv.appendChild(document.createElement('br'))
        hamming_distance(extraFieldsDiv)
    }
}

function hamming_distance(extraFieldsDiv) {
    var span_2 = document.createElement('span');
    span_2.setAttribute('class', 'space');
    span_2.textContent = 'Roll codes:';
    extraFieldsDiv.appendChild(span_2);

    var inputBitShifts_true = document.createElement('input');
    inputBitShifts_true.type = 'radio';
    inputBitShifts_true.id = 'Shifts_true';
    inputBitShifts_true.name = 'bitShifts';
    inputBitShifts_true.value = "True";
    inputBitShifts_true.checked = true;
    inputBitShifts_true.required = true;
    inputBitShifts_true.placeholder = 'Input for Option 1';
    extraFieldsDiv.appendChild(inputBitShifts_true);

    var labelBitShifts_true = document.createElement('label');
    labelBitShifts_true.setAttribute('for', 'Shifts_true');
    labelBitShifts_true.textContent = 'True';
    extraFieldsDiv.appendChild(labelBitShifts_true);

    var inputBitShifts_false = document.createElement('input');
    inputBitShifts_false.type = 'radio';
    inputBitShifts_false.id = 'Shifts_false';
    inputBitShifts_false.name = 'bitShifts';
    inputBitShifts_false.value = "False";
    extraFieldsDiv.appendChild(inputBitShifts_false);

    var labelBitShifts_false = document.createElement('label');
    labelBitShifts_false.setAttribute('for', 'Shifts_false');
    labelBitShifts_false.textContent = 'False';
    extraFieldsDiv.appendChild(labelBitShifts_false);

    extraFieldsDiv.appendChild(document.createElement('br'));

    var labelBatchSize = document.createElement('label');
    labelBatchSize.setAttribute('for', 'batchSize');
    labelBatchSize.setAttribute('class', 'space');
    labelBatchSize.textContent = 'Batch size: ';
    extraFieldsDiv.appendChild(labelBatchSize);

    var inputBatchSize = document.createElement('input');
    inputBatchSize.type = 'number';
    inputBatchSize.id = 'batchSize';
    inputBatchSize.name = 'batchSize';
    inputBatchSize.value = "4";
    inputBatchSize.className = 'number-class';
    extraFieldsDiv.appendChild(inputBatchSize);

    extraFieldsDiv.appendChild(document.createElement('br'));
    extraFieldsDiv.appendChild(document.createElement('hr'));
}