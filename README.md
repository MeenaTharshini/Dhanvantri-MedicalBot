# 🌿 Dhanvantri AI – Preventive Health & Wellness Companion

**Predict • Prevent • Protect**

Dhanvantri AI is a **safety-first AI health and wellness companion** designed to provide responsible, preventive health guidance through conversational AI.

Inspired by **Lord Dhanvantari**, the traditional symbol of Ayurveda and healing, the project combines **modern AI technology with traditional wellness knowledge**, while clearly distinguishing traditional practices from evidence-based medical information.

The system is designed not only to answer health-related questions, but also to recognize situations where providing ordinary chatbot advice may be unsafe.

---

## 🩺 What Makes Dhanvantri AI Different?

Dhanvantri AI follows a **hybrid safety-first architecture** that combines rule-based medical safeguards with AI-powered conversation.

### 🛡️ Safety Layer

The safety layer prioritizes user protection by:

* 🚨 Recognizing potential emergency symptoms
* 🏥 Prioritizing urgent medical care when appropriate
* 💊 Handling medication-related questions cautiously
* ⚠️ Avoiding unsafe or harmful medication guidance
* 🩺 Preventing the chatbot from presenting responses as definitive diagnoses
* 🔍 Encouraging professional medical evaluation when necessary
* 📱 Providing concise emergency guidance suitable for mobile users

### 🤖 AI Conversation Layer

The AI layer handles:

* General health and wellness questions
* Conversational explanations
* Symptom-related discussions
* Preventive health guidance
* Lifestyle and wellness suggestions
* Context-aware conversations
* Tamil + English interactions

This combination provides a balance between **AI flexibility and rule-based safety controls**.

---

## 🌿 Traditional Wellness Knowledge

Dhanvantri AI includes knowledge related to:

* 🪔 Ayurveda
* 🌿 Siddha medicine
* 🌱 Herbal and traditional home practices
* 🧘 Yoga and lifestyle practices
* 🧠 Emotional and preventive wellness

Traditional practices are presented as **traditional knowledge rather than guaranteed medical treatments**, with appropriate distinction between traditional claims and modern scientific evidence.

---

## 🚨 Emergency Symptom Recognition

One of the key safety features is the ability to recognize potentially serious situations.

For example, when a user asks:

> **"I am vomiting a lot of blood. What should I do?"**

Dhanvantri AI is designed to avoid responding with ordinary home remedies or medication suggestions.

Instead, it prioritizes the possibility of a **medical emergency** and directs the user toward immediate professional medical care.

This reflects the project's central principle:

> **A health AI should know when not to behave like an ordinary chatbot.**

---

## 💊 Medication Safety

Dhanvantri AI includes safeguards for medication-related conversations, including scenarios such as:

* Missed doses
* Questions about taking additional doses
* Potentially harmful medication requests
* Requests involving excessive dosage
* Questions where professional medical advice may be necessary

The system is designed to avoid blindly generating potentially dangerous medication instructions.

---

## 🩺 Diagnosis Safety

Dhanvantri AI does **not aim to replace clinical diagnosis**.

When users ask questions such as:

> "I have fever, cough and body pain. Do I definitely have dengue?"

the system is designed to explain that symptoms alone cannot establish a definitive diagnosis and that appropriate medical evaluation or testing may be required.

---

## 🌿 Ayurveda, Siddha & Evidence Awareness

The project combines traditional wellness knowledge with modern AI while maintaining an important distinction between:

**Traditional practice → Scientific evidence → Medical advice**

For example, users can ask about natural remedies and traditional Ayurveda or Siddha practices while the system explains that traditional use and scientific evidence are not necessarily equivalent.

---

## 🌐 Tamil + English Support

Dhanvantri AI supports conversations in both:

* 🇬🇧 English
* 🇮🇳 Tamil

This helps make health and wellness information more accessible to users who are more comfortable communicating in their regional language.

---

## 🧠 Context-Aware Conversations

The chatbot maintains conversation history to provide more context-aware responses.

Instead of treating every question as completely independent, Dhanvantri AI can use relevant previous conversation context when responding to follow-up questions.

---

## 🔄 AI Reliability

The project uses a **primary + fallback AI architecture** to improve reliability.

