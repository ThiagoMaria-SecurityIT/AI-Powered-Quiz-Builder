# AI-Powered Quiz Builder: An Incident Response Learning Tool   

Welcome! This project is a simple, interactive desktop application designed to help people learn the fundamentals of cybersecurity incident response. But it's also something more: **it's a case study in how anyone can team up with an AI to build a custom learning tool from scratch.**

<img width="450" height="450" alt="image" src="https://github.com/user-attachments/assets/6c094109-c7c9-49b2-a70e-d49f5c165002" /> <img width="450" height="450" alt="image" src="https://github.com/user-attachments/assets/3f504e43-f918-4eb0-9e4c-de4553a7aa02" />  
   


## What Does This Application Do?

Imagine you're on a cybersecurity team, and a hacker tries to break into your company's network. What do you do first? What are the steps to contain the damage and kick the hacker out?

This application turns that process into a interactive quiz. It's built around the six phases of Incident Response, a standard framework used by professionals worldwide:  

> **Inspiration Source:** [SANS Glossary of Security Terms: Incident Response](https://www.sans.org/security-resources/glossary-of-terms/incident-response )  

1.  **Preparation:** Getting ready before an attack happens.
2.  **Identification:** Figuring out that you've been hacked.
3.  **Containment:** Stopping the problem from getting worse.
4.  **Eradication:** Removing the hacker and their tools completely.
5.  **Recovery:** Getting everything back to normal.
6.  **Lessons Learned:** Figuring out how to prevent it from happening again.

The app has two main modes:
*   **Learn Mode:** Read simple descriptions and examples for each of the six phases.
*   **Quiz Mode:** Test your knowledge by matching real-world activities to the correct phase.

After you finish the quiz, you get a detailed report card that shows your score, which questions you got right or wrong, and even gives you **"Study Recommendations"** on which phases you should review!

<img width="450" height="450" alt="image" src="https://github.com/user-attachments/assets/e5874450-7e8c-4366-b3d2-53271f6c62e7" />



## The Story Behind the Code: A Partnership with AI

This application wasn't built by a large team of software developers. **It was built through a conversation between a human and an AI assistant (like me and Manus!).**

This is how we did it, and it shows how anyone can use AI to bring their ideas to life:

#### Step 1: The Simple Idea
It all started with a request: "Can you make a Python program to help people learn about Incident Response?"

The AI's first version was just a simple text-based quiz that ran in a black-and-white terminal window. It worked, but it wasn't very user-friendly.

#### Step 2: Making It Visual
The next request was to make it a real desktop application with buttons and a graphical user interface (GUI). The AI generated the code for a clickable, visual app.

#### Step 3: Finding and Fixing Bugs (Teamwork!)
The first visual version had problems! Some buttons didn't work right, and the quiz wouldn't clear your old answers. This is where teamwork was essential. The human user would describe the problem ("When I click next, the old answer is still checked"), and the AI would research the standard way to fix it and provide corrected code. This back-and-forth process of finding and fixing bugs is exactly how real software is made.

#### Step 4: Adding Features, One by One
Once the app was stable, we started adding new features in small, manageable steps:
*   "Let's add a final score at the end."
*   "Can we get a detailed review of all my answers?"
*   "It would be great if it told me what I need to study most."
*   "What if I want to save my results to a file?"

With each request, the AI modified the code, and the human tested it, creating a powerful feedback loop that resulted in the polished application you see today.

## Why This Matters: AI for Everyone

This project is about more than just cybersecurity. It's a blueprint for how you can use AI to create your own custom learning tools for **any subject**.

Imagine if you wanted to create a quiz for:
*   **New Employee Onboarding:** A quiz on company policies and values.
*   **Sales Team Training:** A quiz to help them remember product features.
*   **Safety Compliance:** An interactive test on workplace safety procedures.
*   **Learning a New Language:** A simple app to practice vocabulary.

You don't need to be an expert programmer anymore. If you have a clear idea and can describe what you want, you can guide an AI partner to build a tool that helps you, your team, or your community learn better. This project is proof of that.

## How to Use This Application

1.  Make sure you have Python installed on your computer.
2.  You will also need a library called PyQt. You can install it by opening a terminal or command prompt and typing: `pip install PyQt6`
3.  Download the `ir_gui_app.py` file from this repository.
4.  Run the application from your terminal with the command: `python ir_gui_app.py`

Feel free to explore the code, but more importantly, we hope you feel inspired to think about what custom tools you could build with an AI partner.
