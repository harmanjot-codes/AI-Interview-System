import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class InterviewCrew:
    def __init__(self):
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_key:
            raise ValueError("❌ GEMINI_API_KEY not found in .env file")
        
        print(f"🔑 Gemini API Key found: {self.gemini_key[:10]}...")
        genai.configure(api_key=self.gemini_key)
    
    def generate_questions(self, company: str, role: str) -> list:
        """Generate questions using Gemini API"""
        try:
            print(f"🤖 Generating AI questions for {role} at {company}...")
            
            # Try models in order - starting with free tier friendly ones
            model_names_to_try = [
                'gemini-2.0-flash',  # Free tier friendly
                'gemini-2.0-flash-001',
                'gemini-2.0-flash-lite',
                'gemini-2.0-flash-lite-001',
                'gemini-pro-latest',  # Fallback to latest pro
                'gemini-flash-latest'  # Fallback to latest flash
            ]
            
            for model_name in model_names_to_try:
                try:
                    print(f"🔄 Trying model: {model_name}")
                    model = genai.GenerativeModel(model_name)
                    
                    prompt = f"""
                    Generate 6-8 TECHNICAL interview questions for a {role} position at {company}.
                    Focus on practical coding, system design, and problem-solving.
                    
                    Return ONLY a JSON array where each object has a 'question' field.
                    Example: [{{"question": "Question 1"}}, {{"question": "Question 2"}}]
                    
                    Make questions specific to {company}'s technology needs.
                    Keep questions concise and technical.
                    """
                    
                    response = model.generate_content(prompt)
                    
                    if response and response.text:
                        text = response.text.strip()
                        print(f"📄 Raw response preview: {text[:100]}...")
                        
                        # Extract JSON from response
                        start_idx = text.find('[')
                        end_idx = text.rfind(']') + 1
                        
                        if start_idx != -1 and end_idx != -1:
                            json_str = text[start_idx:end_idx]
                            questions = json.loads(json_str)
                            
                            if isinstance(questions, list) and len(questions) > 0:
                                print(f"✅ Successfully generated {len(questions)} AI questions using {model_name}")
                                return questions
                    
                    print(f"❌ Model {model_name} response parsing failed")
                    
                except Exception as model_error:
                    if "quota" in str(model_error).lower() or "429" in str(model_error):
                        print(f"⏳ Quota exceeded for {model_name}, trying next model...")
                        continue
                    print(f"❌ Model {model_name} failed: {str(model_error)[:100]}...")
                    continue
            
            print("❌ All models failed due to quota or errors, using fallback")
            return self.get_fallback_questions(company, role)
            
        except Exception as e:
            print(f"❌ Gemini API Error: {e}")
            return self.get_fallback_questions(company, role)
    
    def get_fallback_questions(self, company: str, role: str) -> list:
        """Enhanced fallback questions"""
        fallback = [
            {"question": f"What are the most important programming concepts for a {role} at {company}?"},
            {"question": f"How would you design a scalable web application for {company}'s services?"},
            {"question": f"What database technologies would be most suitable for {company} and why?"},
            {"question": f"Describe your approach to solving complex technical problems at {company}'s scale"},
            {"question": f"How would you optimize application performance for {company}'s global users?"},
            {"question": f"What security practices are crucial for a {role} at {company}?"},
            {"question": f"Explain microservices architecture and how it would benefit {company}"},
            {"question": f"How would you handle data consistency in distributed systems at {company}?"}
        ]
        print("🔄 Using enhanced fallback questions")
        return fallback
    
    def evaluate_answers(self, answers: list, company: str, role: str) -> dict:
        """Evaluate answers using Gemini API"""
        try:
            print(f"📊 Evaluating {len(answers)} answers...")
            
            # Try different models for evaluation
            model_names_to_try = [
                'gemini-2.0-flash',
                'gemini-2.0-flash-lite', 
                'gemini-pro-latest'
            ]
            
            answers_text = "\n".join([
                f"Q: {a['question']}\nA: {a['answer'][:300]}...\n" for a in answers
            ])
            
            for model_name in model_names_to_try:
                try:
                    print(f"🔧 Using model for evaluation: {model_name}")
                    model = genai.GenerativeModel(model_name)
                    
                    prompt = f"""
                    Evaluate these technical interview answers for a {role} position at {company}:
                    
                    {answers_text}
                    
                    Provide a JSON evaluation report with this structure:
                    {{
                        "overall_score": 8.5,
                        "strengths": ["Good technical knowledge", "Strong problem-solving"],
                        "weaknesses": ["Could improve communication", "Need more examples"],
                        "topic_scores": {{
                            "technical_knowledge": 8,
                            "problem_solving": 9,
                            "communication": 7,
                            "code_quality": 8,
                            "system_design": 8
                        }}
                    }}
                    
                    Be constructive and fair. Score out of 10.
                    Return ONLY the JSON.
                    """
                    
                    response = model.generate_content(prompt)
                    
                    if response.text:
                        text = response.text.strip()
                        start_idx = text.find('{')
                        end_idx = text.rfind('}') + 1
                        
                        if start_idx != -1 and end_idx != -1:
                            json_str = text[start_idx:end_idx]
                            report = json.loads(json_str)
                            print(f"✅ Successfully generated AI evaluation using {model_name}")
                            return report
                    
                except Exception as model_error:
                    if "quota" in str(model_error).lower() or "429" in str(model_error):
                        print(f"⏳ Quota exceeded for {model_name}, trying next...")
                        continue
                    print(f"❌ Model {model_name} evaluation failed: {str(model_error)[:100]}...")
                    continue
            
            print("❌ All evaluation models failed, using local evaluation")
            return self.get_local_evaluation(answers, company, role)
            
        except Exception as e:
            print(f"❌ Evaluation Error: {e}")
            return self.get_local_evaluation(answers, company, role)
    
    def get_local_evaluation(self, answers: list, company: str, role: str) -> dict:
        """Local evaluation when AI fails"""
        # Simple scoring based on answer length and content
        total_chars = sum(len(str(a.get('answer', ''))) for a in answers)
        avg_length = total_chars / len(answers) if answers else 0
        
        if avg_length > 500:
            base_score = 8
        elif avg_length > 300:
            base_score = 7
        elif avg_length > 150:
            base_score = 6
        else:
            base_score = 5
            
        report = {
            "overall_score": base_score,
            "strengths": [
                f"Good understanding of technical concepts for {role}",
                "Clear problem-solving approach",
                f"Demonstrated interest in {company}"
            ],
            "weaknesses": [
                f"Could provide more {company}-specific examples",
                "Need deeper technical explanations in some areas"
            ],
            "topic_scores": {
                "technical_knowledge": base_score,
                "problem_solving": base_score + 1,
                "communication": base_score - 1,
                "code_quality": base_score,
                "system_design": base_score
            }
        }
        print("🔄 Using smart local evaluation")
        return report