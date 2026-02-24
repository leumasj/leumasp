/* Phase 3: Blog Search & Filtering JavaScript */

$(function($) {
    "use strict";

    const searchInput = $('#blog-search');
    const filterPills = $('.filter-pill');
    const blogItems = $('.blog-item');
    const sortOptions = $('#sort-by');
    const resultsCount = $('.search-results-count');
    let allBlogs = blogItems.length;

    // Initialize
    const blogData = {};
    blogItems.each(function() {
        const $item = $(this);
        const id = $item.data('blog-id');
        blogData[id] = {
            title: $item.find('.blog-title').text().toLowerCase(),
            content: $item.find('.blog-description').text().toLowerCase(),
            tags: ($item.data('tags') || '').toString().toLowerCase(),
            category: $item.data('category') || 'general',
            date: $item.data('date') || '',
            views: parseInt($item.data('views')) || 0,
            element: $item
        };
    });

    // Search functionality
    function performSearch() {
        const searchTerm = searchInput.val().toLowerCase();
        const activeCategory = $('filter-pill.active').data('filter') || 'all';
        let visibleCount = 0;

        blogItems.each(function() {
            const $item = $(this);
            const id = $item.data('blog-id');
            const blog = blogData[id];

            if (!blog) return;

            // Check if blog matches search term
            const matchesSearch = searchTerm === '' || 
                                blog.title.includes(searchTerm) || 
                                blog.content.includes(searchTerm) || 
                                blog.tags.includes(searchTerm);

            // Check if blog matches category filter
            const matchesCategory = activeCategory === 'all' || 
                                   blog.category === activeCategory;

            if (matchesSearch && matchesCategory) {
                $item.removeClass('hidden');
                visibleCount++;
                if (searchTerm !== '') {
                    $item.addClass('highlighted');
                    setTimeout(() => $item.removeClass('highlighted'), 600);
                }
            } else {
                $item.addClass('hidden');
            }
        });

        updateResultsCount(visibleCount);
        sortBlogs(sortOptions.val());
    }

    // Update results count
    function updateResultsCount(count) {
        if (resultsCount.length) {
            if (count === 0) {
                resultsCount.html(`<strong>No results found</strong> for your search`);
            } else {
                resultsCount.html(`Found <strong>${count}</strong> blog${count !== 1 ? 's' : ''}`);
            }
        }
    }

    // Sort blogs
    function sortBlogs(sortBy) {
        const $container = blogItems.parent();
        const visibleBlogs = blogItems.filter(':not(.hidden)');

        const blogsArray = visibleBlogs.get().sort(function(a, b) {
            const aData = blogData[$(a).data('blog-id')];
            const bData = blogData[$(b).data('blog-id')];

            switch(sortBy) {
                case 'newest':
                    return new Date(bData.date) - new Date(aData.date);
                case 'oldest':
                    return new Date(aData.date) - new Date(bData.date);
                case 'popular':
                    return bData.views - aData.views;
                case 'title-asc':
                    return aData.title.localeCompare(bData.title);
                case 'title-desc':
                    return bData.title.localeCompare(aData.title);
                default:
                    return 0;
            }
        });

        blogItems.detach();
        $container.append(visibleBlogs.get());
        visibleBlogs.get().forEach((blog, index) => {
            $(blog).css('animation-delay', (index * 0.05) + 's');
        });
    }

    // Event Listeners
    if (searchInput.length) {
        searchInput.on('input', performSearch);
        searchInput.on('keydown', function(e) {
            if (e.key === 'Escape') {
                searchInput.val('').trigger('input');
            }
        });
    }

    if (filterPills.length) {
        filterPills.on('click', function(e) {
            e.preventDefault();
            filterPills.removeClass('active');
            $(this).addClass('active');
            performSearch();
        });
    }

    if (sortOptions.length) {
        sortOptions.on('change', function() {
            sortBlogs($(this).val());
        });
    }

    // Clear search button
    const clearButton = $('.clear-search');
    if (clearButton.length) {
        clearButton.on('click', function() {
            searchInput.val('').trigger('input').focus();
        });
    }

    // Initialize with count
    updateResultsCount(allBlogs);

    // Export function for external use
    window.blogSearch = {
        search: performSearch,
        clear: function() {
            searchInput.val('').trigger('input');
        },
        filter: function(category) {
            filterPills.removeClass('active');
            filterPills.filter(`[data-filter="${category}"]`).addClass('active');
            performSearch();
        }
    };
});
