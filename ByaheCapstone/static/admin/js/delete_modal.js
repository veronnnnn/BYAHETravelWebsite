document.addEventListener('DOMContentLoaded', () => {
    const deleteButtons = document.querySelectorAll('.delete-button');
    const modal = document.getElementById('deleteModal');
    const deleteForm = modal.querySelector('#deleteUserForm');
    const confirmDeleteButton = modal.querySelector('#confirmDeleteButton');

    deleteButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault(); // Prevent default button behavior
            const userId = button.getAttribute('data-user-id'); // Get the user ID
            if (userId) {
                deleteForm.setAttribute('action', `/delete-user/${userId}/`); // Update form action with correct user ID
            } else {
                console.error('User ID not found');
            }
        });
    });

    confirmDeleteButton.addEventListener('click', () => {
        deleteForm.submit(); // Submit the form to delete the user
    });
});