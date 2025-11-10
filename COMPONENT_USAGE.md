# Component Usage Guide

Quick reference for using the migrated visual components in your Flask templates.

## Basic Page Structure

```html
{% extends 'base.html' %}

{% block title %}Your Page Title - Vidensbank{% endblock %}

{% block content %}
<div class="section">
    <div class="container">
        <h1 class="main-title">Your Page Title</h1>
        <div class="wavy-underline"></div>
        
        <!-- Your content here -->
    </div>
</div>
{% endblock %}
```

## Grid Layouts

### 2-Column Grid
```html
<div class="grid-2-col">
    <div class="card">Content 1</div>
    <div class="card">Content 2</div>
</div>
```

### 3-Column Grid
```html
<div class="grid-3-col">
    <div class="card">Item 1</div>
    <div class="card">Item 2</div>
    <div class="card">Item 3</div>
</div>
```

### 4-Column Auto-fit Grid
```html
<div class="grid-4-col">
    <div class="stat-card">
        <div class="stat-number" data-target="95">0</div>
        <div class="stat-label">Percentage</div>
    </div>
    <!-- More cards -->
</div>
```

## Card Components

### Standard Card
```html
<div class="card">
    <h3 class="card-title">Card Title</h3>
    <p>Card content goes here...</p>
</div>
```

### Card with Background Color
```html
<div class="card bg-light-green">
    <h3>Green Background Card</h3>
    <p>Content...</p>
</div>

<div class="card bg-light-yellow">
    <h3>Yellow Background Card</h3>
    <p>Content...</p>
</div>
```

### KPI Card
```html
<div class="kpi-card">
    <div class="kpi-label">Total Users</div>
    <div class="kpi-number">1,234</div>
    <p>Active users this month</p>
</div>
```

### Metric Card (with Header)
```html
<div class="metric-card">
    <div class="metric-header">Current Status</div>
    <div class="metric-value green">350</div>
    <div class="metric-description">
        Units processed today
    </div>
</div>
```

### Stat Card (with Counter Animation)
```html
<div class="stat-card">
    <div class="stat-number" data-target="271">0</div>
    <div class="stat-label">Total Projects<br><small>Completed this year</small></div>
</div>
```

### Consumption Card (Special with Icon)
```html
<div class="consumption-card">
    <div class="card-title">
        <div class="icon">🌱</div>
        Card Title with Icon
    </div>
    <p>Content goes here...</p>
</div>
```

## Info Panel (Sticky Sidebar)

```html
<div class="grid-2-col">
    <div class="main-content">
        <!-- Main content here -->
    </div>
    
    <div class="info-panel">
        <div class="info-title">
            <span>📊</span>
            Key Facts
        </div>
        <p>Important information...</p>
        
        <div class="progress-bar">
            <div class="progress-fill" data-width="35"></div>
        </div>
        <small>Progress: 35%</small>
    </div>
</div>
```

## Quote Section

```html
<div class="quote-section">
    <div class="quote-text">
        "This is an inspiring quote about sustainability and innovation."
    </div>
    <div class="quote-author">- Your Name, Title</div>
</div>
```

## Timeline

```html
<div class="timeline">
    <div class="timeline-title">Project Milestones</div>
    
    <div class="timeline-item">
        <div class="timeline-year">2021</div>
        <div class="timeline-content">
            <div class="timeline-event">Event Title</div>
            <div class="timeline-description">Event description...</div>
        </div>
    </div>
    
    <div class="timeline-item">
        <div class="timeline-year">2023</div>
        <div class="timeline-content">
            <div class="timeline-event">Another Event</div>
            <div class="timeline-description">Description...</div>
        </div>
    </div>
</div>
```

## Progress Bar

```html
<div class="progress-bar">
    <div class="progress-fill" data-width="65"></div>
</div>
<small>Progress: 65% complete</small>
```

## Section with Background

```html
<div class="section bg-light">
    <div class="container">
        <h2 class="section-title">Section Title</h2>
        <div class="wavy-underline"></div>
        <!-- Content -->
    </div>
</div>
```

## Hero/Landing Section

```html
<div class="section-landing" style="background-image: url('{{ url_for('static', filename='images/hero.jpg') }}');">
    <div class="container">
        <h1 class="section-landing-heading">Welcome</h1>
        <p class="section-landing-sub-heading">Your tagline here</p>
        <a href="#" class="cta-button primary">Get Started</a>
    </div>
</div>
```

