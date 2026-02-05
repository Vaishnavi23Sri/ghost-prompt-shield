# Ghost Prompt Shield
A lightweight backend safety layer for evaluating AI prompts before model execution.

Ghost Prompt Shield is a small backend service I built to solve a problem I noticed while working with AI tools. Many AI systems can be tricked just by the way a prompt is written. Users can slowly push the model to ignore rules, act like a system, or reveal things it shouldn’t.

Instead of trying to fix this after the AI already responds, I designed Ghost Prompt Shield to sit before the AI model. Every prompt first passes through this layer. The system checks whether the prompt looks safe, suspicious, or clearly unsafe, and then decides whether it should be allowed, warned, or blocked.

The project doesn’t generate AI responses on its own. Its job is to make a decision — ALLOW, WARN, or BLOCK — so it can be used as a safety layer in any AI application. I built it as a backend API using Python and FastAPI and deployed it on Render so it works like a real service, not just local code.

I tested it using normal user questions, clearly malicious prompts, and gradual escalation cases to make sure safe prompts aren’t blocked unnecessarily, while risky ones are stopped early. The focus was on correct behavior and safety, not on heavy machine-learning models. I intentionally kept the logic explainable, because in security systems, transparency matters more than complexity.

### Tech Used
- Python
- FastAPI
- Rule-based safety logic
- Deployed on Render

Live API: https://ghost-prompt-shield.onrender.com  
GitHub Repo: https://github.com/Vaishnavi23Sri/ghost-prompt-shield
