function deleteEmployee(id) {
    if (confirm('Are you sure you want to delete this employee?')) {
        window.location.href = `/delete/${id}`;
    }
}

function editEmployee(id) {
    const daysWork = prompt('Enter number of days worked:');
    if (daysWork !== null && !isNaN(daysWork)) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/update_workdays/${id}`;
        
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'days_work';
        input.value = daysWork;
        
        form.appendChild(input);
        document.body.appendChild(form);
        form.submit();
    }
}