function loadFunds(pageNumber, folioId) {
    fetch(`?folio_id=${folioId}&funds_page=${pageNumber}`)
        .then(response => response.text())
        .then(html => {
            const fundsSection = document.getElementById('available-funds-section');
            fundsSection.innerHTML = html;  // Update the funds section with new HTML
        })
        .catch(error => console.error('Error loading funds:', error));
}
