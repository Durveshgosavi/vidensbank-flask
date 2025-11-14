// ============================================================================
// VIDENSBANK - Main JavaScript
// Professional Bootstrap-Based Implementation
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    initFlashMessages();
    initScrollAnimations();
    initNavbarScroll();
    initProgressBars();
    initStatCounters();
    initTimelineHighlight();
    addLoadingState();
    initSearchEnhancement();
    initCopyButtons();
    initLazyLoad();
    initKeyboardNav();
    initTooltips();
    initAwwCardsAnimation();
    initParallaxEffect();
});

// ============================================================================
// FLASH MESSAGES
// ============================================================================
function initFlashMessages() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
}

// Slideout animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ============================================================================
// SCROLL ANIMATIONS (Reveal on scroll)
// ============================================================================
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                
                // Animate progress bar when info panel becomes visible
                if (entry.target.classList.contains('info-panel')) {
                    const progressBar = entry.target.querySelector('.progress-fill');
                    if (progressBar && progressBar.dataset.width) {
                        setTimeout(() => {
                            progressBar.style.width = progressBar.dataset.width + '%';
                        }, 500);
                    }
                }
            }
        });
    }, observerOptions);

    document.querySelectorAll('.reveal, .card, .stat-card, .timeline-item').forEach(el => {
        observer.observe(el);
    });
}

// ============================================================================
// NAVBAR SCROLL EFFECT
// ============================================================================
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.navbar')) {
            const dropdowns = document.querySelectorAll('.dropdown-menu.show');
            dropdowns.forEach(dropdown => {
                const bsDropdown = bootstrap.Dropdown.getInstance(dropdown.previousElementSibling);
                if (bsDropdown) bsDropdown.hide();
            });
        }
    });
}

// ============================================================================
// PROGRESS BARS ANIMATION
// ============================================================================
function initProgressBars() {
    const progressBars = document.querySelectorAll('.progress-fill');
    
    const progressObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const bar = entry.target;
                const targetWidth = bar.dataset.width || 35;
                setTimeout(() => {
                    bar.style.width = targetWidth + '%';
                }, 300);
            }
        });
    }, { threshold: 0.5 });

    progressBars.forEach(bar => progressObserver.observe(bar));
}

// ============================================================================
// STAT COUNTERS ANIMATION
// ============================================================================
function initStatCounters() {
    const statObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
                entry.target.classList.add('animated');
                setTimeout(() => {
                    animateStatCard(entry.target);
                }, Math.random() * 500);
            }
        });
    }, { threshold: 0.5 });

    document.querySelectorAll('.stat-card').forEach(card => {
        statObserver.observe(card);
    });
}

function animateStatCard(card) {
    const numberEl = card.querySelector('.stat-number');
    if (!numberEl) return;
    
    const target = parseInt(numberEl.getAttribute('data-target') || numberEl.textContent);
    const duration = 1500;
    const start = performance.now();

    function animate(current) {
        const elapsed = current - start;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function
        const easeOut = 1 - Math.pow(1 - progress, 3);
        const currentNumber = Math.floor(easeOut * target);
        
        numberEl.textContent = currentNumber;
        
        if (progress < 1) {
            requestAnimationFrame(animate);
        } else {
            numberEl.textContent = target;
        }
    }
    
    // Reset to 0 and start animation
    numberEl.textContent = '0';
    requestAnimationFrame(animate);
}

// ============================================================================
// TIMELINE HIGHLIGHT
// ============================================================================
function initTimelineHighlight() {
    const timelineItems = document.querySelectorAll('.timeline-item');
    
    timelineItems.forEach(item => {
        item.addEventListener('click', function() {
            // Remove highlight from all items
            timelineItems.forEach(el => {
                el.style.background = '';
                el.style.transform = '';
            });
            
            // Highlight clicked item
            this.querySelector('.timeline-content').style.background = 'var(--cheval-gron)';
            this.style.transform = 'translateX(20px) scale(1.02)';
            
            setTimeout(() => {
                this.style.transform = 'translateX(10px)';
            }, 200);
        });
    });
}

// ============================================================================
// METRIC CARD ANIMATIONS
// ============================================================================
window.animateMetrics = function() {
    const cards = document.querySelectorAll('.metric-card');
    cards.forEach(card => {
        card.style.transform = 'scale(1.1)';
        setTimeout(() => {
            card.style.transform = 'scale(1)';
        }, 300);
    });
};

// ============================================================================
// CONSUMPTION CARD HOVER EFFECTS
// ============================================================================
document.querySelectorAll('.consumption-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.background = 'linear-gradient(135deg, var(--light-gron), var(--cheval-gron))';
    });

    card.addEventListener('mouseleave', function() {
        this.style.background = 'var(--light-gron)';
    });
});

// ============================================================================
// SMOOTH SCROLL FOR ANCHOR LINKS
// ============================================================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href !== '#main-content') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// ============================================================================
// FORM VALIDATION ENHANCEMENT
// ============================================================================
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        const requiredFields = this.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.style.borderColor = '#e74c3c';
            } else {
                field.style.borderColor = '';
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            alert('Please fill in all required fields');
        }
    });
});

// ============================================================================
// BOOTSTRAP NAVBAR ENHANCEMENTS
// ============================================================================
function enhanceBootstrapNavbar() {
    // Auto-close mobile menu when clicking a link
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link:not(.dropdown-toggle)');
    const navbarCollapse = document.querySelector('.navbar-collapse');

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
                if (bsCollapse) bsCollapse.hide();
            }
        });
    });
}

