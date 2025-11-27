/**
 * Vidensbank - Data Visualization & Chart Components
 * Modern, interactive chart library using Chart.js and custom animations
 */

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    initializeCounters();
    initializeProgressBars();
    initializeScrollAnimations();
});

/**
 * Initialize all chart components on the page
 */
function initializeCharts() {
    // CO2 Emissions Bar Chart
    const emissionsChart = document.getElementById('emissionsChart');
    if (emissionsChart) {
        createEmissionsChart(emissionsChart);
    }

    // Food Category Comparison Chart
    const comparisonChart = document.getElementById('comparisonChart');
    if (comparisonChart) {
        createComparisonChart(comparisonChart);
    }

    // Environmental Impact Radar Chart
    const radarChart = document.getElementById('radarChart');
    if (radarChart) {
        createRadarChart(radarChart);
    }

    // Trend Line Chart
    const trendChart = document.getElementById('trendChart');
    if (trendChart) {
        createTrendChart(trendChart);
    }
}

/**
 * Create CO2 Emissions Bar Chart
 */
function createEmissionsChart(canvas) {
    const ctx = canvas.getContext('2d');

    const data = {
        labels: ['Oksekød', 'Lam', 'Svinekød', 'Kylling', 'Fisk', 'Mejeriprodukter', 'Grøntsager', 'Bælgfrugter'],
        datasets: [{
            label: 'CO₂e pr. kg (kg)',
            // Source: Our World in Data, Poore & Nemecek (2018) Science
            data: [60, 24, 12, 6.9, 6, 21, 2, 2],
            backgroundColor: [
                'rgba(231, 76, 60, 0.8)',
                'rgba(192, 57, 43, 0.8)',
                'rgba(230, 126, 34, 0.8)',
                'rgba(241, 196, 15, 0.8)',
                'rgba(52, 152, 219, 0.8)',
                'rgba(46, 204, 113, 0.8)',
                'rgba(26, 188, 156, 0.8)',
                'rgba(160, 215, 165, 0.8)'
            ],
            borderColor: [
                'rgba(231, 76, 60, 1)',
                'rgba(192, 57, 43, 1)',
                'rgba(230, 126, 34, 1)',
                'rgba(241, 196, 15, 1)',
                'rgba(52, 152, 219, 1)',
                'rgba(46, 204, 113, 1)',
                'rgba(26, 188, 156, 1)',
                'rgba(160, 215, 165, 1)'
            ],
            borderWidth: 2,
            borderRadius: 8,
            borderSkipped: false,
        }]
    };

    const config = {
        type: 'bar',
        data: data,
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 1500,
                easing: 'easeInOutQuart'
            },
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'CO₂-udslip pr. fødevarekategori',
                    font: {
                        size: 18,
                        weight: 'bold',
                        family: "'Theinhardt', 'Roboto', sans-serif"
                    },
                    padding: 20
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    cornerRadius: 8,
                    displayColors: false,
                    callbacks: {
                        label: function(context) {
                            return context.parsed.x + ' kg CO₂e pr. kg produkt';
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    grid: {
                        display: true,
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        callback: function(value) {
                            return value + ' kg';
                        },
                        font: {
                            size: 12
                        }
                    }
                },
                y: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 13,
                            weight: '500'
                        }
                    }
                }
            }
        }
    };

    new Chart(ctx, config);
}

/**
 * Create Food Category Comparison Chart
 */
function createComparisonChart(canvas) {
    const ctx = canvas.getContext('2d');

    const data = {
        labels: ['Januar', 'Februar', 'Marts', 'April', 'Maj', 'Juni'],
        datasets: [
            {
                label: 'Kød-baseret',
                data: [65, 59, 55, 50, 45, 42],
                backgroundColor: 'rgba(231, 76, 60, 0.2)',
                borderColor: 'rgba(231, 76, 60, 1)',
                borderWidth: 3,
                tension: 0.4,
                fill: true
            },
            {
                label: 'Plantebaseret',
                data: [28, 32, 35, 38, 42, 45],
                backgroundColor: 'rgba(160, 215, 165, 0.2)',
                borderColor: 'rgba(160, 215, 165, 1)',
                borderWidth: 3,
                tension: 0.4,
                fill: true
            }
        ]
    };

    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            animation: {
                duration: 2000,
                easing: 'easeInOutQuart'
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        font: {
                            size: 13,
                            weight: '600'
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Udvikling i måltidsvælg i kantinen (%)',
                    font: {
                        size: 18,
                        weight: 'bold'
                    },
                    padding: 20
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y + '%';
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    };

    new Chart(ctx, config);
}

/**
 * Create Environmental Impact Radar Chart
 */
function createRadarChart(canvas) {
    const ctx = canvas.getContext('2d');

    const data = {
        labels: ['CO₂-udslip', 'Vandforbrug', 'Landanvendelse', 'Biodiversitet', 'Energiforbrug'],
        datasets: [
            {
                label: 'Konventionel',
                data: [85, 75, 80, 30, 70],
                backgroundColor: 'rgba(231, 76, 60, 0.2)',
                borderColor: 'rgba(231, 76, 60, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(231, 76, 60, 1)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgba(231, 76, 60, 1)'
            },
            {
                label: 'Bæredygtig',
                data: [30, 40, 35, 85, 35],
                backgroundColor: 'rgba(160, 215, 165, 0.2)',
                borderColor: 'rgba(160, 215, 165, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(160, 215, 165, 1)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgba(160, 215, 165, 1)'
            }
        ]
    };

    const config = {
        type: 'radar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 1800,
                easing: 'easeInOutQuart'
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        font: {
                            size: 13,
                            weight: '600'
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Miljøpåvirkning: Sammenligning',
                    font: {
                        size: 18,
                        weight: 'bold'
                    },
                    padding: 20
                }
            },
            scales: {
                r: {
                    angleLines: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    },
                    pointLabels: {
                        font: {
                            size: 12,
                            weight: '600'
                        }
                    },
                    ticks: {
                        beginAtZero: true,
                        max: 100,
                        stepSize: 20,
                        backdropColor: 'transparent'
                    }
                }
            }
        }
    };

    new Chart(ctx, config);
}

