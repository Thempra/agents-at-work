# Style Guide for Project App

## Introduction
This document outlines the design principles, style guidelines, and components to be used in our project application (App). Adhering to these guidelines will ensure a cohesive, user-friendly, and consistent experience across all parts of the application.

## Color Scheme
The primary color palette should provide a balance between professionalism and approachability. The following colors have been selected:

- **Primary:** #007BFF (Blue) - This is used for primary actions, links, and call-to-action buttons.
- **Secondary:** #6C757D (Gray) - Used for less important text, borders, and background elements.
- **Success:** #28A745 (Green) - Indicates a successful action or completion.
- **Danger:** #DC3545 (Red) - Used for warning or error messages.
- **Warning:** #FFC107 (Yellow) - Indicating caution or important information.

## Typography
We will use Google Fonts to ensure consistency and readability across all platforms. The primary font is "Roboto", a versatile, sans-serif font suitable for both body text and headings.

### Headings
Headings should be used hierarchically from H1 to H6. For example:
- **H1:** Main title of the page (e.g., "Project Dashboard")
- **H2:** Subsection titles (e.g., "Overview", "Tasks")
- **H3:** Smaller subsections or groups within a section
- **H4:** Subheadings within smaller sections

### Body Text
Body text should be in Roboto with a font size of 16px. Paragraphs should have a line height of 1.5.

### Code Snippets
Code snippets should be formatted using a monospace font like "Courier New" or "Consolas", with a font size slightly smaller than the body text to ensure readability.

## Component Styles

### Buttons
- **Primary Button:** Use primary color (#007BFF). Text color: white.
- **Secondary Button:** Use secondary color (#6C757D). Text color: white.
- **Success Button:** Use success color (#28A745). Text color: white.
- **Danger Button:** Use danger color (#DC3545). Text color: white.

Buttons should have padding of 10px 20px and rounded corners with a radius of 4px.

### Input Fields
Input fields should use the primary color as their border. When focused, the border should change to secondary color. Placeholder text should be in gray (#6C757D).

### Text Areas
Text areas should have similar styling to input fields but with a larger height and more padding for better usability.

### Cards
Cards are used to group related content together. They should have a light gray background (#F8F9FA) and rounded corners with a radius of 4px. Cards should also include drop shadows for depth.

## Layouts

### Dashboard
The dashboard is the main page where users will spend most of their time. It should feature:

- A header with the project name and user profile.
- Navigation sidebar on the left with links to different sections (e.g., Tasks, Calls).
- A main content area on the right that updates based on the selected section.

### Task List
The task list should display all tasks in a table format. Each row should include:

- **Task Name:** The name of the task.
- **Description:** A brief description of what needs to be done.
- **Status:** Current status of the task (e.g., "Pending", "Completed").
- **Action Buttons:** Options to edit, delete, or assign a task.

### Call Details
The call details page should display information about a specific call. It may include:

- **Call ID:** Unique identifier for the call.
- **Name:** Name of the call.
- **Sector:** Sector associated with the call.
- **Description:** Full description of the call.
- **Funding Information:** Total funding, funding percentage, and other relevant financial data.
- **Deadline:** Deadline for completing the call.
- **Status:** Current processing and analysis status.
- **Relevance Score:** A score indicating how relevant the call is.

## Navigation

### Header
The header should be fixed at the top of the page and include:

- The project name.
- User profile (name, avatar).
- Navigation links to different sections of the dashboard.

### Sidebar
The sidebar should be fixed on the left side of the page and include:

- Links to different sections (e.g., Tasks, Calls).

## Icons

Icons will be used sparingly to enhance the visual appeal without overwhelming users. Common icons may include:

- **Add Icon:** For creating new items.
- **Edit Icon:**