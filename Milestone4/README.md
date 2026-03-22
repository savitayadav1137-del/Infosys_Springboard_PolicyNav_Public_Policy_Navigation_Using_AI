# PolicyNav – Intelligent Policy & Document Navigation System
PolicyNav is an AI-powered document understanding and policy navigation platform that allows users to search, analyze, and interact with complex policy documents using Retrieval-Augmented Generation (RAG) and modern Natural Language Processing techniques.

The system combines semantic search, AI-based question answering, analytics dashboards, and user management tools to provide an intelligent environment for document exploration.

# System Overview
PolicyNav integrates multiple technologies into a single platform:

- AI-powered document search
- RAG-based question answering
- User and Admin dashboards
- Interactive data visualization
- Feedback analysis
- Profile personalization
The application is built primarily using Streamlit, Transformers, Sentence Transformers, FAISS, and SQLite.

# Admin Dashboard (Management & Analytics)
The Admin Dashboard functions as the central command center for monitoring and managing the entire system.

## User Control
Admins can manage all registered users with the following actions:

- Promote normal users to Admin
- Lock / Unlock user accounts
- Delete user accounts
- Monitor user activity
This ensures proper role-based access control and security.

## Activity Tracking
The admin panel allows administrators to track:
 - Currently active users
 - Historical login activity
 - System usage logs
 - User interaction history
 - This provides visibility into system behavior and engagement.

## Data Visualization
The admin dashboard includes interactive charts and graphs to analyze system usage.
Admins can view insights about:

## Model Usage
Shows which AI models are used most frequently.

## Language Usage
Displays languages being used by users when interacting with the system.

## Feature Usage
Tracks the most frequently used platform features such as:
- RAG search
- Readability analysis
- Document analysis
- Dashboard features
These insights help administrators understand system adoption patterns.

## Feedback Analysis
User feedback is analyzed using a WordCloud visualization.
This allows admins to quickly identify:
 - Frequently mentioned keywords
 - User concerns
 - Popular feature requests
The visual representation highlights the most dominant topics mentioned by users.

## Data Export
Admins can export system data for reporting and analysis.
Exportable data includes:
 - User information
 - Feedback data
 - Query history
 - System logs
This feature supports administrative reporting and auditing.

# User Dashboard & Profile Personalization
The User Dashboard provides a personalized and secure experience for users interacting with the platform.

## Security Features
Users can manage their account security by:
 - Updating their email address
 - Changing their password
The system includes security mechanisms such as:
 - JWT-based authentication
 - Password hashing
 - Login attempt restrictions
 - Account lock protection

## Profile Personalization
Users can personalize their profile with:
 - Avatar / Display Picture upload
 - Profile updates
 - Account settings
This helps create a customized user experience.

## UI / UX Enhancements
The interface is designed to improve usability and navigation.
Features include:
 - Clean dashboard layout
 - Interactive data visualizations
 - Fast document search
 - Clear result displays
The goal is to provide a smooth and intuitive user workflow.

# Retrieval-Augmented Generation (RAG)
The platform uses a Retrieval-Augmented Generation (RAG) architecture for intelligent document search and question answering.
RAG combines:
 - Document retrieval
 - Language model generation
to provide context-aware responses.

# Document Processing Pipeline
 1.Documents are uploaded or stored in the system.
 2.Text is extracted from documents.
 3.The text is divided into smaller chunks.
 4.Each chunk is converted into vector embeddings.
 5.The embeddings are stored in a vector index.
When a user asks a question:
 1.The query is converted into an embedding.
 2.The system retrieves the most relevant document chunks.
 3.The retrieved context is passed to a language model.
 4.The model generates the final answer.

#  Vector Database
The system uses FAISS (Facebook AI Similarity Search) for vector indexing.
FAISS enables:
 - Fast similarity search
 - Efficient vector retrieval
 - Scalable semantic search
This allows the system to retrieve relevant document sections quickly.

# NLP & Text Analysis Features
The system also provides additional Natural Language Processing capabilities.

## Readability Analysis
Using the TextStat library, the system calculates readability metrics such as:
 - Flesch Reading Ease
 - Reading Grade Level
 - Sentence complexity
 - Word difficulty
This helps users understand how easy or difficult a document is to read.

## Linguistic Analysis
Using SpaCy, the system performs:
 - Named Entity Recognition
 - Tokenization
 - Dependency Parsing
This enables deeper text structure analysis.

# Technology Stack
## Frontend
 - Streamlit
 - Streamlit Option Menu
 - Plotly
 - PyVis

## Backend
 - Python
 - JWT Authentication
 - Bcrypt password hashing
 - SQLite Database
 - 
## Visualization
 - Plotly
 - WordCloud
 - Matplotlib

# Database
The platform uses SQLite for storing system data.
Stored information includes:
 - User accounts
 - Login history
 - Feedback
 - Query logs
 - System activity

# Installation
Install dependencies:
Run the application Cell by cell

# Screenshots
## User Profile Page
<img width="1897" height="842" alt="My_Profile" src="https://github.com/user-attachments/assets/6e91ca14-4fbf-45a9-80e4-dd31345498f1" />

<img width="1322" height="532" alt="avatar" src="https://github.com/user-attachments/assets/f3b3ce12-df93-4d59-a604-05fcedc17c80" />

<img width="1122" height="665" alt="change_email" src="https://github.com/user-attachments/assets/f096989e-c506-4fa9-b324-94381238b27e" />

<img width="1507" height="847" alt="ChangePassword" src="https://github.com/user-attachments/assets/5a9ba344-1858-4ebe-9453-51f74141c94e" />

## Admin Dashboard
<img width="1917" height="890" alt="admin_dashboard" src="https://github.com/user-attachments/assets/57d2ccd9-4b9f-46e2-bdd1-07f88748a860" />

## Feedback Analysis
<img width="1913" height="826" alt="Feedback_analysis1" src="https://github.com/user-attachments/assets/a9cbdb8d-2bf1-4a64-9f45-f2fab041e08e" />
<img width="1918" height="880" alt="Feedback_analysis2" src="https://github.com/user-attachments/assets/0c626799-ed3f-476f-aee1-a4e694ce4254" />

## Activity Tracking
<img width="1918" height="898" alt="Activittracking" src="https://github.com/user-attachments/assets/5915ffdb-108d-4863-8140-0239b3ab5070" />

## Analytics Charts
<img width="1485" height="811" alt="analytics1" src="https://github.com/user-attachments/assets/9ee0aa15-c430-4e0f-88ae-b409e93e3069" />
<img width="1907" height="822" alt="analytics2" src="https://github.com/user-attachments/assets/8e87ba1e-19a0-4b10-a59e-bd8ed3ec8e2e" />

## Data Export
<img width="1916" height="750" alt="dataexport" src="https://github.com/user-attachments/assets/1a8c0c48-040d-46f0-b1f9-54c34640202e" />

## Authors
1.Savita Yadav
2.Velagada Devi Sri Prasad
3.Sanjay Janarthan
4.Aarthi Chandolkar
5.Ramya Kuruvaladoddi 
6.Pooja K K