If the primary AI service encounters an issue, the fallback mechanism can help maintain conversational availability where possible.

This makes the system more resilient than relying on a single AI response path.

---

## 💬 Chat & User Features

Dhanvantri AI currently includes:

* 🔐 User authentication
* 📝 Login and signup
* 💬 Persistent chat conversations
* 📚 Conversation history
* 🔎 Conversation search
* 🗑️ Conversation management
* 👤 Wellness profile
* 📋 Daily health check-ins
* 📊 Wellness dashboard
* 💡 Daily health tips
* 🧘 Wellness practices
* 📱 Responsive mobile interface

---

## 🏗️ Hybrid Architecture

The overall system can be viewed as:

```text
                User
                  │
                  ▼
          ┌───────────────┐
          │   Flask Web   │
          │   Interface   │
          └───────┬───────┘
                  │
                  ▼
        ┌─────────────────────┐
        │   Safety Layer      │
        │                     │
        │ Emergency Detection │
        │ Medication Safety   │
        │ Diagnosis Safety    │
        └──────────┬──────────┘
                   │
            ┌──────┴──────┐
            ▼             ▼
     Rule-Based       AI Layer
       Guidance      Primary + Fallback
            │             │
            └──────┬──────┘
                   ▼
          Context-Aware Response
                   │
                   ▼
                User
```

The goal is to combine:

**Safety + AI + Traditional Wellness + Personalization**

---

## 🛠️ Technology Stack

* **Python**
* **Flask**
* **HTML5**
* **CSS3**
* **JavaScript**
* **SQLite**
* **AI APIs / LLMs**
* **Markdown rendering**
* **Lucide Icons**
* **Three.js**

---

## 🚀 Running the Project

Clone the repository and install the dependencies:

```bash
git clone https://github.com/MeenaTharshini/Dhanvantri-MedicalBot.git
cd Dhanvantri-MedicalBot
pip install -r requirements.txt
```

Run the Flask application:

```bash
python app.py
```

Then open the local application in your browser.

---

## 🧪 Current Development Focus

The project is currently focused on improving:

* 🛡️ AI safety evaluation
* 🚨 Emergency-response testing
* 💊 Medication safety
* 🩺 Diagnosis safeguards
* 🌿 Traditional medicine evidence awareness
* 🌐 Tamil + English interaction
* 🧠 Context-aware responses
* 🔄 AI reliability and fallback handling
* 📱 Overall user experience

---

## 🚀 Future Enhancements

Planned improvements include:

* 🎤 Voice-based interaction
* 📊 Advanced lifestyle and symptom analysis
* 🧠 More personalized wellness recommendations
* 🌐 Web deployment
* 📱 Progressive Web App support
* 🧪 Expanded safety evaluation and testing
* 🕉️ Hindu Panchang integration
* 📈 Wellness trend visualization
* 🔐 Further privacy and security improvements

---

## ⚠️ Medical Disclaimer

**Dhanvantri AI is an experimental preventive health and wellness companion, not a doctor or a replacement for professional medical care.**

The system may provide general health information, traditional wellness practices, and AI-generated responses that can contain errors.

* Do not use the chatbot to diagnose a medical condition.
* Do not rely on it for emergency medical decisions.
* Do not use AI responses as a substitute for a qualified healthcare professional.
* For serious, worsening, or emergency symptoms, seek appropriate professional medical care immediately.

Traditional Ayurveda, Siddha, herbal, and natural practices presented by the system should not be interpreted as proven treatments unless supported by appropriate scientific evidence.

---

## 🙏 Inspiration

Inspired by **Lord Dhanvantari**, traditionally associated with Ayurveda and healing, Dhanvantri AI explores how traditional wellness concepts and modern artificial intelligence can be brought together responsibly.

The core idea is simple:

> **Technology should not only become smarter. It should become safer.**

---

## 👩‍💻 Author

**Meena Tharshini I**

B.E. Computer Science & Engineering
Aspiring Tech Enthusiast | AI & Software Development

---

## 🌱 Project Vision

Dhanvantri AI is an ongoing learning and development project exploring:

**Artificial Intelligence × Healthcare Safety × Traditional Wellness × Responsible Technology**

The project is continuously evolving through testing, experimentation, and safety improvements.
