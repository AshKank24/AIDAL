# Socratic AI Teaching Assistant for Sorting Algorithms

## Overview

This project was developed as part of the Google Gen AI Exchange Hackathon. The goal is to create a Gen AI-powered teaching assistant that uses the Socratic method to teach Data Structures and Algorithms, specifically focusing on Sorting Algorithms. The Socratic method is a form of cooperative argumentative dialogue that stimulates critical thinking, where the AI asks a series of questions to guide the student toward the correct answer instead of directly providing it.

## Features

### 1. Socratic Questioning Engine
- **Dynamic Question Generation**: The AI dynamically generates probing questions based on the student's input, leading them to discover answers on their own.
- **Context Awareness**: The system tracks the conversation's context to ensure questions are relevant to the student’s current understanding.
- **Error Recognition**: If the student goes off track, the AI identifies this and redirects them with guiding questions.

### 2. Interactive Learning Interface
- **Real-Time Feedback**: Students receive real-time feedback as they answer questions, ensuring they stay engaged and on the right path without revealing the answer outright.
- **Code Editor Integration**: An interactive code editor is integrated into the platform, allowing students to write and test their algorithms while the AI asks questions related to their approach and optimization strategies.
- **Visual Aids**: The system can show visual aids like flowcharts and animations based on the student's responses to help them understand complex sorting algorithms.

### 3. Personalized Learning Path
- **Skill Assessment**: The learning journey begins with an assessment to gauge the student’s initial understanding of sorting algorithms, allowing the AI to tailor the level of questioning accordingly.
- **Adaptive Learning**: The difficulty and depth of the questions are adjusted based on the student's progress, ensuring a personalized learning experience.
- **Progress Tracking**: A dashboard is provided to track the student’s progress over time, highlighting strengths and areas needing improvement.

## Technical Implementation

### Language Model Selection
- **Pre-trained Large Language Model**: The project utilizes a pre-trained large language model (e.g., GPT-4 or LLaMA-3), fine-tuned specifically on educational content related to sorting algorithms, to handle natural language processing and Socratic questioning.

### Backend Architecture
- **Question Generator**: A rule-based system combined with the language model is used to generate questions dynamically based on user input.
- **Code Execution Environment**: The system includes a sandboxed environment (e.g., using Docker) for safe code execution, allowing the assistant to analyze code written by students.
- **Context Management**: A session management system is implemented to keep track of the student's learning path and previous interactions.

### Frontend Development
- **User Interface**: The user interface is developed using React.js, offering a side panel for the Socratic assistant and a main panel for coding.
- **Visualization Tools**: Tools like D3.js are used to create real-time visualizations of algorithm behavior, aiding in student comprehension.

### AI Safety and Bias Mitigation
- The model is regularly updated to avoid reinforcing biases and effectively handle diverse student interactions.
- User feedback loops are implemented to continually refine and improve the questioning logic.

## Roadmap

- **Phase 1**: Develop the MVP with core Socratic questioning and a basic code editor. Test with a small user base.
- **Phase 2**: Implement advanced features like progress tracking, adaptive learning paths, and visual aids.
- **Phase 3**: Polish the UI/UX and prepare for the final presentation, ensuring all aspects of the project meet the judging criteria.

## Getting Started

### Prerequisites
- Node.js
- Docker
- Python (for backend services)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/AshKank24/CerebroX.git
   ```
2. Install dependencies for the frontend:
   ```bash
   cd frontend
   npm install
   ```
3. Start the frontend server:
   ```bash
   npm start
   ```
4. Set up the backend services:
   ```bash
   cd backend
   docker-compose up
   ```

### Usage
- Access the application via `http://localhost:3000`.
- Start learning by engaging with the Socratic AI Assistant on the topic of sorting algorithms.

## Contributing

We welcome contributions! Please refer to our [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.