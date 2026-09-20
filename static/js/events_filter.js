// Live Event Search & Dynamic Filter Engine

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchQuery');
    const categorySelect = document.getElementById('categorySelect');
    const locationInput = document.getElementById('locationInput');
    const eventsContainer = document.getElementById('eventsContainer');
    const countDisplay = document.getElementById('eventResultsCount');

    if (!eventsContainer) return;

    const cards = Array.from(eventsContainer.querySelectorAll('.event-card'));

    function filterEvents() {
        const query = searchInput ? searchInput.value.toLowerCase().trim() : '';
        const category = categorySelect ? categorySelect.value.toLowerCase().trim() : '';
        const location = locationInput ? locationInput.value.toLowerCase().trim() : '';

        let visibleCount = 0;

        cards.forEach(card => {
            const title = card.getAttribute('data-title') || '';
            const cardCategory = card.getAttribute('data-category') || '';
            const cardLocation = card.getAttribute('data-location') || '';

            const matchesTitle = !query || title.includes(query);
            const matchesCategory = !category || cardCategory === category;
            const matchesLocation = !location || cardLocation.includes(location);

            if (matchesTitle && matchesCategory && matchesLocation) {
                card.style.display = 'flex';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        if (countDisplay) {
            countDisplay.textContent = visibleCount;
        }
    }

    if (searchInput) searchInput.addEventListener('input', filterEvents);
    if (categorySelect) categorySelect.addEventListener('change', filterEvents);
    if (locationInput) locationInput.addEventListener('input', filterEvents);
});
