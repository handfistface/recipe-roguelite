// JS for Collection Ingredients page (currently minimal, can be expanded)
document.addEventListener('DOMContentLoaded', function() {
    // Ingredient row removal and undo functionality
    const table = document.getElementById('ingredients-table');
    const tbody = table ? table.querySelector('tbody') : null;
    const undoButton = document.getElementById('undo-button');
    const previewList = document.getElementById('undo-preview');
    const undoContainer = document.getElementById('undo-container');
    const container = document.querySelector('.container');

    // Style undo container is now handled by CSS
    if (undoContainer && container) {
        container.style.position = 'relative';
    }

    let undoStack = [];
    const MAX_UNDO = 5;

function updatePreview() {
    previewList.innerHTML = '';
    undoStack.slice(-MAX_UNDO).reverse().forEach(item => {
        const li = document.createElement('li');
        li.textContent = item.name;
        li.className = 'undo-preview-item';
        previewList.appendChild(li);
    });
}

    function handleRowClick(e) {
        const row = e.currentTarget;
        // Get ingredient name and measure from row
        const name = row.children[0].textContent;
        const measure = row.children[1].textContent;
        // Add to undo stack
        undoStack.push({ name, measure, row });
        if (undoStack.length > MAX_UNDO) undoStack = undoStack.slice(-MAX_UNDO);
        updatePreview();
        // Fade out animation
        row.style.transition = 'opacity 0.5s';
        row.style.opacity = '0';
        setTimeout(() => {
            row.style.display = 'none';
        }, 500);
    }

    if (tbody) {
        Array.from(tbody.rows).forEach(row => {
            row.style.cursor = 'pointer';
            row.addEventListener('click', handleRowClick);
        });
    }

    if (undoButton) {
        undoButton.addEventListener('click', function() {
            if (undoStack.length === 0) return;
            const last = undoStack.pop();
            // Restore row
            last.row.style.display = '';
            last.row.style.opacity = '0';
            setTimeout(() => {
                last.row.style.transition = 'opacity 0.5s';
                last.row.style.opacity = '1';
            }, 10);
            updatePreview();
        });
    }

    updatePreview();
});