// Initialize navbar enhancements
enhanceBootstrapNavbar();

// ============================================================================
// LOADING STATES FOR FORMS
// ============================================================================
function addLoadingState() {
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                submitBtn.disabled = true;
                const originalText = submitBtn.textContent;
                submitBtn.textContent = 'Behandler...';
                submitBtn.style.opacity = '0.7';

                // Re-enable after 5 seconds as fallback
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalText;
                    submitBtn.style.opacity = '1';
                }, 5000);
            }
        });
    });
}

// ============================================================================
// SEARCH ENHANCEMENT WITH DEBOUNCE
// ============================================================================
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function initSearchEnhancement() {
    const searchInputs = document.querySelectorAll('input[type="search"], input[name="q"]');

    searchInputs.forEach(input => {
        input.addEventListener('input', debounce(function(e) {
            const value = e.target.value;
            if (value.length >= 2) {
                // Visual feedback
                input.style.borderColor = 'var(--cheval-gron)';
                input.style.boxShadow = '0 0 0 2px rgba(160, 215, 165, 0.2)';
            } else {
                input.style.borderColor = '';
                input.style.boxShadow = '';
            }
        }, 300));
    });
}

// ============================================================================
// COPY TO CLIPBOARD FUNCTIONALITY
// ============================================================================
function initCopyButtons() {
    document.querySelectorAll('[data-copy]').forEach(button => {
        button.addEventListener('click', async function() {
            const textToCopy = this.getAttribute('data-copy');
            try {
                await navigator.clipboard.writeText(textToCopy);
                const originalText = this.textContent;
                this.textContent = '✓ Kopieret!';
                this.style.background = 'var(--cheval-gron)';

                setTimeout(() => {
                    this.textContent = originalText;
                    this.style.background = '';
                }, 2000);
            } catch (err) {
                console.error('Failed to copy:', err);
            }
        });
    });
}

// ============================================================================
// LAZY LOAD IMAGES
// ============================================================================
function initLazyLoad() {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.classList.add('loaded');
                    observer.unobserve(img);
                }
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// ============================================================================
// KEYBOARD NAVIGATION ENHANCEMENT
// ============================================================================
function initKeyboardNav() {
    // Focus trap for modal-like elements
    document.addEventListener('keydown', (e) => {
        // Tab navigation hints
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-nav-active');
        }
    });

    document.addEventListener('mousedown', () => {
        document.body.classList.remove('keyboard-nav-active');
    });
}

// ============================================================================
// ANIMATE ON SCROLL (Enhanced)
// ============================================================================
function initEnhancedScrollAnimations() {
    const elements = document.querySelectorAll('.kpi-card, .card, .section-block');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 100);
            }
        });
    }, { threshold: 0.1 });

    elements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// ============================================================================
// TOOLTIP SYSTEM
// ============================================================================
function initTooltips() {
    document.querySelectorAll('[data-tooltip]').forEach(element => {
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = element.getAttribute('data-tooltip');
        tooltip.style.cssText = `
            position: absolute;
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 0.85rem;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s ease;
            z-index: 10000;
            white-space: nowrap;
        `;
        document.body.appendChild(tooltip);

        element.addEventListener('mouseenter', (e) => {
            const rect = element.getBoundingClientRect();
            tooltip.style.left = rect.left + rect.width / 2 - tooltip.offsetWidth / 2 + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + window.scrollY + 'px';
            tooltip.style.opacity = '1';
        });

        element.addEventListener('mouseleave', () => {
            tooltip.style.opacity = '0';
        });
    });
}

// ============================================================================
// AWW-CARDS PREMIUM ANIMATION
// ============================================================================
function initAwwCardsAnimation() {
    const cards = document.querySelectorAll('.aww-card, .image-overlay-card');

    const cardObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 100); // Stagger animation
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    });

    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s cubic-bezier(0.4, 0, 0.2, 1), transform 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
        cardObserver.observe(card);
    });

    // Add 3D tilt effect on mouse move (premium Awwwards-style)
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
        });
    });
}

// ============================================================================
// SUBTLE PARALLAX EFFECT FOR HERO SECTIONS
// ============================================================================
function initParallaxEffect() {
    const heroSections = document.querySelectorAll('.hero-video-container, .section-landing');

    window.addEventListener('scroll', () => {
        heroSections.forEach(section => {
            const scrolled = window.pageYOffset;
            const rate = scrolled * 0.5;
            section.style.transform = `translate3d(0, ${rate}px, 0)`;
        });
    });
}

// ============================================================================
// PREMIUM BUTTON RIPPLE EFFECT
// ============================================================================
document.querySelectorAll('.cta-button, .filter-pill, .btn').forEach(button => {
    button.addEventListener('click', function(e) {
        const rect = this.getBoundingClientRect();
        const ripple = document.createElement('span');
        ripple.className = 'ripple';
        ripple.style.left = (e.clientX - rect.left) + 'px';
        ripple.style.top = (e.clientY - rect.top) + 'px';

        this.appendChild(ripple);

        setTimeout(() => ripple.remove(), 600);
    });
});

// Add ripple styles dynamically
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        width: 20px;
        height: 20px;
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }

    @keyframes ripple-animation {
        to {
            transform: scale(20);
            opacity: 0;
        }
    }

    .cta-button, .filter-pill, .btn {
        position: relative;
        overflow: hidden;
    }
`;
document.head.appendChild(rippleStyle);

console.log('✓ Vidensbank JavaScript loaded successfully with premium animations!');
