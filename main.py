# import os
# import json
# import time
# from flask import Flask, render_template, request, redirect, session
# from interview_crew.crew import InterviewCrew
# app = Flask(__name__)
# app.secret_key = "harman_secret"
# crew = InterviewCrew()

# def safe_json_load(path):
#     if not os.path.exists(path):
#         return None
#     try:
#         with open(path, "r") as f:
#             data = f.read().strip()
#             if not data:
#                 return None
#             return json.loads(data)
#     except Exception as e:
#         print(f"Error loading {path}: {e}")
#         return None

# def load_or_create_questions(company, role):
#     path = "output/questions.json"
#     if os.path.exists(path):
#         os.remove(path)
    
#     print(f"Generating fresh technical questions for {company} - {role}")
    
#     try:
#         research_crew = crew.research_crew()
#         result = research_crew.kickoff(inputs={"company": company, "role": role})

#         time.sleep(5)
        
#         # Try to load the generated questions
#         new_questions = safe_json_load(path)
        
#         if new_questions and len(new_questions) > 5:
#             print(f"✅ Successfully generated {len(new_questions)} technical questions")
#             return new_questions
#         else:
#             print("❌ Generated questions are insufficient, using enhanced technical questions")
#             return get_technical_fallback_questions(company, role)
            
#     except Exception as e:
#         print(f"❌ Error generating questions: {e}")
#         return get_technical_fallback_questions(company, role)

# def get_technical_fallback_questions(company, role):
#     """Technical fallback questions - NO BEHAVIORAL"""
#     return [
#         {"question": f"Explain the most important programming concepts for a {role} at {company}"},
#         {"question": f"How would you design a scalable system for {company}'s main service?"},
#         {"question": f"What database technologies would be most suitable for {company} and why?"},
#         {"question": f"Describe your approach to solving complex technical problems at {company}'s scale"},
#         {"question": f"How would you optimize application performance for {company}'s users?"},
#         {"question": f"What security considerations are important for {company}'s type of business?"},
#         {"question": f"Explain microservices architecture and its relevance to {company}"},
#         {"question": f"How would you handle data consistency in distributed systems at {company}?"},
#         {"question": f"What cloud technologies are most suitable for {company}'s needs?"},
#         {"question": f"How would you implement CI/CD pipelines for {company}'s development process?"},
#         {"question": f"Describe your experience with containerization and orchestration technologies"},
#         {"question": f"How would you debug performance issues in production at {company}'s scale?"},
#         {"question": f"What testing strategies would you implement for {company}'s applications?"},
#         {"question": f"Explain your approach to code review and quality assurance"},
#         {"question": f"How do you stay updated with emerging technologies relevant to {company}"}
#     ]

# # ---------- ROUTES ----------
# @app.route("/")
# def start():
#     return render_template("start.html")

# @app.route("/begin", methods=["POST"])
# def begin():
#     company = request.form["company"]
#     role = request.form["role"]

#     session["company"] = company
#     session["role"] = role

#     questions = load_or_create_questions(company, role)
#     session["questions"] = questions
#     session["answers"] = []
#     session["index"] = 0

#     print(f"🚀 Starting technical interview with {len(questions)} questions for {role} at {company}")
#     return redirect("/interview")

# @app.route("/interview", methods=["GET", "POST"])
# def interview():
#     questions = session.get("questions")
#     if not questions:
#         return redirect("/")
    
#     index = session.get("index", 0)
    
#     if request.method == "POST":
#         user_answer = request.form["answer"]
#         session["answers"].append({
#             "question": questions[index]["question"],
#             "answer": user_answer
#         })
#         session["index"] = index + 1
#         session.modified = True
#         return redirect("/interview")
    
#     if index >= len(questions):
#         return redirect("/dashboard")
    
#     current_question = questions[index]
#     return render_template("interview.html",
#                            q=current_question["question"],
#                            index=index + 1,
#                            total=len(questions))

# @app.route("/dashboard")
# def dashboard():
#     answers = session.get("answers", [])
#     company = session.get("company", "Unknown Company")
#     role = session.get("role", "Unknown Role")
    
#     if not answers:
#         return "No answers to evaluate. Please complete the interview first."
    
#     print(f"📊 Evaluating {len(answers)} technical answers for {role} at {company}...")
    
#     try:
#         # Pass BOTH company and role to evaluation crew
#         eval_crew = crew.evaluation_crew()
#         eval_crew.kickoff(inputs={
#             "answers": json.dumps(answers),
#             "company": company,
#             "role": role
#         })
        
#         time.sleep(5)
        
#         report = safe_json_load("output/report.json")
        
