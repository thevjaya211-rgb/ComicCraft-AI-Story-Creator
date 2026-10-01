# Project Design Phase

## Project Title
ComicCraft AI Story Creator

## System Overview
ComicCraft AI Story Creator is a web-based application that
converts a user's comic idea into an AI-generated story and
five comic panels.

## System Flow

User enters comic idea
        ↓
Select AI provider
        ↓
Generate story
        ↓
Generate five comic panels
        ↓
Save panel images
        ↓
Combine story and panels
        ↓
Generate Comic PDF
        ↓
Display final comic

## Main Modules

### 1. User Interface
Provides a simple web interface for entering the comic idea
and selecting the generation options.

### 2. Story Generation
Uses AI to generate a story from the user's input.

### 3. Image Generation
Generates five comic panel images based on the story idea.

### 4. Image Storage
Stores the generated panel images as PNG files.

### 5. PDF Generation
Combines the story and five comic panels into a single PDF.

## Technologies Used

- Python
- FastAPI
- HTML/CSS
- Gemini API
- Pollinations API
- Pillow
- ReportLab
- Git
- GitHub

## Output

The final output consists of:
- AI-generated story
- Five comic panel images
- A downloadable comic PDF