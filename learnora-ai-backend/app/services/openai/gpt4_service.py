from openai import AsyncOpenAI
from typing import List, Dict, Any, Optional
from app.core.config import settings
import logging
import json

logger = logging.getLogger(__name__)

class GPT4Service:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
    
    async def generate_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> str:
        """Generate completion using GPT-4"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"GPT-4 completion error: {str(e)}")
            raise
    
    async def generate_quiz_questions(
        self,
        subject: str,
        topic: str,
        difficulty: str,
        num_questions: int,
        question_types: List[str] = ["mcq"]
    ) -> List[Dict[str, Any]]:
        """Generate quiz questions based on subject and difficulty"""
        prompt = f"""Generate {num_questions} {difficulty} level quiz questions about {subject}, specifically on the topic: {topic}.

Requirements:
- Questions should be challenging but fair for {difficulty} level
- Include real-world applications and practical scenarios
- Ensure questions test understanding, not just memorization
- Make distractors plausible but clearly incorrect

For each question, provide:
1. Question text (clear and concise)
2. Four options (A, B, C, D) for MCQ
3. Correct answer (A, B, C, or D)
4. Brief explanation (2-3 sentences explaining why the answer is correct)

Format as JSON array with this exact structure:
[
  {{
    "question": "What is the primary purpose of...",
    "options": {{
      "A": "First option",
      "B": "Second option",
      "C": "Third option",
      "D": "Fourth option"
    }},
    "correct_answer": "B",
    "explanation": "The correct answer is B because...",
    "difficulty": "{difficulty}",
    "topic": "{topic}"
  }}
]

IMPORTANT: Return ONLY the JSON array, no additional text or markdown formatting."""
        
        messages = [
            {"role": "system", "content": "You are an expert educator creating high-quality, pedagogically sound quiz questions. You always return valid JSON without any markdown formatting."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = await self.generate_completion(messages, temperature=0.8, max_tokens=3000)
            
            # Clean response to ensure valid JSON
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            questions = json.loads(response)
            return questions
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}, Response: {response}")
            raise ValueError("Failed to parse quiz questions. Please try again.")
        except Exception as e:
            logger.error(f"Quiz generation error: {str(e)}")
            raise
    
    async def solve_doubt(
        self,
        question: str,
        context: Optional[str] = None,
        subject: Optional[str] = None
    ) -> Dict[str, Any]:
        """Solve student doubt with detailed explanation"""
        system_prompt = """You are an expert tutor who:
- Explains concepts clearly and patiently
- Provides step-by-step explanations
- Uses examples and analogies when helpful
- Encourages critical thinking
- Adapts explanations to the student's level"""
        
        user_prompt = f"Question: {question}"
        if subject:
            user_prompt = f"Subject: {subject}\n{user_prompt}"
        if context:
            user_prompt = f"Context from uploaded document:\n{context}\n\n{user_prompt}"
        
        user_prompt += """

Please provide:
1. **Direct Answer**: A clear, concise answer to the question
2. **Detailed Explanation**: Step-by-step breakdown with reasoning
3. **Key Concepts**: Important concepts related to this topic
4. **Related Topics**: Suggest 2-3 related topics to explore further"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            response = await self.generate_completion(messages, temperature=0.7, max_tokens=2000)
            
            return {
                "answer": response,
                "explanation": response,
                "related_resources": []
            }
        except Exception as e:
            logger.error(f"Doubt solving error: {str(e)}")
            raise
    
    async def assess_career_profile(
        self,
        responses: Dict[str, Any],
        user_skills: List[str],
        user_interests: List[str]
    ) -> Dict[str, Any]:
        """Assess career profile and provide recommendations"""
        prompt = f"""Based on the following assessment data, provide a comprehensive career analysis:

**Assessment Responses**: {json.dumps(responses, indent=2)}
**Current Skills**: {', '.join(user_skills)}
**Interests**: {', '.join(user_interests)}

Provide a detailed analysis including:
1. **Overall Career Score** (0-100): Based on skills, interests, and responses
2. **Technical Score** (0-100): Technical aptitude and skills
3. **Soft Skills Score** (0-100): Communication, leadership, teamwork
4. **Domain Knowledge Score** (0-100): Expertise in specific domains

5. **Top 5 Recommended Career Paths**: 
   - Career title
   - Why it's a good fit (2-3 sentences)
   - Required skills to develop
   - Average salary range
   - Growth potential

6. **Strengths**: List 5-7 key strengths with brief explanations

7. **Areas for Improvement**: List 3-5 areas with actionable advice

8. **Personality Traits**: Key traits that influence career fit

9. **Career Report**: 2-3 paragraph summary with actionable next steps

