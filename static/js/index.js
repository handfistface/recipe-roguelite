let typingTimer;

function doneTyping() {
    const name = document.getElementById('name').value;
    const urlParams = new URLSearchParams(window.location.search);
    let per_page = urlParams.get('per_page');
    if (!per_page || per_page === 'null') {
        per_page = 10;
    }
    window.location.href = `/?page=1&per_page=${per_page}&name=${name}`;
}

function setupTypingTimer() {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(doneTyping, 2000);
}