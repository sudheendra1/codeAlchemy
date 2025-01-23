# CodeAlchemy: AI-Powered Interactive Debugging Assistant

## Overview

The AI-Powered Interactive Debugging Assistant revolutionizes the traditional debugging process by enabling developers to communicate directly with their codebase. By establishing a contextual understanding of the entire codebase and engaging in targeted dialogue with users, the system offers intelligent debugging support and problem resolution. It minimizes the time spent manually tracing through complex codebases, providing accurate solutions while ensuring safety through verification steps.

Key features include:

- Contextual understanding of the entire codebase.
- Interactive and natural language dialogue with developers.
- Intelligent step-by-step error debugging.
- Secure, targeted requests for relevant code snippets rather than the entire codebase.

## System Components

### Backend

The backend handles the AI-powered logic for parsing, analyzing, and debugging the code. It ensures the contextual understanding of the codebase and processes user queries for targeted problem resolution.

### Frontend

The frontend provides an intuitive user interface for developers to interact with the debugging assistant. It enables users to explore their codebase, submit queries, and receive detailed debugging insights.

## Setup Instructions

Follow these steps to set up and run the AI Debugger:

### Prerequisites

```
Python 3.8 or later
Node.js and npm
A modern web browser
```

### Backend Setup

1. Clone this repository to your local machine.
2. Navigate to the backend directory:
```
cd api
```
3. Install the required dependencies:
```
pip install -r requirements.txt
```
4. Run the backend server:
```
python main.py
```
5. The backend will start running on the configured port (e.g., http://localhost:5000).

### Frontend Setup

1. Navigate to the frontend directory:
```
cd website/codealchemy
```
2. Install the required dependencies:
```
npm install
```
3. Start the frontend development server:
```
npm run dev
```
4. The frontend will start running on the configured port (e.g., http://localhost:3000).

## Usage

1. Start both the backend and frontend servers as described above.
2. Open your web browser and navigate to the frontend development server (e.g., http://localhost:3000).
3. Interact with the debugging assistant by uploading relevant code snippets, submitting queries, or exploring your codebase interactively.