/**
 * Create Trend Line Chart
 */
function createTrendChart(canvas) {
    const ctx = canvas.getContext('2d');

    const data = {
        labels: ['2019', '2020', '2021', '2022', '2023', '2024', '2025'],
        datasets: [{
            label: 'Økologi-andel i kantinen (%)',
            data: [18, 25, 32, 38, 45, 52, 60],
            backgroundColor: (context) => {
                const ctx = context.chart.ctx;
                const gradient = ctx.createLinearGradient(0, 0, 0, 300);
                gradient.addColorStop(0, 'rgba(160, 215, 165, 0.5)');
                gradient.addColorStop(1, 'rgba(160, 215, 165, 0.0)');
                return gradient;
            },
            borderColor: 'rgba(160, 215, 165, 1)',
            borderWidth: 3,
            tension: 0.4,
            fill: true,
            pointRadius: 6,
            pointHoverRadius: 8,
            pointBackgroundColor: '#fff',
            pointBorderColor: 'rgba(160, 215, 165, 1)',
            pointBorderWidth: 3
        }]
    };

    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 2000,
                easing: 'easeInOutQuart'
            },
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Udvikling i økologi-andel over tid',
                    font: {
                        size: 18,
                        weight: 'bold'
                    },
                    padding: 20
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            return 'Økologi: ' + context.parsed.y + '%';
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        },
                        font: {
                            size: 12
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 12,
                            weight: '500'
                        }
                    }
                }
            }
        }
    };

    new Chart(ctx, config);
}

/**
 * Initialize animated counters
 */
function initializeCounters() {
    const counters = document.querySelectorAll('[data-counter]');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
                animateCounter(entry.target);
                entry.target.classList.add('counted');
            }
        });
    }, {
        threshold: 0.5
    });

    counters.forEach(counter => observer.observe(counter));
}

/**
 * Animate a counter element
 */
function animateCounter(element) {
    const target = parseFloat(element.getAttribute('data-counter'));
    const duration = 2000; // 2 seconds
    const steps = 60;
    const increment = target / steps;
    let current = 0;
    const suffix = element.getAttribute('data-suffix') || '';
    const prefix = element.getAttribute('data-prefix') || '';

    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }

        let displayValue = Math.round(current);
        if (target % 1 !== 0) {
            displayValue = current.toFixed(1);
        }

        element.textContent = prefix + displayValue + suffix;
    }, duration / steps);
}

/**
 * Initialize progress bars
 */
function initializeProgressBars() {
    const progressBars = document.querySelectorAll('[data-progress]');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
                const target = entry.target.getAttribute('data-progress');
                entry.target.style.width = target + '%';
                entry.target.classList.add('animated');
            }
        });
    }, {
        threshold: 0.5
    });

    progressBars.forEach(bar => observer.observe(bar));
}

/**
 * Initialize scroll-triggered animations
 */
function initializeScrollAnimations() {
    const elements = document.querySelectorAll('.animate-on-scroll');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    elements.forEach(element => observer.observe(element));
}

/**
 * Create a doughnut chart for percentages
 */
function createDoughnutChart(canvas, value, label, color) {
    const ctx = canvas.getContext('2d');

    const data = {
        labels: [label, 'Resterende'],
        datasets: [{
            data: [value, 100 - value],
            backgroundColor: [
                color,
                'rgba(200, 200, 200, 0.2)'
            ],
            borderWidth: 0
        }]
    };

    const config = {
        type: 'doughnut',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '75%',
            animation: {
                animateRotate: true,
                animateScale: true,
                duration: 1500,
                easing: 'easeInOutQuart'
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            }
        }
    };

    new Chart(ctx, config);
}

// Export functions for use in other scripts
window.VidenbankCharts = {
    createEmissionsChart,
    createComparisonChart,
    createRadarChart,
    createTrendChart,
    createDoughnutChart
};
