document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('createCollectionForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const name = document.getElementById('collectionName').value;
        const description = document.getElementById('collectionDescription').value;
        const meals = document.getElementById('collectionMeals').value;
        fetch('/collections/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, description, meals })
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById('creationMessage').textContent = data.message;
            document.getElementById('createCollectionForm').reset();
        });
    });
});
