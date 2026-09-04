# LLP -- Language Learning Pal

## Cultural Bridge Agent -- Project Documentation

### 1. Project Overview

**Language Learning Pal (LLP)** is an AI-powered language learning
application designed to help learners improve vocabulary, grammar,
translation, pronunciation, daily phrases, synonyms, antonyms, and
conversational English.

The current project version is **LLP V1**. This version includes a
**Cultural Bridge Agent** that helps identify language patterns
influenced by Indian-language literal translations and suggests more
natural English alternatives.

### 2. Cultural Bridge Agent

The Cultural Bridge Agent is designed to bridge the gap between
grammatically understandable Indian English and natural,
context-appropriate English.

For example:

  ------------------------------------------------------------------------------------
  Input                                            Agent response
  ------------------------------------------------ -----------------------------------
  `Yesterday itself I completed the work.`         `I completed the work yesterday.`

  `Please do the needful and revert back to me.`   A more natural professional-English
                                                   alternative is suggested.

  `I finished the work yesterday.`                 The sentence is treated as natural
                                                   English and does not need
                                                   unnecessary correction.
  ------------------------------------------------------------------------------------

The agent is intended to **improve clarity and naturalness without
changing the user's intended meaning**.

### 3. Technology Stack

#### Backend

-   Python
-   FastAPI
-   Pydantic
-   Local LLM integration through Ollama
-   Modular agent/service architecture
-   Automated tests with pytest

#### Frontend

-   React
-   Vite
-   JavaScript/JSX
-   CSS

#### AI/LLM

-   Ollama for local model serving
-   Local Ministral/Mistral-family model used for the Cultural Bridge
    Agent
-   Prompt-based guidance for cultural/language correction

### 4. High-Level Architecture

``` text
User
  |
  v
React Frontend
  |
  | HTTP API
  v
FastAPI Backend
  |
  v
Agent Controller / Chat Flow
  |
  +--------------------+
  |                    |
  v                    v
Intent / Tool Logic    Cultural Bridge Agent
                           |
                           v
                     Prompt + Local LLM
                           |
                           v
                    Natural English Response
```

### 5. Main Backend Areas

The backend contains modular components for:

-   Agent control and execution
-   Intent classification
-   LLM communication
-   Prompt management
-   Cultural Bridge processing
-   Grammar and language tools
-   Vocabulary
-   Synonyms and antonyms
-   Translation
-   Pronunciation
-   Word of the day
-   Memory and personalization
-   Guardrails
-   Analytics
-   Testing

### 6. Frontend

The React frontend provides the user-facing application and includes
components/pages for:

-   Chat interaction
-   Agent status
-   Authentication
-   Dashboard
-   Learning analytics
-   Learner profile
-   Roadmap
-   Today's learning plan
-   Example prompts
-   Project/features information

The frontend communicates with the backend through the API service.

### 7. API Configuration

The frontend API service is configured to communicate with the local
FastAPI server.

Typical local backend address:

``` text
http://127.0.0.1:8000
```

The frontend can use the `VITE_API_URL` environment variable when a
different backend URL is required.

### 8. Running the Backend

From the project root:

``` powershell
cd backend
```

Create/activate the Python virtual environment if required, install
dependencies, and configure the required environment variables.

Install dependencies:

``` powershell
pip install -r requirements.txt
```

Start FastAPI:

``` powershell
uvicorn app.main:app --reload
```

The API is then available locally through the FastAPI server.

### 9. Running the Frontend

From the project root:

``` powershell
cd frontend
```

Install dependencies:

``` powershell
npm install
```

Start the Vite development server:

``` powershell
npm run dev
```

Open the local URL displayed by Vite in the terminal.

### 10. Environment Variables and Security

Sensitive configuration should be stored in a local `.env` file and must
not be committed to GitHub.

The repository `.gitignore` excludes sensitive and generated files such
as:

``` text
backend/venv/
backend/.env
frontend/node_modules/
frontend/dist/
*.pyc
.vscode/
.DS_Store
Thumbs.db
```

Never commit API keys, passwords, OAuth secrets, or other credentials.

### 11. Testing

The project contains backend tests and dedicated Cultural Bridge Agent
test scripts.

