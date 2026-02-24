/* Phase 2: Advanced Interactions JavaScript */

$(function($) {
    "use strict";

    // Intersection Observer for Scroll Reveal Animation
    const revealElements = document.querySelectorAll('.reveal');
    
    if (revealElements.length > 0 && 'IntersectionObserver' in window) {
        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                    revealObserver.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -100px 0px'
        });

        revealElements.forEach(element => {
            revealObserver.observe(element);
        });
    }

    // Cursor Following Effect
    const cursorFollowElements = document.querySelectorAll('.cursor-follow');
    let mouseX = 0;
    let mouseY = 0;

    if (cursorFollowElements.length > 0) {
        document.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;

            cursorFollowElements.forEach(element => {
                const rect = element.getBoundingClientRect();
                const elementX = rect.left + rect.width / 2;
                const elementY = rect.top + rect.height / 2;

                const distX = mouseX - elementX;
                const distY = mouseY - elementY;

                element.style.setProperty('--mouse-x', distX + 'px');
                element.style.setProperty('--mouse-y', distY + 'px');
            });
        });
    }

    // Smooth Scroll Behavior
    $('a[href*="#"]').on('click', function(e) {
        e.preventDefault();
        const target = $(this.getAttribute('href'));
        if (target.length) {
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 100
            }, 1000);
        }
    });

    // Parallax Scroll Effect
    const parallaxElements = $('.parallax');
    if (parallaxElements.length > 0 && $(window).width() > 768) {
        $(window).on('scroll', function() {
            const scrollTop = $(window).scrollTop();
            parallaxElements.each(function() {
                const elementOffset = $(this).offset().top;
                const distance = elementOffset - scrollTop;
                if (distance > -$(window).height() && distance < $(window).height() * 2) {
                    $(this).css('background-position', 'center ' + (distance * 0.5) + 'px');
                }
            });
        });
    }

    // Staggered List Animation
    const staggerLists = $('.stagger-list');
    staggerLists.each(function() {
        $(this).find('li').each(function(index) {
            $(this).css('animation-delay', (index * 0.1) + 's');
        });
    });

    // Counter Animation
    const counters = $('.counter');
    let hasAnimated = false;

    function animateCounters() {
        counters.each(function() {
            const $counter = $(this);
            const target = parseInt($counter.attr('data-target')) || parseInt($counter.text());
            const increment = target / 50;
            let current = 0;

            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    $counter.text(target);
                    clearInterval(timer);
                } else {
                    $counter.text(Math.floor(current));
                }
            }, 50);
        });
    }

    // Trigger counter animation when visible
    if (counters.length > 0 && 'IntersectionObserver' in window) {
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !hasAnimated) {
                    animateCounters();
                    hasAnimated = true;
                    counterObserver.disconnect();
                }
            });
        }, { threshold: 0.5 });

        counters.parent().each(function() {
            counterObserver.observe(this);
        });
    }

    // Tooltip Functionality
    $('[data-tooltip]').on('mouseenter', function() {
        const tooltip = $('<div class="custom-tooltip"></div>')
            .text($(this).attr('data-tooltip'))
            .appendTo('body');

        const isAbove = $(this).offset().top - tooltip.height() > 0;
        tooltip
            .css({
                position: 'absolute',
                left: $(this).offset().left + $(this).width() / 2 - tooltip.width() / 2,
                top: isAbove ? $(this).offset().top - tooltip.height() - 10 : $(this).offset().top + $(this).height() + 10,
                opacity: 1
            });
    }).on('mouseleave', function() {
        $('.custom-tooltip').remove();
    });

    // Flip Card Interaction
    const flipCards = $('.flip-card-inner');
    flipCards.each(function() {
        const $card = $(this);
        let isFlipped = false;

        $card.parent().on('click', function() {
            isFlipped = !isFlipped;
            if (isFlipped) {
                $card.css('transform', 'rotateY(180deg)');
            } else {
                $card.css('transform', 'rotateY(0)');
            }
        });
    });

    // Gradient Text Animation
    const gradientTexts = $('.gradient-text');
    gradientTexts.each(function() {
        $(this).css({
            backgroundImage: 'linear-gradient(45deg, #4285f4, #667eea, #764ba2)',
            backgroundSize: '300% 300%',
            animation: 'gradient-shift 8s ease infinite'
        });
    });

    // Smooth Underline Animation
    $('.underline-animation').each(function() {
        const $link = $(this);
        $link.on('mouseenter', function() {
            $(this).css('--underline-width', '100%');
        }).on('mouseleave', function() {
            $(this).css('--underline-width', '0%');
        });
    });

    // Text Reveal on Scroll
    const textRevealElements = $('.text-reveal');
    if (textRevealElements.length > 0 && 'IntersectionObserver' in window) {
        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    $(entry.target).addClass('active');
                }
            });
        }, { threshold: 0.5 });

        textRevealElements.each(function() {
            revealObserver.observe(this);
        });
    }

    // Blob Animation Trigger
    const blobElements = $('.blob-bg');
    if (blobElements.length > 0) {
        blobElements.each(function() {
            $(this).on('mouseenter', function() {
                $(this).css('--blob-speed', '0.5s');
            }).on('mouseleave', function() {
                $(this).css('--blob-speed', '8s');
            });
        });
    }

    // Shimmer Loading Effect
    const shimmerElements = $('.shimmer');
    if (shimmerElements.length > 0) {
        // Automatically remove shimmer after content loads
        setTimeout(() => {
            shimmerElements.fadeOut(400, function() {
                $(this).remove();
            });
        }, 2000);
    }

    // Floating Animation for Icons
    const floatingElements = $('.floating');
    floatingElements.each(function(index) {
        $(this).css('animation-delay', (index * 0.2) + 's');
    });

    // Bounce Icon on Hover
    $('.bounce-icon').on('mouseenter', function() {
        $(this).css('animation-iteration-count', '2');
    }).on('mouseleave', function() {
        $(this).css('animation-iteration-count', 'infinite');
    });

    // Glow Pulse on Active Elements
    $('.glow-pulse').each(function() {
        $(this).on('mouseenter', function() {
            $(this).css('--glow-intensity', '1');
        }).on('mouseleave', function() {
            $(this).css('--glow-intensity', '0.5');
        });
    });

    // Initialize AOS (if script is included)
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true
        });
    }

    // Morph Shape Animation
    const morphShapes = $('.morph-shape');
    if (morphShapes.length > 0) {
        morphShapes.each(function() {
            $(this).css('animation-delay', (Math.random() * 2) + 's');
        });
    }

    // Window Resize Handler for Responsive adjustments
    $(window).on('resize', function() {
        if ($(window).width() < 768) {
            // Disable parallax on mobile
            parallaxElements.css('background-attachment', 'scroll');
        } else {
            parallaxElements.css('background-attachment', 'fixed');
        }
    });

    // Trigger resize on load
    $(window).trigger('resize');
});
