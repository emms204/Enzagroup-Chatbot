## User Documentation for RASA Chatbot

### Introduction
RASA is an open-source machine learning framework for building conversational AI applications, such as chatbots. RASA enables the development of chatbots that can handle complex and nuanced human conversations.

### Installation

1. **Prerequisites**:
   - Python (3.6, 3.7, 3.8, or 3.9)
   - pip

2. **Install RASA**:
   Run the following command in your terminal:
   ```bash
   pip install rasa
   ```

3. **Create a New RASA Project**:
   Navigate to the directory where you want your project to be set up and run:
   ```bash
   rasa init
   ```

### Understanding RASA Components

1. **NLU (Natural Language Understanding)**:
   - Handles understanding user messages through intent classification and entity extraction.
   - Defined in `nlu.yml`, where you specify examples for each intent and entity.

2. **Stories**:
   - Stories are sample conversations that define how dialogs should flow.
   - Stored in `stories.yml`, they guide the model on expected sequences of intents and actions.

3. **Rules**:
   - Rules define fixed conversational behaviors that always follow the same path.
   - Specified in `rules.yml`, they are used for straightforward interactions that do not require machine learning, such as greetings or fallbacks.

4. **Domain**:
   - The domain specifies the universe in which your bot operates. It defines intents, entities, slots, responses, and actions.
   - Configured in `domain.yml`.

5. **Config**:
   - Defines the pipeline for processing messages and the policies for deciding actions.
   - Configured in `config.yml`, where you can specify the NLU pipeline and the policies your model should use.

6. **Custom Actions**:
    - A custom action can run any code you want, including API calls, database queries etc.
    - Configured in `actions.py`.

### Training Your RASA Model

1. **Prepare Training Data**:
   - Populate your `nlu.yml` with examples for each intent.
   - Define stories in `stories.yml` that reflect typical conversations.
   - Set up rules in `rules.yml` for predictable interactions.

2. **Train the Model**:
   Run the following command to train your model based on the provided data:
   ```bash
   rasa train
   ```
   
### Deploying Your RASA Chatbot

0. **Run Custom Actions**:
    If you have any available Custom Actions, run it first:
      ```bash
      rasa run actions
      ```

1. **Local Testing**:
   - Start your chatbot locally to test the interactions:
     ```bash
     rasa shell
     ```
2. **Debug the Model**:
   Run the following command to debug the model predictions:
   ```bash
   rasa shell --debug
   ```

3. **Deployment**:
    - You can launch the Index.html on a webserver to interact with the Chatbot, start the chatbot locally to test the interactions:
      ```bash
      rasa run --enable-api --cors="*"
      ```
    - For production, you can deploy your RASA chatbot on servers or platforms like RASA X, which provides tools for CI/CD, version control, and user testing.

### Tips for Effective Model Development

1. **Iterative Development**:
   - Continuously improve your bot by expanding training data, refining the domain, and adjusting policies based on real user interactions.

2. **Interactive Learning**:
   - Use `rasa interactive` to refine your model by correcting it in real-time, improving the understanding and flow based on actual user inputs.

3. **Monitoring and Analytics**:
   - Monitor interactions and use analytics to understand usage patterns and identify areas for improvement.


This documentation provides a foundational guide to new users for setting up and managing the ENZA RASA chatbot, tailored to their needs and specifications.
