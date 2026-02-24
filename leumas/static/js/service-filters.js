/* Phase 1: Service Filter JavaScript */

$(function ($) {
    "use strict";

    // Service Filter Functionality
    const filterButtons = document.querySelectorAll('.filter-btn');
    const serviceItems = document.querySelectorAll('.service-item');

    if (filterButtons.length > 0 && serviceItems.length > 0) {
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Remove active class from all buttons
                filterButtons.forEach(btn => btn.classList.remove('active'));
                
                // Add active class to clicked button
                this.classList.add('active');
                
                // Get filter value
                const filterValue = this.getAttribute('data-filter');
                
                // Show/hide service items based on filter
                serviceItems.forEach(item => {
                    const itemCategory = item.getAttribute('data-category');
                    
                    if (filterValue === 'all' || itemCategory === filterValue) {
                        item.classList.remove('hidden');
                        item.style.display = 'block';
                        // Trigger re-animation
                        void item.offsetWidth;
                        item.style.animation = 'none';
                        setTimeout(() => {
                            item.style.animation = '';
                        }, 50);
                    } else {
                        item.classList.add('hidden');
                        item.style.display = 'none';
                    }
                });
            });
        });
    }

    // Initialize: Show all services by default
    if (serviceItems.length > 0) {
        serviceItems.forEach(item => {
            item.style.display = 'block';
        });
    }
});
