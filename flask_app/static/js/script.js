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