Examples of validation performed for the Cultural Bridge Agent include:

``` text
Yesterday itself I completed the work.
```

and

``` text
Please do the needful and revert back to me.
```

The tests verify that the agent can identify relevant
Indian-English/literal phrasing and provide a more natural English
formulation while preserving the intended meaning.

Natural English examples are also tested to reduce unnecessary
corrections.

### 12. GitHub Workflow

The project is maintained in a private GitHub repository:

``` text
LLP_Project
```

Recommended workflow for contributors:

``` powershell
git pull origin main
```

Make changes, test them, then:

``` powershell
git add .
git commit -m "Describe your change"
git push origin main
```

For larger team changes, contributors should preferably work on a
separate branch and create a pull request.

### 13. Project Structure

A simplified structure is:

``` text
LLP_Project/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── config/
│   │   ├── models/
│   │   ├── prompts/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── storage/
│   │   ├── tools/
│   │   └── utils/
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── styles/
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

### 14. Purpose of the Cultural Bridge Feature

The Cultural Bridge Agent focuses on language improvement rather than
simply flagging grammar errors. Its purpose is to help learners
understand when a sentence is technically understandable but sounds
unnatural in professional or general English.

The feature can be useful for:

-   Professional communication
-   Emails and workplace messages
-   Everyday English
-   Learners influenced by their first language
-   Improving natural sentence construction

### 15. My Work – Cultural Bridge Agent

#### Work Completed

The main assigned work for the **Cultural Bridge Agent** in LLP has been completed and locally tested.

The completed work includes:

- Implemented the **Cultural Bridge Agent** in the LLP backend.
- Integrated the agent with the local **Ollama** LLM setup.
- Used the locally available **Ministral 3 8B** model for the implementation/testing.
- Added handling for **Indian-English and literal-translation influenced phrasing**.
- Added prompt-based logic to improve sentences while preserving the user's intended meaning.
- Tested the agent with Indian-English examples such as:
  - `Yesterday itself I completed the work.` → `I completed the work yesterday.`
  - `Please do the needful and revert back to me.` → a more natural professional-English alternative.
- Verified that natural English such as:
  - `I finished the work yesterday.`
  does not receive an unnecessary correction.
- Ran independent Cultural Bridge Agent tests successfully.
- Kept the implementation within **LLP** as the current project version.

#### Current Status

**Cultural Bridge Agent: IMPLEMENTED AND TESTED ✅**

The core agent behavior is working locally. The next stage is to complete the project handover/documentation and verify the complete application flow.

#### Pending / Remaining Work

The remaining work for the LLP project is mainly:

1. **Frontend–backend end-to-end verification**
   - Confirm the React frontend sends requests correctly to the FastAPI backend.
   - Verify that Cultural Bridge responses are displayed correctly in the UI.

2. **Final testing**
   - Run the relevant backend test suite.
   - Test additional Indian-English/literal-translation examples.
   - Verify that normal English is not over-corrected.

3. **Documentation**
   - Maintain this `DOCUMENTATION.md`.
   - Keep the main `README.md` updated with setup and project information.
   - Add research/references used for the Cultural Bridge approach where appropriate.

4. **GitHub/team collaboration**
   - The new private `LLP_Project` repository has been created and the LLP code has been pushed.

5. **Final project understanding**
   - Review the complete request flow and important files.
   - Prepare to explain the Cultural Bridge Agent, architecture, model choice, prompts, testing, and limitations confidently.

#### Model Note

The original assignment referenced **Mistral Saba**. Since Mistral Saba was not available locally, the implementation/testing was carried out with the available local **Ministral/Mistral-family model through Ollama**. This should be clearly mentioned when explaining the implementation.


### 16. Future Improvements

Potential improvements include:

-   Expanding the cultural-language pattern library
-   Adding more regional language influence patterns
-   Improving context-aware correction
-   Adding confidence/explanation scores
-   Increasing automated test coverage
-   Improving frontend feedback for corrections
-   Adding branch protection and pull-request workflow
-   Adding deployment configuration

------------------------------------------------------------------------

**Project:** Language Learning Pal (LLP)\
**Feature:** Cultural Bridge Agent\
**Repository:** LLP_Project
