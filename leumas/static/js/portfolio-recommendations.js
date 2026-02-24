/* Phase 3: Portfolio Recommendations JavaScript */

$(function($) {
    "use strict";

    // Initialize recommendations when portfolio detail page loads
    const portfolioDetail = $('.portfolio-details');
    if (portfolioDetail.length === 0) return;

    const currentTags = portfolioDetail.data('tags') || '';
    const currentId = portfolioDetail.data('portfolio-id');
    const tagArray = currentTags.toString().split(',').map(tag => tag.trim().toLowerCase()).filter(tag => tag);

    // Calculate match score between two tag arrays
    function calculateMatchScore(tags1, tags2) {
        if (tags1.length === 0 || tags2.length === 0) return 0;
        
        const matches = tags1.filter(tag => tags2.includes(tag));
        return Math.round((matches.length / Math.max(tags1.length, tags2.length)) * 100);
    }

    // Generate portfolio recommendations
    function generateRecommendations() {
        const recommendations = [];

        // Get all portfolio items
        const allPortfolios = $('[data-portfolio-item]');
        
        allPortfolios.each(function() {
            const $item = $(this);
            const id = $item.data('portfolio-id');
            
            // Skip current portfolio
            if (id === currentId) return;

            const portfolioTags = $item.data('tags') || '';
            const tagList = portfolioTags.toString().split(',').map(tag => tag.trim().toLowerCase()).filter(tag => tag);
            const matchScore = calculateMatchScore(tagArray, tagList);

            if (matchScore > 0) {
                recommendations.push({
                    id: id,
                    element: $item,
                    title: $item.data('title') || 'Untitled',
                    image: $item.find('img').attr('src') || '',
                    description: $item.find('.portfolio-desc').text() || '',
                    tags: tagList,
                    matchScore: matchScore,
                    url: $item.find('a').attr('href') || '#'
                });
            }
        });

        // Sort by match score (descending)
        recommendations.sort((a, b) => b.matchScore - a.matchScore);

        // Return top 3 recommendations
        return recommendations.slice(0, 3);
    }

    // Render recommendations card
    function renderRecommendations(recommendations) {
        const container = $('.recommendations-grid');
        
        if (recommendations.length === 0) {
            container.html(`
                <div class="no-recommendations" style="grid-column: 1 / -1;">
                    <i class="fas fa-search"></i>
                    <p>No recommendations available at this time.</p>
                </div>
            `);
            return;
        }

        let html = '';
        recommendations.forEach((rec, index) => {
            html += `
                <div class="recommendation-card" style="animation-delay: ${index * 0.1}s;">
                    <div class="recommendation-image">
                        <img src="${rec.image}" alt="${rec.title}">
                        <span class="recommendation-badge">${rec.matchScore}% Match</span>
                    </div>
                    <div class="recommendation-content">
                        <h4 class="recommendation-title">${rec.title}</h4>
                        <p class="recommendation-description-short">${rec.description.substring(0, 80)}...</p>
                        <div class="recommendation-tags">
                            ${rec.tags.slice(0, 3).map(tag => `<span class="recommendation-tag">${tag}</span>`).join('')}
                        </div>
                        <div class="match-score">
                            <span class="match-label">Match Score</span>
                            <div class="match-bar">
                                <div class="match-fill" style="width: ${rec.matchScore}%;"></div>
                            </div>
                            <span class="match-percentage">${rec.matchScore}%</span>
                        </div>
                        <a href="${rec.url}" class="recommendation-cta">View Project →</a>
                    </div>
                </div>
            `;
        });

        container.html(html);

        // Add click event to cards
        container.find('.recommendation-card').on('click', function() {
            window.location.href = $(this).find('.recommendation-cta').attr('href');
        });
    }

    // Initialize recommendations
    const recommendations = generateRecommendations();
    if (recommendations.length > 0) {
        renderRecommendations(recommendations);
    }

    // Export for external use
    window.portfolioRecommendations = {
        generate: generateRecommendations,
        render: renderRecommendations,
        refresh: function() {
            const recs = generateRecommendations();
            renderRecommendations(recs);
        }
    };
});