## CTA Block

```html
<div class="cta-block">
    <h2>Ready to Get Started?</h2>
    <p>Join us in making a difference for the environment</p>
    <a href="{{ url_for('contact') }}" class="cta-button secondary">Contact Us</a>
</div>
```

## Buttons

```html
<!-- Primary Button -->
<a href="#" class="cta-button primary">Primary Action</a>

<!-- Secondary Button -->
<a href="#" class="cta-button secondary">Secondary Action</a>
```

## Comparison Grid (Metrics Side by Side)

```html
<div class="comparison-grid">
    <div class="metric-card">
        <div class="metric-header">Target</div>
        <div class="metric-value green">350</div>
        <div class="metric-description">Goal amount</div>
    </div>
    
    <div class="metric-card">
        <div class="metric-header">Current</div>
        <div class="metric-value red">950</div>
        <div class="metric-description">Current amount</div>
    </div>
</div>
```

## Floating Decorative Elements

```html
<div class="floating-elements">
    <div class="floating-element"></div>
    <div class="floating-element"></div>
    <div class="floating-element"></div>
</div>
```

## Scroll-Triggered Animations

Add the `reveal` class to any element to make it fade in on scroll:

```html
<div class="card reveal">
    <!-- This will fade in when scrolled into view -->
</div>
```

## Color Classes

Use these for backgrounds:
- `.bg-light` - Light gray background
- `.bg-light-green` - Light green background
- `.bg-light-yellow` - Light yellow background
- `.bg-cheval-taube` - Taupe/beige background

## Typography Classes

- `.main-title` - Large uppercase display heading
- `.section-title` - Section heading
- `.card-title` - Card heading with icon support
- `.subtitle` - Smaller subtitle text
- `.caption` - Small caption/helper text

## Form Styling

Forms automatically get styled. Use standard HTML:

```html
<div class="form-group">
    <label for="name">Name</label>
    <input type="text" id="name" name="name" required>
</div>

<div class="form-group">
    <label for="message">Message</label>
    <textarea id="message" name="message" required></textarea>
</div>

<button type="submit" class="cta-button primary">Submit</button>
```

## Tips

1. **Animations**: Stat cards automatically count up when scrolled into view
2. **Progress bars**: Set `data-width="XX"` attribute for target percentage
3. **Sticky panels**: Info panels stick to the top when scrolling
4. **Responsive**: All components automatically adapt to mobile
5. **Icons**: Use emoji or icon fonts in `.icon` divs

## Example Full Page

```html
{% extends 'base.html' %}

{% block title %}Example Page - Vidensbank{% endblock %}

{% block content %}
<!-- Hero Section -->
<div class="section-landing" style="background-image: url('{{ url_for('static', filename='images/hero.jpg') }}');">
    <div class="container">
        <h1 class="section-landing-heading">Page Title</h1>
        <p class="section-landing-sub-heading">Subtitle goes here</p>
    </div>
</div>

<!-- Main Content -->
<div class="section">
    <div class="container">
        <h2 class="section-title">Main Section</h2>
        <div class="wavy-underline"></div>
        
        <div class="grid-3-col">
            <div class="card reveal">
                <h3>Feature 1</h3>
                <p>Description...</p>
            </div>
            <div class="card reveal">
                <h3>Feature 2</h3>
                <p>Description...</p>
            </div>
            <div class="card reveal">
                <h3>Feature 3</h3>
                <p>Description...</p>
            </div>
        </div>
    </div>
</div>

<!-- Stats Section -->
<div class="section bg-light">
    <div class="container">
        <h2 class="section-title">Our Impact</h2>
        <div class="grid-4-col">
            <div class="stat-card">
                <div class="stat-number" data-target="1500">0</div>
                <div class="stat-label">Metric 1</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" data-target="95">0</div>
                <div class="stat-label">Metric 2</div>
            </div>
            <!-- More stats -->
        </div>
    </div>
</div>

<!-- CTA Section -->
<div class="section">
    <div class="container">
        <div class="cta-block">
            <h2>Take Action Today</h2>
            <p>Join us in our mission</p>
            <a href="{{ url_for('contact') }}" class="cta-button secondary">Get in Touch</a>
        </div>
    </div>
</div>
{% endblock %}
```

---

## Need Help?

All components are fully documented in the CSS with comments. Check `static/css/style.css` for detailed styling options and customization.