#         if not report:
#             report = {
#                 "overall_score": 7,
#                 "strengths": [f"Good understanding of technical concepts for {role}", "Strong problem-solving approach"],
#                 "weaknesses": [f"Could provide more specific examples for {company}'s context", "Need deeper technical explanations"],
#                 "topic_scores": {
#                     "technical_knowledge": 7,
#                     "problem_solving": 8,
#                     "communication": 6
#                 }
#             }
            
#         return render_template("dashboard.html", report=report, company=company, role=role)
        
#     except Exception as e:
#         print(f"❌ Evaluation error: {e}")
#         report = {
#             "overall_score": 6,
#             "strengths": [f"Completed technical interview for {role}", f"Demonstrated interest in {company}"],
#             "weaknesses": ["Evaluation system temporarily unavailable"],
#             "topic_scores": {
#                 "technical_knowledge": 6,
#                 "problem_solving": 7,
#                 "communication": 5
#             }
#         }
#         return render_template("dashboard.html", report=report, company=company, role=role)

# @app.route("/restart")
# def restart():
#     session.clear()
#     return redirect("/")

# if __name__ == "__main__":
#     os.makedirs("output", exist_ok=True)
#     app.run(debug=True)


# import os
# import json
# import time
# from flask import Flask, render_template, request, redirect, session
# from interview_crew.crew import InterviewCrew

# app = Flask(__name__)
# app.secret_key = os.getenv("FLASK_SECRET", "harman_secret")

# def safe_json_load(path):
#     if not os.path.exists(path):
#         return None
#     try:
#         with open(path, "r", encoding="utf-8") as f:
#             data = f.read().strip()
#             if not data:
#                 return None
#             return json.loads(data)
#     except Exception as e:
#         print(f"Error loading {path}: {e}")
#         return None

# def save_questions(questions, path="output/questions.json"):
#     """Save questions to file"""
#     os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
#     with open(path, "w", encoding="utf-8") as f:
#         json.dump(questions, f, indent=2, ensure_ascii=False)

# def load_or_create_questions(company, role):
#     """Generate questions using the new InterviewCrew"""
#     print(f"🚀 Generating questions for {role} at {company}")
    
#     try:
#         crew = InterviewCrew()
#         questions = crew.generate_questions(company, role)
        
#         # Save questions for reference
#         save_questions(questions)
        
#         return questions
        
#     except Exception as e:
#         print(f"❌ Error generating questions: {e}")
#         # Fallback to basic questions
#         fallback = [
#             {"question": f"Explain key programming concepts for {role} at {company}"},
#             {"question": f"Design a scalable system for {company}'s main service"},
#             {"question": f"Database technologies suitable for {company}"},
#             {"question": f"Solve complex technical problems at {company}'s scale"},
#             {"question": f"Optimize performance for {company}'s users"}
#         ]
#         save_questions(fallback)
#         return fallback

# # ---------- ROUTES ----------
# @app.route("/")
# def start():
#     session.clear()
#     return render_template("start.html")

# @app.route("/begin", methods=["POST"])
# def begin():
#     company = request.form.get("company", "").strip()
#     role = request.form.get("role", "").strip()
    
#     if not company or not role:
#         return redirect("/")
    
#     session["company"] = company
#     session["role"] = role

#     questions = load_or_create_questions(company, role)
#     session["questions"] = questions
#     session["answers"] = []
#     session["index"] = 0

#     print(f"🎯 Starting interview with {len(questions)} questions")
#     return redirect("/interview")

# @app.route("/interview", methods=["GET", "POST"])
# def interview():
#     questions = session.get("questions")
#     if not questions:
#         return redirect("/")

#     index = session.get("index", 0)

#     if index >= len(questions):
#         return redirect("/dashboard")

#     if request.method == "POST":
#         user_answer = request.form.get("answer", "").strip()
#         if not user_answer:
#             current_question = questions[index]
#             progress = int((index + 1) / len(questions) * 100)
#             return render_template("interview.html",
#                                 q=current_question.get("question"),
#                                 index=index + 1,
#                                 total=len(questions),
#                                 progress=progress,
#                                 error="Please provide an answer")
        
#         session["answers"].append({
#             "question": questions[index]["question"],
#             "answer": user_answer
#         })
#         session["index"] = index + 1
#         session.modified = True
        
#         if session["index"] >= len(questions):
#             return redirect("/dashboard")
#         else:
#             return redirect("/interview")

#     # GET request
#     current_question = questions[index]
#     progress = int((index + 1) / len(questions) * 100)
    
#     return render_template("interview.html",
#                         q=current_question.get("question"),
#                         index=index + 1,
#                         total=len(questions),
#                         progress=progress)

