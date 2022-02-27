const deleteField = document.getElementById("id_delete_field")
const deleteConfirm = document.getElementById("delete-confirm")

deleteField.addEventListener('input', (event) => {
    deleteConfirm.disabled = event.target.value !== "DELETE";
})