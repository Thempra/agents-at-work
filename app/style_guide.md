# Style Guide for the Task Management App

## Overview

This style guide provides a comprehensive set of guidelines to ensure consistency and quality in the user interface (UI) and user experience (UX) of the task management app. The guidelines are designed to improve usability, readability, and overall aesthetic appeal.

## Color Scheme

### Palette
- **Primary Blue**: #007BFF - Used for primary actions, navigation, and accents.
- **Secondary Gray**: #6C757D - Used for background elements, dividers, and less important text.
- **Success Green**: #28A745 - Used to indicate successful actions or positive outcomes.
- **Error Red**: #DC3545 - Used to indicate errors or negative outcomes.

### Usage
- **Primary Blue**: Emphasize primary actions such as "Create Task," "Delete Task," and navigation links.
- **Secondary Gray**: Use for background colors, dividers, and less important text elements to maintain a clean layout.
- **Success Green**: Highlight successful actions like marking a task as completed.
- **Error Red**: Indicate errors or negative outcomes, such as failed task creation.

## Typography

### Fonts
- **Primary Font**: Open Sans - A versatile sans-serif font that is easy to read on screens and in print.
- **Secondary Font**: Roboto - Used for headings and titles to add a touch of modernity and professionalism.

### Sizes
- **Heading 1 (H1)**: 2.5rem, Roboto Bold
- **Heading 2 (H2)**: 2rem, Open Sans SemiBold
- **Heading 3 (H3)**: 1.75rem, Open Sans SemiBold
- **Body Text**: 1.25rem, Open Sans Regular

### Usage
- **Heading 1**: Use for the main title of the app or large sections.
- **Heading 2 and Heading 3**: Use for section headers and subheadings.
- **Body Text**: Use for all regular text content, including descriptions and labels.

## Component Styles

### Buttons

#### Primary Button
- **Background Color**: Primary Blue (#007BFF)
- **Text Color**: White
- **Border**: None
- **Hover State**: Lighter shade of primary blue (#0056b3)

#### Secondary Button
- **Background Color**: Transparent
- **Text Color**: Primary Blue (#007BFF)
- **Border**: 1px solid Primary Blue
- **Hover State**: Darker shade of primary blue (#004085)

### Input Fields

#### Text Input
- **Background Color**: White
- **Border**: 1px solid Secondary Gray (#6C757D)
- **Text Color**: Black
- **Placeholder Color**: Secondary Gray (#6C757D)

#### Submit Button
- **Background Color**: Primary Blue (#007BFF)
- **Text Color**: White
- **Border**: None
- **Hover State**: Lighter shade of primary blue (#0056b3)

### Cards

#### Task Card
- **Background Color**: White
- **Border**: 1px solid Secondary Gray (#6C757D)
- **Padding**: 1rem
- **Radius**: 8px

### Navigation

#### Sidebar
- **Background Color**: Primary Blue (#007BFF)
- **Text Color**: White
- **Hover State**: Lighter shade of primary blue (#0056b3)

## Layout

### General Guidelines
- **Grid System**: Use a grid system for consistent spacing and alignment.
- **Responsive Design**: Ensure the app is responsive and adapts to different screen sizes.
- **Consistent Spacing**: Use consistent padding, margin, and spacing between elements.

## Navigation

### Sidebar
- The sidebar should be fixed on the left side of the screen.
- It should contain links to major sections of the app such as "Tasks," "Settings," and "Profile."
- The active link should have a different background color or text color to indicate the current section.

### Header
- The header should be located at the top of the screen.
- It should contain the app name, user profile picture, and navigation links.
- Use a dark mode for better visibility on light backgrounds.

## Forms

### Task Form
- The task form should include fields for task name, description, status, and due date.
- Use labels above each field for clarity.
- Provide validation feedback to help users complete the form correctly.

## Error Handling

### Error Messages
- Display error messages prominently at the top of the screen or in a modal dialog.
- Use the error red color (#DC3545) for error messages.
- Provide actionable steps to