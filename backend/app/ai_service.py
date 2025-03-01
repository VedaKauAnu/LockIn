import os
import openai
from flask import current_app

class AIService:
    """Service class for AI-powered features using OpenAI API."""
    
    def __init__(self):
        # Initialize with OpenAI API key
        openai.api_key = os.environ.get('OPENAI_API_KEY')
        if not openai.api_key:
            raise ValueError("OpenAI API key is required")
    
    def generate_notes(self, course_title, topic, detail_level="medium"):
        """Generate study notes for a given topic."""
        # Define token limits based on detail level
        max_tokens = {
            "brief": 500,
            "medium": 1000,
            "detailed": 2000
        }.get(detail_level, 1000)
        
        prompt = f"""
        Create organized study notes for a college course.
        
        Course: {course_title}
        Topic: {topic}
        
        Include:
        1. Key concepts and definitions
        2. Important principles or theories
        3. Relevant examples
        4. Summary of main points
        
        Use clear headings and bullet points where appropriate.
        """
        
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].text.strip()
        except Exception as e:
            current_app.logger.error(f"OpenAI API error: {str(e)}")
            return f"Failed to generate notes. Error: {str(e)}"
    
    def generate_practice_questions(self, course_title, topic, count=5, difficulty="mixed"):
        """Generate practice questions for a given topic."""
        difficulty_prompt = ""
        if difficulty != "mixed":
            difficulty_prompt = f"Make all questions {difficulty} difficulty level."
        
        prompt = f"""
        Create {count} practice questions for a college course.
        
        Course: {course_title}
        Topic: {topic}
        
        For each question:
        1. Write a clear question
        2. Provide a comprehensive answer
        3. Specify difficulty (easy, medium, or hard)
        
        Format as JSON with this structure:
        [
            {{
                "question": "Question text here?",
                "answer": "Answer text here.",
                "difficulty": "medium"
            }},
            ...
        ]
        
        {difficulty_prompt}
        """
        
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=2000,
                temperature=0.7
            )
            
            # Note: In production, you'd want to properly parse the JSON
            # This is simplified for demonstration
            return response.choices[0].text.strip()
        except Exception as e:
            current_app.logger.error(f"OpenAI API error: {str(e)}")
            return f"Failed to generate questions. Error: {str(e)}"
    
    def generate_test_strategies(self, test_type, student_problems=None):
        """Generate test-taking strategies."""
        problems_prompt = ""
        if student_problems:
            problems_prompt = f"The student has mentioned these specific challenges: {', '.join(student_problems)}."
        
        prompt = f"""
        Create personalized test-taking strategies for a {test_type} exam.
        
        {problems_prompt}
        
        Include:
        1. Before the test preparation tips
        2. During the test strategies
        3. Time management techniques
        4. Anxiety management strategies
        5. Specific strategies for {test_type} exams
        
        Format with clear sections and actionable advice.
        """
        
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=1500,
                temperature=0.7
            )
            return response.choices[0].text.strip()
        except Exception as e:
            current_app.logger.error(f"OpenAI API error: {str(e)}")
            return f"Failed to generate test strategies. Error: {str(e)}"