# @app.route("/dashboard")
# def dashboard():
#     answers = session.get("answers", [])
#     company = session.get("company", "Unknown Company")
#     role = session.get("role", "Unknown Role")

#     if not answers:
#         return "No answers to evaluate. Please complete the interview first."

#     print(f"📊 Evaluating {len(answers)} answers...")

#     try:
#         crew = InterviewCrew()
#         report = crew.evaluate_answers(answers, company, role)
        
#         return render_template("dashboard.html", report=report, company=company, role=role)
        
#     except Exception as e:
#         print(f"❌ Evaluation error: {e}")
#         report = {
#             "overall_score": 6,
#             "strengths": [f"Completed interview for {role}", f"Interest in {company}"],
#             "weaknesses": ["Evaluation system unavailable"],
#             "topic_scores": {
#                 "technical_knowledge": 6,
#                 "problem_solving": 7,
#                 "communication": 5,
#                 "code_quality": 6,
#                 "system_design": 6
#             }
#         }
#         return render_template("dashboard.html", report=report, company=company, role=role)

# @app.route("/restart")
# def restart():
#     session.clear()
#     return redirect("/")

# if __name__ == "__main__":
#     os.makedirs("output", exist_ok=True)
#     app.run(debug=True)


from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import google.generativeai as genai
import json
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET', 'harman_secret')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

# Configure Gemini AI from .env
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

print(f"🔑 Loaded Gemini API Key: {GEMINI_API_KEY[:10]}...")
genai.configure(api_key=GEMINI_API_KEY)

def generate_questions(company, role):
    """Generate interview questions using Gemini AI"""
    try:
        print(f"🚀 Generating questions for {role} at {company}")
        
        # Try different models
        model_names = ['gemini-2.0-flash', 'gemini-pro', 'gemini-1.5-flash']
        questions = None
        
        for model_name in model_names:
            try:
                print(f"🔄 Trying model: {model_name}")
                model = genai.GenerativeModel(model_name)
                
                prompt = f"""
                Generate 7 technical interview questions for a {role} position at {company}.
                Return ONLY a JSON array with this exact format:
                
                [
                    {{"question": "First technical question"}},
                    {{"question": "Second technical question"}},
                    {{"question": "Third technical question"}},
                    {{"question": "Fourth technical question"}},
                    {{"question": "Fifth technical question"}},
                    {{"question": "Sixth technical question"}},
                    {{"question": "Seventh technical question"}}
                ]
                
                Make questions practical and specific to {role} at {company}.
                Focus on programming, system design, databases, and problem-solving.
                Return ONLY the JSON array, no other text.
                """
                
                response = model.generate_content(prompt)
                response_text = response.text.strip()
                
                print(f"📄 Raw response: {response_text[:100]}...")
                
                # Clean the response
                if '```json' in response_text:
                    response_text = response_text.split('```json')[1].split('```')[0]
                elif '```' in response_text:
                    response_text = response_text.split('```')[1].split('```')[0]
                
                response_text = response_text.strip()
                
                questions = json.loads(response_text)
                print(f"✅ Successfully generated {len(questions)} questions using {model_name}")
                break
                
            except Exception as model_error:
                print(f"❌ Model {model_name} failed: {str(model_error)[:100]}")
                continue
        
        if not questions:
            raise Exception("All models failed")
            
        return questions
        
    except Exception as e:
        print(f"❌ Error generating questions: {e}")
        # Fallback questions
        return [
            {"question": f"Explain the difference between processes and threads. Give examples when you would use each at {company}."},
            {"question": f"How would you design a scalable web application for {company}'s services?"},
            {"question": f"What database technologies would be most suitable for {company} and why?"},
            {"question": f"Describe your approach to solving complex technical problems at {company}'s scale"},
            {"question": f"How would you optimize application performance for {company}'s global users?"},
            {"question": f"What security practices are crucial for a {role} at {company}?"},
            {"question": f"Explain microservices architecture and how it would benefit {company}"}
        ]

