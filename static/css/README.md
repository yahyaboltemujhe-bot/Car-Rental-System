# Car Rental System - CSS Documentation

## Overview
This Car Rental System uses a **modern, modular CSS architecture** with a consistent design system built on CSS custom properties (CSS variables). The styling is professional, responsive, and optimized for maintainability.

## File Structure

```
static/css/
├── main.css                    # Main stylesheet with variables and common components
├── auth/
│   └── login.css              # Login page specific styles
└── admin/
    ├── dashboard.css          # Dashboard overview styles
    ├── add_car.css            # Add vehicle form styles
    ├── manage_fleet.css       # Fleet management table styles
    ├── tracking.css           # Vehicle tracking styles (or use tracking_complete.css)
    ├── tracking_complete.css  # Complete tracking styles
    ├── damage_claims.css      # Claims management styles (or use damage_claims_complete.css)
    └── damage_claims_complete.css  # Complete claims styles
```

## Design System

### Color Palette
- **Primary**: Soft blue (#5a7fff) - Main action color
- **Success**: Green (#28a745) - Positive actions, available status
- **Warning**: Yellow (#ffc107) - Caution, pending status
- **Danger**: Red (#dc3545) - Errors, out-of-range alerts
- **Info**: Cyan (#17a2b8) - Information, tracking data
- **Neutrals**: Gray scale (#f8f9fa to #212529)

### Typography
- **Font Family**: Segoe UI, Tahoma, Geneva, Verdana, sans-serif
- **Font Sizes**: Uses responsive scale (xs: 12px → 3xl: 32px)
- **Font Weights**: 400 (normal), 500 (medium), 600 (semibold), 700 (bold)

### Spacing
- Uses a consistent spacing scale: xs (4px), sm (8px), md (16px), lg (24px), xl (32px), 2xl (48px)
- Access via CSS variables: `var(--spacing-md)`

### Shadows
- **sm**: Subtle elevation
- **md**: Standard card shadow
- **lg**: Prominent cards
- **xl**: Modals and overlays

## CSS Variables

All design tokens are defined as CSS custom properties in `main.css`:

```css
:root {
    --color-primary: #5a7fff;
    --color-success: #28a745;
    --spacing-md: 1rem;
    --border-radius: 8px;
    --shadow: 0 4px 6px rgba(0, 0, 0, 0.08);
    --transition-base: 250ms ease-in-out;
    /* ... and many more */
}
```

## Component Classes

### Buttons
```css
.btn                 /* Base button */
.btn-primary         /* Primary action */
.btn-secondary       /* Secondary action */
.btn-success         /* Success action */
.btn-danger          /* Destructive action */
.btn-sm              /* Small button */
.btn-lg              /* Large button */
```

### Forms
```css
.form-group          /* Form field wrapper */
.form-label          /* Field label */
.form-control        /* Input, textarea */
.form-select         /* Select dropdown */
.input-group         /* Input with icon/prefix */
.is-valid            /* Valid state */
.is-invalid          /* Invalid state */
```

### Cards
```css
.card                /* Base card */
.card-header         /* Card header */
.card-body           /* Card content */
.card-footer         /* Card footer */
.stat-card           /* Dashboard statistics card */
```

### Tables
```css
.table               /* Base table */
.table-container     /* Table wrapper with styling */
.table-responsive    /* Horizontal scroll on mobile */
```

### Badges
```css
.badge               /* Base badge */
.badge-primary       /* Primary badge */
.badge-success       /* Success badge */
.status-badge        /* Status indicator badge */
```

### Alerts
```css
.alert               /* Base alert */
.alert-success       /* Success message */
.alert-danger        /* Error message */
.alert-warning       /* Warning message */
.alert-info          /* Info message */
```

## How to Use

### 1. Include Main Stylesheet
All pages should include `main.css` first:
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
```

### 2. Add Page-Specific Styles
Then include the page-specific stylesheet:
```html
<!-- For login page -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/auth/login.css') }}">

<!-- For dashboard -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/admin/dashboard.css') }}">
```

### 3. Use Utility Classes
```html
<div class="mt-3 mb-4">      <!-- Margin top 3, bottom 4 -->
<p class="text-primary">      <!-- Primary color text -->
<div class="d-flex gap-2">   <!-- Flexbox with gap -->
```

## Page-Specific Features

### Login Page (login.css)
- Centered layout with gradient background
- Animated card entrance
- Form validation styling
- Mobile responsive

### Dashboard (dashboard.css)
- Fixed sidebar navigation
- Statistics cards grid
- Hover effects
- Pattern badges

### Add Car (add_car.css)
- Clean form layout
- Category selection
- Input validation
- Pattern explanation section

### Fleet Management (manage_fleet.css)
- Filter bar
- Data table with sorting
- Status badges
- Action buttons
- State pattern visualization

### Tracking (tracking_complete.css)
- Alert cards with pulse animation
- Location badges
- Distance indicators
- Observer pattern info

### Damage Claims (damage_claims_complete.css)
- Claims statistics
- Modal form
- Chain of Responsibility visualization
- Approval/rejection buttons

## Responsive Breakpoints

```css
/* Tablet */
@media (max-width: 992px) { ... }

/* Mobile landscape */
@media (max-width: 768px) { ... }

/* Mobile portrait */
@media (max-width: 576px) { ... }
```

## Animations

All animations are defined in `main.css`:
- `fadeIn` - Fade in content
- `fadeInUp` - Fade in with upward movement
- `slideInDown` - Slide down alerts
- `pulse` - Pulsing effect for alerts
- `spin` - Loading spinner rotation

## Accessibility Features

- `:focus` states on all interactive elements
- High contrast mode support
- Reduced motion support
- Semantic color usage
- Keyboard navigation friendly

## Customization

To customize the design system:

1. **Colors**: Edit color variables in `:root` in `main.css`
2. **Spacing**: Adjust spacing scale variables
3. **Typography**: Change font family and size scale
4. **Shadows**: Modify shadow variables
5. **Animations**: Adjust transition and animation durations

## Browser Support

- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- IE11: ⚠️ No CSS variable support (requires fallbacks)

## Best Practices

1. **Always use CSS variables** for colors, spacing, and shadows
2. **Use semantic class names** (`.btn-primary` not `.btn-blue`)
3. **Mobile-first approach** - Base styles for mobile, enhance for desktop
4. **Avoid inline styles** - Use classes instead
5. **Group related styles** - Keep page-specific styles in their own files
6. **Comment your code** - Explain complex selectors or hacks

## Performance Tips

- CSS files are small and load quickly
- Use `main.css` for shared styles to avoid duplication
- Combine related selectors
- Avoid deep nesting (max 3 levels)
- Use efficient selectors (class over tag)

## Future Enhancements

- [ ] Dark mode support (use `@media (prefers-color-scheme: dark)`)
- [ ] CSS Grid fallbacks for older browsers
- [ ] Print stylesheet
- [ ] RTL (Right-to-Left) language support
- [ ] Component library documentation

## Questions?

For more information or to report issues, check the project documentation or open an issue in the repository.
