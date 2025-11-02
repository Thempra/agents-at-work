# Style Guide for the Task Management Application

## Introduction

This style guide provides a comprehensive set of guidelines for designing and implementing the user interface (UI) and user experience (UX) elements of the task management application. The goal is to ensure a consistent, intuitive, and visually appealing user interface that enhances productivity and usability.

## Color Scheme

### Palette
- **Primary Blue:** #1E90FF
  - Used for primary actions, such as creating tasks or updating their status.
- **Secondary Gray:** #808080
  - Used for background elements, minor text, and inactive states.
- **Accent Green:** #32CD32
  - Used for positive notifications and completed tasks.
- **Error Red:** #FF0000
  - Used for error messages and critical alerts.

### Usage Guidelines
- **Primary Blue:** Emphasize key actions and call-to-action elements.
- **Secondary Gray:** Use as a neutral background color or for minor text to avoid visual clutter.
- **Accent Green:** Indicate success, completion, or positive outcomes.
- **Error Red:** Highlight errors, issues, or critical notifications.

## Typography

### Fonts
- **Primary Font:** Open Sans (Sans-serif)
  - Used throughout the application for headings and body text.
- **Secondary Font:** Roboto (Sans-serif)
  - Used for smaller text elements, such as captions or footnotes.

### Sizes
- **Headings:**
  - H1: 36px
  - H2: 28px
  - H3: 24px
  - H4: 20px
  - H5: 18px
  - H6: 16px
- **Body Text:** 16px

### Usage Guidelines
- **Headings:** Use headings to organize content and guide users through the application.
- **Body Text:** Use body text for main content, descriptions, and instructions.

## Component Styles

### Buttons
- **Primary Button:**
  - Background Color: Primary Blue
  - Border: None
  - Text Color: White
  - Padding: 10px 20px
  - Font Size: 16px
- **Secondary Button:**
  - Background Color: Transparent
  - Border: 1px solid Secondary Gray
  - Text Color: Secondary Gray
  - Padding: 5px 10px
  - Font Size: 14px

### Inputs
- **Text Input:**
  - Background Color: White
  - Border: 1px solid Secondary Gray
  - Text Color: Black
  - Padding: 8px 12px
  - Font Size: 16px
- **Textarea:**
  - Same as text input but with a larger height.

### Cards
- **Card Background:** White
- **Card Border:** 1px solid Secondary Gray
- **Padding:** 15px

### Alerts
- **Success Alert:**
  - Background Color: Accent Green
  - Text Color: White
  - Padding: 10px
- **Error Alert:**
  - Background Color: Error Red
  - Text Color: White
  - Padding: 10px

## Layout and Spacing

### Grid System
- Use a responsive grid system to ensure consistent spacing and alignment across different devices.

### Margins and Paddings
- **Margin:** Use margins to create space between elements.
- **Padding:** Use padding within elements to separate content from the edges.

## Accessibility

### Color Contrast
- Ensure sufficient color contrast for readability. The WCAG 2.1 guidelines recommend a minimum contrast ratio of 4.5:1 for normal text and 3:1 for larger text.

### Keyboard Navigation
- Ensure that all interactive elements can be accessed using keyboard navigation.

### Screen Reader Compatibility
- Use semantic HTML and ARIA attributes to improve accessibility for screen readers.

## Responsive Design

### Breakpoints
- Define breakpoints for different device sizes:
  - Mobile (small): <600px
  - Tablet (medium): >=601px and <900px
  - Desktop (large): >=901px

### Media Queries
- Use media queries to apply styles specific to each breakpoint.

## Conclusion

By following these style guidelines, we can create a cohesive and user-friendly interface that enhances the overall experience of using our task management application. Consistency in design elements will help users quickly navigate and interact with the application, improving productivity and satisfaction.