def evaluate_answers(answers, company, role):
    """Evaluate answers and generate report"""
    try:
        print(f"📊 Evaluating {len(answers)} answers...")
        
        # Simple evaluation logic
        total_score = 0
        strengths = []
        weaknesses = []
        
        for answer in answers:
            answer_text = answer.get('answer', '')
            answer_length = len(answer_text)
            
            if answer_length > 400:
                total_score += 9
                strengths.append("Detailed and comprehensive answers")
            elif answer_length > 250:
                total_score += 7
                strengths.append("Good technical explanations")
            elif answer_length > 150:
                total_score += 6
            else:
                total_score += 4
                weaknesses.append("Could provide more detailed explanations")
        
        avg_score = total_score / len(answers) if answers else 6
        
        # Ensure we have some strengths and weaknesses
        if not strengths:
            strengths = ["Good technical foundation", "Clear problem-solving approach"]
        if not weaknesses:
            weaknesses = ["Could provide more company-specific examples"]
        
        report = {
            "overall_score": round(avg_score, 1),
            "strengths": strengths[:3],  # Limit to 3 strengths
            "weaknesses": weaknesses[:3],  # Limit to 3 weaknesses
            "topic_scores": {
                "technical_knowledge": round(avg_score, 1),
                "problem_solving": round(avg_score + 0.5, 1),
                "communication": round(avg_score - 0.3, 1),
                "code_quality": round(avg_score + 0.2, 1),
                "system_design": round(avg_score, 1)
            }
        }
        
        print(f"✅ Evaluation complete - Score: {report['overall_score']}/10")
        return report
        
    except Exception as e:
        print(f"❌ Error in evaluation: {e}")
        return {
            "overall_score": 7.0,
            "strengths": ["Completed technical interview", "Demonstrated technical knowledge"],
            "weaknesses": ["Could improve answer depth", "Need more specific examples"],
            "topic_scores": {
                "technical_knowledge": 7.0,
                "problem_solving": 7.5,
                "communication": 6.5,
                "code_quality": 7.0,
                "system_design": 7.0
            }
        }


@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/begin', methods=['POST'])
def begin_interview():
    try:
        company = request.form['company'].strip()
        role = request.form['role'].strip()
        
        if not company or not role:
            return redirect('/')
        
        print(f"🎯 Starting interview for {role} at {company}")
        
        # Generate questions
        questions = generate_questions(company, role)
        
        # Save to session
        session['company'] = company
        session['role'] = role
        session['questions'] = questions
        session['current_question'] = 0
        session['answers'] = []
        session.modified = True
        
        print(f"✅ Session saved with {len(questions)} questions")
        print(f"📝 Questions: {[q['question'][:50] + '...' for q in questions]}")
        
        return redirect('/interview')
        
    except Exception as e:
        print(f"❌ Error in begin_interview: {e}")
        return redirect('/')

@app.route('/interview', methods=['GET', 'POST'])
def interview():
    try:
        # Check if questions exist in session
        if 'questions' not in session or not session['questions']:
            print("❌ No questions found in session")
            return redirect('/')
        
        questions = session['questions']
        current_index = session.get('current_question', 0)
        
        print(f"📋 Current question index: {current_index}, Total questions: {len(questions)}")
        
        if current_index >= len(questions):
            return redirect('/report')
        
        if request.method == 'POST':
            # Save answer
            answer = request.form.get('answer', '').strip()
            if not answer:
                # If no answer provided, show error
                current_question = questions[current_index]
                progress = ((current_index) / len(questions)) * 100
                return render_template('interview.html',
                                    company=session.get('company', 'Unknown Company'),
                                    role=session.get('role', 'Unknown Role'),
                                    question=current_question['question'],
                                    question_number=current_index + 1,
                                    total_questions=len(questions),
                                    progress=progress,
                                    error="Please provide an answer before proceeding.")
            
            # Save the answer
            session['answers'].append({
                'question': questions[current_index]['question'],
                'answer': answer
            })
            session['current_question'] = current_index + 1
            session.modified = True
            
            print(f"💾 Saved answer for question {current_index + 1}")
            
            if session['current_question'] >= len(questions):
                return redirect('/report')
            else:
                return redirect('/interview')
        
        # GET request - show current question
        current_question = questions[current_index]
        progress = ((current_index) / len(questions)) * 100
        
        print(f"🎯 Displaying question {current_index + 1}: {current_question['question'][:50]}...")
        
        return render_template('interview.html',
                             company=session.get('company', 'Unknown Company'),
                             role=session.get('role', 'Unknown Role'),
                             question=current_question['question'],
                             question_number=current_index + 1,
                             total_questions=len(questions),
                             progress=progress)
                             
    except Exception as e:
        print(f"❌ Error in interview route: {e}")
        return redirect('/')

@app.route('/report')
def report():
    try:
        if 'answers' not in session or not session['answers']:
            return redirect('/')
        
        answers = session['answers']
        company = session.get('company', 'Unknown Company')
        role = session.get('role', 'Unknown Role')
        
        print(f"📊 Generating report for {len(answers)} answers")
        
        # Evaluate answers
        report_data = evaluate_answers(answers, company, role)
        
        return render_template('report.html',
                             report=report_data,
                             company=company,
                             role=role)
                             
    except Exception as e:
        print(f"❌ Error in report route: {e}")
        return redirect('/')

@app.route('/restart')
def restart():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)