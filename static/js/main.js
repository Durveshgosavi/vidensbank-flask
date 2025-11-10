// ============================================================================
// VIDENSBANK - Main JavaScript
// Enhanced with Power Pages interactions
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    initFlashMessages();
    initScrollAnimations();
    initHeaderScroll();
    initProgressBars();
    initStatCounters();
    initTimelineHighlight();
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
// HEADER SCROLL EFFECT
// ============================================================================
function initHeaderScroll() {
    const header = document.querySelector('.premium-header');
    if (!header) return;

    let lastScroll = 0;
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        
        lastScroll = currentScroll;
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
// MOBILE MENU TOGGLE
// ============================================================================
function initMobileMenu() {
    const toggleButton = document.querySelector('.navbar-toggler');
    const navMenu = document.querySelector('.navbar-nav');
    
    if (toggleButton && navMenu) {
        toggleButton.addEventListener('click', function() {
            navMenu.classList.toggle('show');
            this.classList.toggle('active');
        });
    }
}

// Initialize mobile menu
initMobileMenu();

console.log('Vidensbank JavaScript initialized successfully!');