Format as valid JSON with this structure:
{{
  "overall_score": 85,
  "technical_score": 80,
  "soft_skills_score": 90,
  "domain_knowledge_score": 75,
  "recommended_careers": [
    {{
      "title": "Software Engineer",
      "fit_reason": "Your strong problem-solving skills...",
      "skills_to_develop": ["System Design", "AWS"],
      "salary_range": "$80,000 - $150,000",
      "growth_potential": "High"
    }}
  ],
  "strengths": ["Problem-solving", "Analytical thinking"],
  "areas_for_improvement": ["Public speaking", "Networking"],
  "personality_traits": {{
    "analytical": true,
    "creative": true,
    "detail_oriented": true
  }},
  "report": "Based on your assessment..."
}}

Return ONLY valid JSON, no markdown formatting."""
        
        messages = [
            {"role": "system", "content": "You are an expert career counselor with deep knowledge of various industries, job markets, and career paths. You provide data-driven, actionable career guidance. You always return valid JSON."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = await self.generate_completion(messages, temperature=0.7, max_tokens=3000)
            
            # Clean response
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            analysis = json.loads(response)
            return analysis
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            raise ValueError("Failed to parse career assessment. Please try again.")
        except Exception as e:
            logger.error(f"Career assessment error: {str(e)}")
            raise
    
    async def generate_resume_content(
        self,
        user_data: Dict[str, Any],
        target_role: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate ATS-optimized resume content"""
        prompt = f"""Create professional, ATS-optimized resume content for:

**User Data**: {json.dumps(user_data, indent=2)}
**Target Role**: {target_role or 'General professional'}

Generate:
1. **Professional Summary**: Compelling 3-4 line summary highlighting key strengths
2. **Optimized Skills**: Categorized skills with industry keywords
3. **Experience Descriptions**: Achievement-focused bullet points using action verbs and quantifiable results
4. **ATS Keywords**: Industry-relevant keywords for the target role
5. **Formatting Tips**: Specific recommendations for ATS compatibility

Return as JSON:
{{
  "professional_summary": "Results-driven professional with...",
  "skills": {{
    "technical": ["Python", "AWS"],
    "soft": ["Leadership", "Communication"]
  }},
  "experience_enhancements": [
    {{
      "original": "Worked on projects",
      "optimized": "Led cross-functional team of 5 to deliver 3 critical projects, resulting in 30% efficiency improvement"
    }}
  ],
  "ats_keywords": ["keyword1", "keyword2"],
  "ats_tips": ["Use standard section headings", "Avoid tables and graphics"]
}}"""
        
        messages = [
            {"role": "system", "content": "You are a professional resume writer specializing in ATS-optimized resumes and career documents. You always return valid JSON."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = await self.generate_completion(messages, temperature=0.7, max_tokens=2000)
            
            # Clean response
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            raise ValueError("Failed to parse resume content. Please try again.")
    
    async def generate_learning_roadmap(
        self,
        goal: str,
        current_level: str,
        available_time: str
    ) -> Dict[str, Any]:
        """Generate personalized learning roadmap"""
        prompt = f"""Create a detailed, actionable learning roadmap:

**Goal**: {goal}
**Current Level**: {current_level}
**Available Time**: {available_time}

Create a comprehensive roadmap with:
1. **Milestones**: 5-8 key milestones with:
   - Title
   - Description (what you'll learn)
   - Duration estimate
   - Prerequisites
   - Success criteria

2. **Resources**: For each milestone, provide:
   - Recommended courses (with platforms)
   - Books/articles
   - Practice projects
   - Free vs paid options

3. **Timeline**: Realistic timeline based on available time
4. **Success Metrics**: How to measure progress

Return as JSON:
{{
  "title": "Web Development Roadmap",
  "total_duration_weeks": 24,
  "milestones": [
    {{
      "id": 1,
      "title": "HTML & CSS Fundamentals",
      "description": "Master the building blocks...",
      "duration_weeks": 3,
      "prerequisites": [],
      "resources": [
        {{
          "title": "freeCodeCamp HTML/CSS",
          "type": "course",
          "url": "https://...",
          "cost": "free"
        }}
      ],
      "projects": ["Build a portfolio website"],
      "success_criteria": ["Can build responsive layouts", "Understand CSS Grid"]
    }}
  ],
  "prerequisites": ["Basic computer skills"],
  "success_metrics": ["Complete all milestone projects", "Build 5 portfolio projects"]
}}"""
        
        messages = [
            {"role": "system", "content": "You are an expert learning designer creating effective, practical learning paths. You always return valid JSON."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = await self.generate_completion(messages, temperature=0.7, max_tokens=3000)
            
            # Clean response
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            raise ValueError("Failed to parse learning roadmap. Please try again.")

gpt4_service = GPT4Service()