function showEditForm(exerciseId) {
    // Hide all other edit forms first
    var editForms = document.querySelectorAll('div[id^="exercise_edit_form_"]');
    editForms.forEach(function(form) {
        form.style.display = 'none';
    });
    
    // Hide all display divs
    var displayDivs = document.querySelectorAll('div[id^="exercise_display_"]');
    displayDivs.forEach(function(div) {
        div.style.display = 'block';
    });

    // Now show the edit form for the clicked exercise
    document.getElementById('exercise_display_' + exerciseId).style.display = 'none';
    document.getElementById('exercise_edit_form_' + exerciseId).style.display = 'block';
}

function hideEditForm(exerciseId) {
    document.getElementById('exercise_edit_form_' + exerciseId).style.display = 'none';
    document.getElementById('exercise_display_' + exerciseId).style.display = 'block';
}

function navigateToProgram(programId) {
    window.location.href = '/program/' + programId;
}

function addWeek(programId) {
    // Preventing default form submission
    event.preventDefault();

    // Getting data from the form
    const weekNumber = document.getElementById('weeknumber').value;

    // Setting up the AJAX request
    fetch(`/create-week/${programId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `weeknumber=${weekNumber}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            addWeekToDOM(data.week_id, data.weekNumber, programId);
            // Update week number for the next addition
            const weekNumberInput = document.getElementById('weeknumber');
            if (weekNumberInput) {
                weekNumberInput.value = data.nextWeekNumber;
            }
            // Check if the maximum number of weeks is reached
            if (data.nextWeekNumber >= 8) {
                // Hide the add week form/button
                const addWeekForm = document.getElementById('addWeekForm');
                if (addWeekForm) {
                    addWeekForm.style.display = 'none';
                }
                // Optionally, show the 'Maximum number of weeks reached' message
                const maxWeeksReachedMessage = document.getElementById('maxWeeksReachedMessage'); // Make sure to add this element to your HTML
                if (maxWeeksReachedMessage) {
                    maxWeeksReachedMessage.style.display = 'block';
                }
            }
        }
    });
}

function updateWeekNumber(nextWeekNumber) {
    const weekNumberInput = document.getElementById('weeknumber');
    if (weekNumberInput) {
        weekNumberInput.value = nextWeekNumber;
    }
}

function addWeekToDOM(weekId, weekNumber, programId) {
    const weeksContainer = document.getElementById('weeksContainer'); // Ensure this ID exists in your HTML
    if (!weeksContainer) {
        console.error('Weeks container element not found');
        return;
    }

    // Create the outer structure of the week card
    const weekCard = document.createElement('div');
    weekCard.className = 'week-card mb-4';

    const rowDiv = document.createElement('div');
    rowDiv.className = 'row';

    const colDiv = document.createElement('div');
    colDiv.className = 'col';

    // Header and Add Day Form
    const headerDiv = document.createElement('div');
    headerDiv.className = 'd-flex justify-content-between align-items-center mb-3';

    const innerDiv = document.createElement('div');
    innerDiv.className = 'd-flex align-items-center';

    const weekHeader = document.createElement('h2');
    weekHeader.className = 'mb-0';
    weekHeader.textContent = `Week ${weekNumber}`;

    // Add weekHeader to innerDiv
    innerDiv.appendChild(weekHeader);

    // Append innerDiv to headerDiv
    headerDiv.appendChild(innerDiv);

    // Create and append the Delete Week Form
    const deleteForm = document.createElement('form');
    deleteForm.action = `/delete-week/${weekId}/${programId}`;
    deleteForm.method = 'POST';

    const deleteButton = document.createElement('button');
    deleteButton.type = 'submit';
    deleteButton.className = 'btn btn-danger';
    deleteButton.textContent = 'Remove';

    if (weekNumber <= 7) {  // Adjust this condition based on your program's logic
        const addDayForm = document.createElement('form');
        addDayForm.action = `/create-day/${programId}`;
        addDayForm.method = 'POST';
        addDayForm.className = 'ml-2 form-inline'; // Add any additional classes as needed

        // Next day number is typically 1 since this is a new week
        const nextDayNumber = 1;

        // Create hidden inputs for the form
        const inputs = [
            { name: 'daynumber', value: nextDayNumber },
            { name: 'week_id', value: weekId },
            { name: 'completed', value: '0' },
            { name: 'RPE', value: '0' },
            { name: 'usernotes', value: '' }
        ];

        // Append inputs to the form
        inputs.forEach(inputInfo => {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = inputInfo.name;
            input.value = inputInfo.value;
            addDayForm.appendChild(input);
        });

        // Create and append the submit button to the form
        const addDayButton = document.createElement('button');
        addDayButton.type = 'submit';
        addDayButton.className = 'btn btn-success';
        addDayButton.textContent = 'Add Day';
        addDayForm.appendChild(addDayButton);

        // Append the form to the correct location within the weekCard
        // Assuming it should be inside the innerDiv
        innerDiv.appendChild(addDayForm);
    }

    deleteForm.appendChild(deleteButton);

    // Append deleteForm to headerDiv
    headerDiv.appendChild(deleteForm);

    // Append headerDiv to colDiv
    colDiv.appendChild(headerDiv);

    // Append colDiv to rowDiv
    rowDiv.appendChild(colDiv);

    // Append rowDiv to weekCard
    weekCard.appendChild(rowDiv);

    // Finally, append the new week card to the weeks container
    weeksContainer.appendChild(weekCard);
}
