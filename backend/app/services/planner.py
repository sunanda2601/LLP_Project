"""
===========================================================
LANGUAGE LEARNING PAL PLAN MODEL
Version: 2.0

Purpose:
- Represents a personalized learning plan
- Used by Planner Engine
- Supports roadmap generation
- Supports progress tracking
- Supports recommendations

===========================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict


@dataclass
class Plan:

    # =====================================================
    # BASIC INFORMATION
    # =====================================================

    title: str

    goal: str

    duration: str

    difficulty: str

    # =====================================================
    # PLAN CONTENT
    # =====================================================

    steps: List[str] = field(default_factory=list)

    recommendations: List[str] = field(default_factory=list)

    milestones: List[str] = field(default_factory=list)

    weeks: Dict = field(default_factory=dict)

    # =====================================================
    # PROGRESS TRACKING
    # =====================================================

    completed_steps: int = 0

    total_steps: int = 0

    progress_percentage: float = 0.0

    # =====================================================
    # PERSONALIZATION
    # =====================================================

    weak_areas: List[str] = field(default_factory=list)

    strong_areas: List[str] = field(default_factory=list)

    learning_level: str = ""

    # =====================================================
    # METADATA
    # =====================================================

    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    updated_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    # =====================================================
    # HELPER METHODS
    # =====================================================

    def calculate_progress(self) -> float:
        """
        Calculate plan completion percentage.
        """

        if self.total_steps == 0:
            return 0.0

        self.progress_percentage = round(
            (self.completed_steps / self.total_steps) * 100,
            2
        )

        return self.progress_percentage

    def mark_step_completed(self):
        """
        Mark one step as completed.
        """

        if self.completed_steps < self.total_steps:
            self.completed_steps += 1

        self.calculate_progress()

        self.updated_at = datetime.utcnow().isoformat()

    def add_step(self, step: str):
        """
        Add new learning step.
        """

        self.steps.append(step)

        self.total_steps = len(self.steps)

        self.updated_at = datetime.utcnow().isoformat()

    def add_recommendation(self, recommendation: str):
        """
        Add personalized recommendation.
        """

        self.recommendations.append(recommendation)

        self.updated_at = datetime.utcnow().isoformat()

    def add_milestone(self, milestone: str):
        """
        Add milestone to roadmap.
        """

        self.milestones.append(milestone)

        self.updated_at = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict:
        """
        Convert Plan object into dictionary.
        Useful for APIs and JSON responses.
        """

        return {
            "title": self.title,
            "goal": self.goal,
            "duration": self.duration,
            "difficulty": self.difficulty,
            "steps": self.steps,
            "weeks": self.weeks,
            "recommendations": self.recommendations,
            "milestones": self.milestones,
            "completed_steps": self.completed_steps,
            "total_steps": self.total_steps,
            "progress_percentage": self.progress_percentage,
            "weak_areas": self.weak_areas,
            "strong_areas": self.strong_areas,
            "learning_level": self.learning_level,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


    @staticmethod
    def _get_dynamic_curriculum(day_num: int, goal_lower: str, vocab_words: list) -> tuple:
        # Default fallback values
        objective = f"Day {day_num} Learning Plan"
        tasks = [f"Practice grammar with vocabulary: {', '.join(vocab_words)}.", "Complete daily speaking drill.", "Complete daily assessment checklist."]
        assessment = "Daily 5-minute reflection"
        expected_outcome = "Improve overall comprehension and fluency"

        if "placement" in goal_lower or "interview" in goal_lower:
            # Placements curriculum map for Days 8-30
            placements_map = {
                8: ("Professional Vocabulary & Active Achievements", [
                    f"Learn 5 professional vocabulary words: {', '.join(vocab_words)}.",
                    "Practice describing your key college projects using action verbs.",
                    "Grammar Focus: Correct sentence tenses in resume summaries."
                ], "Test on vocabulary meanings", "Understand professional phrasing"),
                9: ("Technical Concept Explanation", [
                    f"Practice saying: {', '.join(vocab_words)}.",
                    "Explain a technical database or programming concept in simple English.",
                    "Speaking Focus: Answer 'What tech stacks do you prefer?'"
                ], "Record a 1-minute explanation and self-correct", "Communicate technical concepts clearly"),
                10: ("Professional Email Etiquette", [
                    f"Review terms: {', '.join(vocab_words)}.",
                    "Draft a professional email requesting mock interview feedback.",
                    "Grammar Focus: Proper passive voice in corporate emails."
                ], "Review passive voice guidelines", "Write clear professional emails"),
                11: ("Elevator Pitch Preparation", [
                    f"Practice pronunciation of: {', '.join(vocab_words)}.",
                    "Deliver a 30-second elevator pitch about your skills.",
                    "Speaking Focus: Avoid fillers like 'um' and 'like'."
                ], "Self-assess pitch timing and stress", "Smooth elevator pitch delivery"),
                12: ("Group Discussion Vocabulary", [
                    f"Learn 5 terms: {', '.join(vocab_words)}.",
                    "Practice expressions of agreement/disagreement in formal meetings.",
                    "Speaking Focus: Deliver opinions with polite modifiers."
                ], "Identify 3 polite disagreement structures", "Participate in formal discussions"),
                13: ("Resume Intonation & Presentation", [
                    f"Pronounce clearly: {', '.join(vocab_words)}.",
                    "Read your resume profile aloud focusing on word stress.",
                    "Grammar Focus: Master active verb placement in resume points."
                ], "Submit a 1-minute resume pitch", "Improve resume pitch confidence"),
                14: ("Week 2 Review & Assessment", [
                    f"Review Week 2 vocabulary: {', '.join(vocab_words)}.",
                    "Complete the mid-term placements written challenge.",
                    "Speaking Focus: Complete full career profile overview."
                ], "Placements vocabulary test", "Verify Week 2 vocabulary retention"),
                
                # Week 3
                15: ("STAR Method: Situation", [
                    f"Practice vocabulary: {', '.join(vocab_words)}.",
                    "Describe a project setting and team size clearly.",
                    "Grammar Focus: Setting the background using past continuous tense."
                ], "Verify situation paragraph", "Establish clear background contexts"),
                16: ("STAR Method: Task & Action", [
                    f"Learn 5 action verbs: {', '.join(vocab_words)}.",
                    "Explain your exact contribution to a group project.",
                    "Speaking Focus: Emphasize personal ownership with 'I achieved' rather than 'We did'."
                ], "Write down 3 action statements", "Detail individual contributions"),
                17: ("STAR Method: Result", [
                    f"Use outcome metrics: {', '.join(vocab_words)}.",
                    "Explain the metrics and results of your project.",
                    "Grammar Focus: Express results using cause-and-effect connectors."
                ], "Identify project performance metrics", "Quantify project outcomes"),
                18: ("Behavioral Qs: Strengths & Weaknesses", [
                    f"Practice pronunciation of: {', '.join(vocab_words)}.",
                    "Answer behavioral question: 'What is your greatest weakness?'",
                    "Speaking Focus: Frame weaknesses constructively as learning areas."
                ], "Deliver weakness response under 1 minute", "Handle critical personal evaluation"),
                19: ("Behavioral Qs: Teamwork & Conflicts", [
                    f"Learn cooperation terms: {', '.join(vocab_words)}.",
                    "Explain how you resolved a team conflict in college.",
                    "Grammar Focus: Correct direct/indirect speech syntax."
                ], "Complete conflict resolution outline", "Demonstrate collaborative skills"),
                20: ("Verbal Clarity & Intonation", [
                    f"Pronounce with stress: {', '.join(vocab_words)}.",
                    "Record yourself speaking with rising/falling intonation.",
                    "Speaking Focus: Pause before major conclusions for verbal emphasis."
                ], "Pitch comparison recording", "Speak with professional rhythm"),
                21: ("Week 3 HR Review Mock", [
                    f"Review behaviorals: {', '.join(vocab_words)}.",
                    "Answer 5 common HR placement questions.",
                    "Grammar Focus: Polish overall consistency of past and present tenses."
                ], "HR mock evaluation", "Ensure robust interview responses"),

                # Week 4
                22: ("Technical Introduction Review", [
                    f"Summarize database skills using: {', '.join(vocab_words)}.",
                    "Deliver your technical background introduction.",
                    "Speaking Focus: Keep introduction concise (90 seconds)."
                ], "Evaluate technical intro clarity", "Summarize technical stack effectively"),
                23: ("STAR Methodology Integration", [
                    f"Practice project narrative using: {', '.join(vocab_words)}.",
                    "Combine Situation, Task, Action, and Result into one project story.",
                    "Grammar Focus: Correct transitional flow between past events."
                ], "Assess project story flow", "Connect narrative steps seamlessly"),
                24: ("Active Listening & Scenario Queries", [
                    f"Listen to complex terms: {', '.join(vocab_words)}.",
                    "Respond to an unexpected scenario question in real-time.",
                    "Speaking Focus: Clarify questions politely before answering."
                ], "Reply to scenario problem challenge", "Manage surprise situational prompts"),
                25: ("Asking the Interviewer Questions", [
                    f"Learn engagement terms: {', '.join(vocab_words)}.",
                    "Draft 3 questions to ask your placement interviewer.",
                    "Speaking Focus: Voice tone control during inquiry."
                ], "Submit interview questions list", "Show proactive interest"),
                26: ("Speech Stress & Pacing", [
                    f"Practice pauses on: {', '.join(vocab_words)}.",
                    "Deliver a 2-minute project summary with slow, clear pacing.",
                    "Speaking Focus: Reduce speech rate under pressure."
                ], "Self-pacing review check", "Maintain calm delivery speed"),
                27: ("Placements Grammar Polish", [
                    f"Review complex structures: {', '.join(vocab_words)}.",
                    "Correct 10 common placement interview grammar errors.",
                    "Grammar Focus: Conditional tenses ('If I were...')."
                ], "Complete conditional grammar test", "Avoid syntax errors under stress"),
                28: ("Vocabulary Speed Drills", [
                    f"Replace synonyms of: {', '.join(vocab_words)}.",
                    "Answer questions substituting basic words with professional vocabulary.",
                    "Speaking Focus: Demonstrate wide lexical resource range."
                ], "Synonym substitution quiz", "Use varied vocabulary forms"),
                29: ("Final Placements Mock Drill", [
                    f"Practice pronunciation of: {', '.join(vocab_words)}.",
                    "Participate in a full simulated placement interview.",
                    "Speaking Focus: Integrate pitch, STAR, and behaviorals."
                ], "Evaluate placement mock scorecard", "Complete full simulation trial"),
                30: ("Final Placements Evaluation", [
                    f"Verify final placement words: {', '.join(vocab_words)}.",
                    "Deliver final placement assessment speech.",
                    "Grammar Focus: Absolute syntactic accuracy."
                ], "Day 30 Final Assessment Exam", "Attain placement-readiness certification")
            }
            if day_num in placements_map:
                objective, tasks, assessment, expected_outcome = placements_map[day_num]
        
        elif "ielts" in goal_lower:
            # IELTS curriculum map for Days 8-30
            ielts_map = {
                8: ("Academic Writing Task 1 Graph Trends", [
                    f"Learn 5 trends terms: {', '.join(vocab_words)}.",
                    "Analyze a double-line graph and write the overview.",
                    "Grammar Focus: Using passive voice to describe data changes."
                ], "Submit 150-word report overview", "Paraphrase complex graph patterns"),
                9: ("Speaking Part 2 Cue-card Delivery", [
                    f"Pronounce cue-card vocabulary: {', '.join(vocab_words)}.",
                    "Practice speaking for 2 minutes continuously on a personal event.",
                    "Speaking Focus: Use transitions like 'Initially' and 'Eventually'."
                ], "Speak for 2 mins with timer", "Deliver structured speaking responses"),
                10: ("Academic Writing Task 2 Essay Structuring", [
                    f"Learn essay vocabulary: {', '.join(vocab_words)}.",
                    "Outline a agree/disagree essay on education.",
                    "Grammar Focus: Subordinate clauses for complex sentences."
                ], "Draft introduction & thesis statements", "Formulate clear essay stances"),
                11: ("Listening Distractors & Spelling", [
                    f"Practice spelling words: {', '.join(vocab_words)}.",
                    "Identify listening distractors in section 1 mock audio.",
                    "Speaking Focus: Spell difficult names and numbers aloud."
                ], "Spelling accuracy check", "Listen and capture specific details"),
                12: ("Reading True/False/Not Given", [
                    f"Identify synonyms for: {', '.join(vocab_words)}.",
                    "Read an academic passage and answer 5 comprehension questions.",
                    "Reading Focus: Locate keywords and identify subtle differences."
                ], "Comprehension correctness check", "Differentiate fact from assumptions"),
                13: ("Speaking Part 3 Abstract Discussion", [
                    f"Use abstract terms: {', '.join(vocab_words)}.",
                    "Answer 3 discussion questions about societal trends.",
                    "Speaking Focus: Structure responses with statement-reason-example."
                ], "Abstract arguments recording", "Discuss societal issues maturely"),
                14: ("Week 2 Review & Assessment", [
                    f"Review Week 2 vocabulary: {', '.join(vocab_words)}.",
                    "Complete a timed Writing Task 1 overview.",
                    "Speaking Focus: Deliver a full 2-minute cue card."
                ], "Mid-term vocabulary & writing test", "Verify writing and speaking flow"),
                
                # Week 3
                15: ("Writing Task 1 Process & Flowcharts", [
                    f"Use sequential connectors: {', '.join(vocab_words)}.",
                    "Describe a manufacturing process chart.",
                    "Grammar Focus: Present passive tense for process stages."
                ], "Flowchart description paragraph", "Link process stages logically"),
                16: ("Writing Task 2 Discussion Essays", [
                    f"Learn debate vocabulary: {', '.join(vocab_words)}.",
                    "Outline a 'Discuss both views and give your opinion' essay.",
                    "Grammar Focus: Connectors of concession ('Although', 'Whereas')."
                ], "Draft two balanced body paragraphs", "Present balanced viewpoints"),
                17: ("Cohesive Devices & Essay Flow", [
                    f"Practice linking words: {', '.join(vocab_words)}.",
                    "Rewrite a paragraph replacing repetitive words with cohesive devices.",
                    "Grammar Focus: Relative clauses for descriptive fluency."
                ], "Cohesion score review", "Smooth paragraph transitions"),
                18: ("Speaking Part 2 Cue-card Objects/Events", [
                    f"Pronounce adjectives: {', '.join(vocab_words)}.",
                    "Speak for 2 minutes on a memorable event you attended.",
                    "Speaking Focus: Adjective variety to expand lexical score."
                ], "Timed cue card assessment", "Speak descriptively and fluently"),
                19: ("Listening Multiple Choice & Map Labeling", [
                    f"Learn spatial terms: {', '.join(vocab_words)}.",
                    "Answer 5 map labeling questions from a listening passage.",
                    "Listening Focus: Follow directions and ignore distractors."
                ], "Map coordinates checklist", "Map audio cues to spatial layouts"),
                20: ("Reading Matching Headings", [
                    f"Scan paragraph terms: {', '.join(vocab_words)}.",
                    "Read a 3-paragraph section and match headings.",
                    "Reading Focus: Summarize paragraph main ideas in 3 words."
                ], "Heading matcher scorecard", "Extract paragraph themes quickly"),
                21: ("Week 3 Timed IELTS Mock", [
                    f"Review cohesive terms: {', '.join(vocab_words)}.",
                    "Write a full 250-word essay on technology trends.",
                    "Speaking Focus: Answer 5 abstract Part 3 questions."
                ], "Essay and speaking band scoring", "Complete full writing task under limits"),

                # Week 4
                22: ("Writing Task 1 Timed Challenge", [
                    f"Utilize comparison words: {', '.join(vocab_words)}.",
                    "Complete a timed Writing Task 1 bar chart description (20 mins).",
                    "Grammar Focus: Complex comparisons and prepositions."
                ], "Task 1 timed review", "Describe stats under time pressure"),
                23: ("Writing Task 2 Timed Challenge", [
                    f"Integrate academic words: {', '.join(vocab_words)}.",
                    "Complete a timed Writing Task 2 essay (40 mins).",
                    "Grammar Focus: Relative clauses and conditional clauses."
                ], "Task 2 essay band evaluation", "Write structured essay under limits"),
                24: ("Speaking Parts 1-3 Simulation", [
                    f"Practice pronunciation of: {', '.join(vocab_words)}.",
                    "Simulate a full IELTS speaking test with the agent.",
                    "Speaking Focus: Maintain fluency and correct intonation."
                ], "Speaking mock band scoring", "Complete full spoken interview simulation"),
                25: ("Lexical Resource Expansion", [
                    f"Review synonym pools of: {', '.join(vocab_words)}.",
                    "Rewrite basic sentences replacing simple verbs with academic synonyms.",
                    "Speaking Focus: Avoid repeating vocabulary words."
                ], "Academic synonym assessment", "Vary word choices seamlessly"),
                26: ("Intonation & Pronunciation Polish", [
                    f"Stress key syllables in: {', '.join(vocab_words)}.",
                    "Read IELTS cue card responses with correct word stress and links.",
                    "Speaking Focus: Natural rising and falling pitch structures."
                ], "Intonation accuracy check", "Speak with native-like stress patterns"),
                27: ("Grammar Range & Accuracy Test", [
                    f"Structure conditionals on: {', '.join(vocab_words)}.",
                    "Correct grammatical errors in a complex academic passage.",
                    "Grammar Focus: Inversion and conditional structures."
                ], "Grammatical accuracy quiz", "Minimize basic syntax errors in essays"),
                28: ("Speed Reading Skim-Scan Drills", [
                    f"Locate keywords: {', '.join(vocab_words)}.",
                    "Locate 10 specific terms in a 1000-word text under 3 minutes.",
                    "Reading Focus: Rapid synonym mapping."
                ], "Speed reading scoreboard", "Find answers in text rapidly"),
                29: ("IELTS Practice Exam Simulation", [
                    f"Pronounce key terms: {', '.join(vocab_words)}.",
                    "Complete a full mock IELTS paper (Reading & Writing sections).",
                    "Speaking Focus: Polish abstract speech structures."
                ], "Mock examination grade card", "Validate readiness for final evaluation"),
                30: ("Final IELTS Band Assessment", [
                    f"Demonstrate final IELTS vocabulary: {', '.join(vocab_words)}.",
                    "Deliver final academic speaking and writing essays.",
                    "Grammar Focus: Clear complex structures."
                ], "Day 30 Final IELTS Assessment", "Attain final band placement scorecard")
            }
            if day_num in ielts_map:
                objective, tasks, assessment, expected_outcome = ielts_map[day_num]
        
        else:
            # Communication curriculum map for Days 8-30
            comm_map = {
                8: ("Casual Greetings & Chit-chat", [
                    f"Learn 5 casual terms: {', '.join(vocab_words)}.",
                    "Practice greeting a neighbor and making small talk about weather.",
                    "Grammar Focus: Correct subject-verb patterns in casual chat."
                ], "Roleplay casual greetings", "Initiate friendly dialogues naturally"),
                9: ("Expressing Likes, Dislikes & Hobbies", [
                    f"Pronounce likes vocabulary: {', '.join(vocab_words)}.",
                    "Describe your favorite food or restaurant to a friend.",
                    "Speaking Focus: Express excitement using pitch variety."
                ], "Deliver likes summary (1 min)", "Share preferences comfortably"),
                10: ("Invitations & Making Plans", [
                    f"Use arrangements vocabulary: {', '.join(vocab_words)}.",
                    "Invite a friend out for dinner or movies in a spoken dialog.",
                    "Grammar Focus: Using present continuous for future social events."
                ], "Verify spoken invitation details", "Schedule social plans in English"),
                11: ("Ordering Food & Directions", [
                    f"Learn request terms: {', '.join(vocab_words)}.",
                    "Simulate ordering a meal at a restaurant and asking for directions.",
                    "Speaking Focus: Use polite rising intonation for requests."
                ], "Food ordering roleplay challenge", "Navigate public spaces and services"),
                12: ("Describing Hobbies & Rituals", [
                    f"Learn descriptions: {', '.join(vocab_words)}.",
                    "Detail your weekly hobby routine using frequency adverbs.",
                    "Speaking Focus: Smooth speech rate during lists."
                ], "Hobby review recording", "Discuss interest areas with structure"),
                13: ("Colloquial Idioms & Expressions", [
                    f"Review idioms: {', '.join(vocab_words)}.",
                    "Explain 3 common idioms ('piece of cake', 'break a leg') with examples.",
                    "Grammar Focus: Connect idioms grammatically in conversation."
                ], "Idiom usage check", "Understand natural colloquial expressions"),
                14: ("Week 2 Review & Dialogue Practice", [
                    f"Review Week 2 vocabulary: {', '.join(vocab_words)}.",
                    "Engage in a 2-minute dialogue covering likes, routines, and plans.",
                    "Speaking Focus: Speak without pausing for more than 3 seconds."
                ], "Social dialogue assessment", "Demonstrate intermediate social fluency"),

                # Week 3
                15: ("Polite Agreement & Disagreement", [
                    f"Use disagreement terms: {', '.join(vocab_words)}.",
                    "Express disagreement on a controversial topic politely.",
                    "Grammar Focus: Softening connectors ('I see your point, but...')."
                ], "Record polite disagreement response", "Engage in debates respectfully"),
                16: ("Sharing Stories & Past Events", [
                    f"Learn narrative terms: {', '.join(vocab_words)}.",
                    "Tell a 2-minute story about a funny memory from childhood.",
                    "Speaking Focus: Chronological sequencing words ('First', 'Next')."
                ], "Story timeline check", "Retell life stories chronologically"),
                17: ("Connected Speech & Syllable Stress", [
                    f"Pronounce multi-syllable terms: {', '.join(vocab_words)}.",
                    "Read a list of phrases showing word linking ('want to' -> 'wanna').",
                    "Speaking Focus: Smooth vocal transitions between words."
                ], "Phonetic stress test", "Speak with smooth connected flow"),
                18: ("Intonation & Emotion in Speech", [
                    f"Express emotions with: {', '.join(vocab_words)}.",
                    "Read a short script expressing joy, surprise, and sadness.",
                    "Speaking Focus: Alter pitch to reflect different emotions."
                ], "Emotional script recording", "Convey feelings through voice tone"),
                19: ("Telephone Conversation Etiquette", [
                    f"Learn phone phrasing: {', '.join(vocab_words)}.",
                    "Simulate calling a store to ask about opening hours.",
                    "Speaking Focus: Speak slowly and enunciate clearly."
                ], "Phone calling simulation checklist", "Handle phone calls with confidence"),
                20: ("Clarification & Asking for Explanation", [
                    f"Learn clarification words: {', '.join(vocab_words)}.",
                    "Practice asking someone to repeat a fast instruction politely.",
                    "Speaking Focus: Use questions like 'Could you elaborate?'"
                ], "Clarification request audit", "Resolve verbal misunderstandings"),
                21: ("Week 3 Conversational Assessment", [
                    f"Review conversation terms: {', '.join(vocab_words)}.",
                    "Complete a timed dialog discussing future travel arrangements.",
                    "Grammar Focus: Review modal verbs for advice."
                ], "Conversational scoring matrix", "Validate spoken expression metrics"),

                # Week 4
                22: ("Workplace Communication & Greetings", [
                    f"Learn office vocabulary: {', '.join(vocab_words)}.",
                    "Greet a colleague and explain your current task.",
                    "Speaking Focus: Use formal greetings over casual ones."
                ], "Workplace intro audit", "Navigate office conversation styles"),
                23: ("Spontaneous Dialogue & Current Affairs", [
                    f"Discuss news terms: {', '.join(vocab_words)}.",
                    "Give a 1-minute opinion on a recent technology news story.",
                    "Speaking Focus: Maintain fluent sentence structure."
                ], "Spontaneous speech check", "Discuss current events fluently"),
                24: ("Travel, Shopping & Hotel Scenarios", [
                    f"Practice travel terms: {', '.join(vocab_words)}.",
                    "Simulate checking into a hotel and reporting a room issue.",
                    "Speaking Focus: Assertive yet polite request structure."
                ], "Hotel check-in review", "Manage common travel difficulties"),
                25: ("Giving Advice & Making Suggestions", [
                    f"Learn suggestion terms: {', '.join(vocab_words)}.",
                    "Advise a friend on how to study for exams.",
                    "Grammar Focus: Using 'should', 'ought to', 'had better'."
                ], "Advice paragraph check", "Formulate helpful recommendations"),
                26: ("Active Listening & Backchanneling", [
                    f"Review listening responses: {', '.join(vocab_words)}.",
                    "Practice conversations using 'Is that so?', 'Aha', 'Right'.",
                    "Speaking Focus: Respond quickly to audio statements."
                ], "Backchannel response count", "Show active listening non-verbally"),
                27: ("Connected Speech & Blending Words", [
                    f"Practice blending: {', '.join(vocab_words)}.",
                    "Read dialogue scripts showing word blending rules.",
                    "Speaking Focus: Avoid mechanical, choppy word splits."
                ], "Word blending scorecard", "Acquire natural conversational links"),
                28: ("Adjective Variety & Expressiveness", [
                    f"Use descriptive words: {', '.join(vocab_words)}.",
                    "Describe a beautiful scenery substituting simple adjectives with vivid ones.",
                    "Speaking Focus: Expressive vocabulary ranges."
                ], "Adjective variety check", "Speak with colorful descriptors"),
                29: ("Conversational Speed Drill", [
                    f"Practice quick reactions: {', '.join(vocab_words)}.",
                    "Deliver rapid responses to 5 fast dialogue questions.",
                    "Speaking Focus: Speed and spontaneity."
                ], "Speed drill result evaluation", "Reduce hesitation times"),
                30: ("Final Conversation Evaluation", [
                    f"Verify final social words: {', '.join(vocab_words)}.",
                    "Deliver final spoken social dialog.",
                    "Grammar Focus: Flawless everyday speech syntax."
                ], "Day 30 Final Conversational Assessment", "Acquire conversational excellence card")
            }
            if day_num in comm_map:
                objective, tasks, assessment, expected_outcome = comm_map[day_num]
                
        return objective, tasks, assessment, expected_outcome

class Planner:

    @staticmethod
    def generate_learning_plan(
        user_id: str,
        goal: str,
        duration: str,
        level: str,
        weak_areas: List[str] = None
    ) -> Plan:
        """
        Generate a personalized learning plan.
        """
        goal = goal or "Fluent English"
        duration = duration or "30 Days"
        level = level or "Beginner"
        weak_areas = weak_areas or []

        goal_lower = goal.lower()
        wa_desc = f" focusing heavily on {', '.join(weak_areas)}" if weak_areas else ""

        if "ielts" in goal_lower:
            steps = [
                f"Week 1: IELTS Band 7+ Academic Reading & Writing task structures ({level}){wa_desc if 'Grammar' in weak_areas or 'Vocabulary' in weak_areas else ''}",
                f"Week 2: Academic Vocabulary development & IELTS Speaking part 1 & 2 practice{wa_desc if 'Pronunciation' in weak_areas or 'Conversation' in weak_areas else ''}",
                "Week 3: Guided listening exams & Writing Task 2 essays",
                "Week 4: Full IELTS Speaking Mock Exams & final review"
            ]
        elif "placement" in goal_lower or "interview" in goal_lower:
            steps = [
                f"Week 1: Technical resume vocabulary & self-introduction pitch ({level}){wa_desc if 'Grammar' in weak_areas or 'Vocabulary' in weak_areas else ''}",
                f"Week 2: STAR interview methodology and structural speaking drills{wa_desc if 'Pronunciation' in weak_areas or 'Conversation' in weak_areas else ''}",
                "Week 3: HR Interview Communication & Mock Placements tests",
                "Week 4: Mock Interviews & final review"
            ]
        else:
            steps = [
                f"Week 1: Daily conversational active listening & spoken grammar basics ({level}){wa_desc if 'Grammar' in weak_areas or 'Vocabulary' in weak_areas else ''}",
                f"Week 2: Spontaneous dialogue building and colloquial idioms{wa_desc if 'Pronunciation' in weak_areas or 'Conversation' in weak_areas else ''}",
                "Week 3: Pronunciation clarity & sentence intonation correction",
                "Week 4: Spoken confidence mock tasks and real-world chats"
            ]

        recommendations = [
            f"Set aside 15 minutes daily for {goal} practice.",
            "Complete the daily Word of the Day challenges."
        ]
        for wa in weak_areas:
            if wa == "Grammar":
                recommendations.append("Do 5 grammar corrections in the chat daily.")
            elif wa == "Vocabulary":
                recommendations.append("Use the synonym and antonym search tool to broaden expression.")
            elif wa == "Pronunciation":
                recommendations.append("Use the pronunciation helper to split hard words into syllables.")
            elif wa == "Conversation":
                recommendations.append("Start a topic-based chat session daily and review agent feedback.")

        milestones = [
            "Complete Weekly Progress Checks",
            f"Achieve basic comfort discussing {goal} scenarios",
            "Pass the final learning plan assessment"
        ]

        # Word pools for vocabulary tasks
        placement_vocab = [
            {"word": "Opportunity", "meaning": "A time or set of circumstances that makes it possible to do something.", "example": "This job placement is a great opportunity for my career."},
            {"word": "Professional", "meaning": "Relating to or characteristic of a useful or competent worker.", "example": "Maintaining a professional tone in interviews is extremely important."},
            {"word": "Confidence", "meaning": "A feeling of self-assurance arising from one's appreciation of one's own abilities.", "example": "Mock interviews help build confidence before the placement drive."},
            {"word": "Responsibility", "meaning": "The state or fact of having a duty to deal with something.", "example": "A software engineer has the responsibility to write clean, tested code."},
            {"word": "Achievement", "meaning": "A thing done successfully, typically by effort, courage, or skill.", "example": "Winning the hackathon was my biggest college achievement."},
            {"word": "Collaboration", "meaning": "The action of working with someone to produce or create something.", "example": "Good collaboration skills are highly valued during group discussions."},
            {"word": "Innovative", "meaning": "Featuring new methods; advanced and original.", "example": "The company is looking for innovative developers to solve complex problems."},
            {"word": "Strategy", "meaning": "A plan of action or policy designed to achieve a major or overall aim.", "example": "We need a clear strategy to crack the technical rounds."},
            {"word": "Leadership", "meaning": "The action of leading a group of people or an organization.", "example": "He demonstrated leadership by coordinating the college project."},
            {"word": "Efficiency", "meaning": "The state or quality of being efficient and productive.", "example": "Writing optimized code improves program efficiency significantly."},
            {"word": "Adaptability", "meaning": "The quality of being able to adjust to new conditions.", "example": "Adaptability is key when working with shifting project requirements."},
            {"word": "Punctuality", "meaning": "The fact or quality of being on time.", "example": "Punctuality shows respect for the interviewer's schedule."},
            {"word": "Proactive", "meaning": "Creating or controlling a situation by causing something to happen rather than responding to it.", "example": "A proactive developer learns new tools before they are required."},
            {"word": "Analytical", "meaning": "Relating to or using analysis or logical reasoning.", "example": "Interviews often test your analytical thinking with puzzles."},
            {"word": "Competency", "meaning": "The ability to do something successfully or efficiently.", "example": "Coding competency is the most critical factor for placements."},
            {"word": "Negotiation", "meaning": "Discussion aimed at reaching an agreement.", "example": "Salary negotiation is a common part of the final HR round."},
            {"word": "Dedication", "meaning": "The quality of being dedicated or committed to a task or purpose.", "example": "Cracking top-tier placements requires continuous dedication."},
            {"word": "Synergy", "meaning": "The interaction or cooperation of two or more agents to produce a combined effect greater than the sum of their separate effects.", "example": "Our team synergy helped us complete the project ahead of schedule."},
            {"word": "Resolution", "meaning": "The action of solving a problem, dispute, or contentious matter.", "example": "Conflict resolution is an important soft skill for engineers."},
            {"word": "Objective", "meaning": "A thing aimed at or sought; a goal.", "example": "My immediate objective is to secure a software engineering role."},
            {"word": "Milestone", "meaning": "An action or event marking a significant change or stage in development.", "example": "Completing my project draft was a major milestone."},
            {"word": "Contribution", "meaning": "A gift or payment to a common fund or collection.", "example": "Your individual contribution to the team project will be evaluated."},
            {"word": "Aspiration", "meaning": "A hope or ambition of achieving something.", "example": "My career aspiration is to become a software architect."},
            {"word": "Expertise", "meaning": "Expert skill or knowledge in a particular field.", "example": "She has deep technical expertise in database management systems."},
            {"word": "Capability", "meaning": "Power or ability to do something.", "example": "This tool expands our capability to process large amounts of text data."},
            {"word": "Initiative", "meaning": "The ability to assess and initiate things independently.", "example": "Taking the initiative to learn new backend structures shows great promise."},
            {"word": "Perseverance", "meaning": "Persistence in doing something despite difficulty or delay in achieving success.", "example": "With hard work and perseverance, you will clear the interview."},
            {"word": "Performance", "meaning": "An act of performance or quality of presentation.", "example": "The manager praised his stellar performance in the project."},
            {"word": "Feedback", "meaning": "Information about reactions to a product, a person's performance of a task, etc.", "example": "Constructive feedback from mock interviews is invaluable."},
            {"word": "Evaluation", "meaning": "The making of a judgment about the amount, number, or value of something.", "example": "The HR manager conducts an evaluation of communication skills."}
        ]

        ielts_vocab = [
            {"word": "Analyze", "meaning": "Examine methodically and in detail.", "example": "You need to analyze the line graph carefully in Writing Task 1."},
            {"word": "Synthesize", "meaning": "Combine a number of things into a coherent whole.", "example": "Try to synthesize different arguments in your essay conclusion."},
            {"word": "Evaluate", "meaning": "Form an idea of the amount, number, or value of.", "example": "The examiner will evaluate your grammatical range and accuracy."},
            {"word": "Hypothesis", "meaning": "A proposed explanation made on the basis of limited evidence.", "example": "The academic article proposes a new hypothesis on climate change."},
            {"word": "Significant", "meaning": "Sufficiently great or important to be worthy of attention.", "example": "There is a significant difference between the two datasets shown."},
            {"word": "Substantial", "meaning": "Of considerable importance, size, or worth.", "example": "The company made a substantial profit in the third quarter."},
            {"word": "Coherent", "meaning": "Logical and consistent; forming a unified whole.", "example": "Using transition signals makes your essay paragraphs coherent."},
            {"word": "Adverse", "meaning": "Preventing success or development; harmful; unfavorable.", "example": "The region is suffering from adverse weather conditions."},
            {"word": "Beneficial", "meaning": "Favorable or advantageous; resulting in good.", "example": "Regular practice is highly beneficial for scoring a band 8."},
            {"word": "Consequence", "meaning": "A result or effect of an action or condition.", "example": "Rising sea levels are a direct consequence of global warming."},
            {"word": "Aesthetic", "meaning": "Concerned with beauty or the appreciation of beauty.", "example": "The modern architecture has a unique aesthetic appeal."},
            {"word": "Cognitive", "meaning": "Relating to the mental action or process of acquiring knowledge.", "example": "Learning a foreign language improves cognitive function."},
            {"word": "Demographic", "meaning": "Relating to the structure of populations.", "example": "The survey analyzed various demographic factors such as age and income."},
            {"word": "Empirical", "meaning": "Based on observation or experience rather than theory.", "example": "You must back up your academic claims with empirical evidence."},
            {"word": "Feasible", "meaning": "Possible to do easily or conveniently.", "example": "Implementing carbon taxes is a feasible solution to reduce emissions."},
            {"word": "Inherent", "meaning": "Existing in something as a permanent, essential, or characteristic attribute.", "example": "There are inherent risks in adopting unverified technologies."},
            {"word": "Pragmatic", "meaning": "Dealing with things sensibly and realistically.", "example": "We need a pragmatic approach to solve traffic congestion in cities."},
            {"word": "Ubiquitous", "meaning": "Present, appearing, or found everywhere.", "example": "Mobile phones have become ubiquitous in modern society."},
            {"word": "Vulnerable", "meaning": "Susceptible to physical or emotional attack or harm.", "example": "Coastal cities are vulnerable to extreme weather events."},
            {"word": "Advocate", "meaning": "Publicly recommend or support.", "example": "Many experts advocate for renewable energy sources."},
            {"word": "Mitigate", "meaning": "Make less severe, serious, or painful.", "example": "Planting trees helps mitigate the effects of global warming."},
            {"word": "Precipitate", "meaning": "Cause to happen suddenly, unexpectedly, or prematurely.", "example": "Economic instability can precipitate social unrest."},
            {"word": "Substantiate", "meaning": "Provide evidence to support or prove the truth of.", "example": "You must substantiate your arguments with relevant examples."},
            {"word": "Fluctuate", "meaning": "Rise and fall irregularly in number or amount.", "example": "As shown in the graph, carbon emissions fluctuate throughout the decade."},
            {"word": "Corroborate", "meaning": "Confirm or give support to.", "example": "Scientific studies corroborate the theory of climate change."},
            {"word": "Paradox", "meaning": "A seemingly absurd or self-contradictory statement or proposition.", "example": "It is a paradox that technology connects us yet sometimes isolates us."},
            {"word": "Diligence", "meaning": "Careful and persistent work or effort.", "example": "Studying with diligence is the best way to clear the exams."},
            {"word": "Discrepancy", "meaning": "A lack of compatibility or similarity between two or more facts.", "example": "The audit revealed a major discrepancy in the records."},
            {"word": "Equilibrium", "meaning": "A state in which opposing forces or influences are balanced.", "example": "Nature maintains a delicate equilibrium that humans must respect."},
            {"word": "Sovereign", "meaning": "Possessing supreme or ultimate power.", "example": "A sovereign nation has the right to manage its own resources."}
        ]

        comm_vocab = [
            {"word": "Interact", "meaning": "Act in such a way as to have an effect on another.", "example": "It is important to interact with classmates to build confidence."},
            {"word": "Express", "meaning": "Say or show what you think or feel.", "example": "Try to express your ideas clearly without hesitating."},
            {"word": "Converse", "meaning": "Engage in conversation.", "example": "I want to converse with native speakers to learn their accents."},
            {"word": "Dialogue", "meaning": "Conversation between two or more people.", "example": "Healthy dialogue helps resolve misunderstandings at home."},
            {"word": "Articulate", "meaning": "Express an idea or feeling fluently and coherently.", "example": "She is highly articulate and presents her arguments beautifully."},
            {"word": "Gesture", "meaning": "A movement of part of the body, especially a hand or head, to express an idea.", "example": "Using natural gestures makes your speech feel more engaging."},
            {"word": "Empathize", "meaning": "Understand and share the feelings of another.", "example": "To be a good listener, you need to empathize with the speaker."},
            {"word": "Tone", "meaning": "The general character or attitude of a place, piece of writing, situation, etc.", "example": "A polite tone is essential in customer relations."},
            {"word": "Context", "meaning": "The circumstances that form the setting for an event, statement, or idea.", "example": "Understanding the context helps you pick the right vocabulary words."},
            {"word": "Nuance", "meaning": "A subtle difference in or shade of meaning, expression, or sound.", "example": "Native speakers use subtle nuances that take time to learn."},
            {"word": "Fluency", "meaning": "The ability to speak or write a foreign language easily and accurately.", "example": "Speaking daily is the fastest way to achieve fluency."},
            {"word": "Vocabulary", "meaning": "The body of words used in a particular language.", "example": "Reading books is an excellent way to expand your vocabulary."},
            {"word": "Pronounce", "meaning": "Make the sound of a word or letter in a particular way.", "example": "The tool shows you how to pronounce complex syllables correctly."},
            {"word": "Comprehend", "meaning": "Grasp mentally; understand.", "example": "Do you comprehend the difference between active and passive tenses?"},
            {"word": "Feedback", "meaning": "Information about reactions to a product, performance of a task, etc.", "example": "I appreciate your constructive feedback on my grammar mistakes."},
            {"word": "Clarity", "meaning": "The quality of coherence and intelligibility in communication.", "example": "Speak slowly to maintain clarity throughout your speech."},
            {"word": "Assertion", "meaning": "A confident and forceful statement of fact or belief.", "example": "Support your assertion with logical reasoning."},
            {"word": "Discussion", "meaning": "The action or process of talking about something in order to reach a decision.", "example": "We had a lively discussion about language education."},
            {"word": "Banter", "meaning": "The playful and friendly exchange of teasing remarks.", "example": "Friendly banter is a common part of casual conversations."},
            {"word": "Colloquial", "meaning": "Used in ordinary or familiar conversation; not formal.", "example": "Phrases like 'what's up?' are colloquial and should be avoided in interviews."},
            {"word": "Sarcasm", "meaning": "The use of irony to mock or convey contempt.", "example": "Sarcasm can easily be misunderstood in written messages."},
            {"word": "Idiom", "meaning": "A group of words established by usage as having a meaning not deducible from those of the individual words.", "example": "'Bite the bullet' is an English idiom meaning to face a difficult situation."},
            {"word": "Metaphor", "meaning": "A figure of speech in which a word or phrase is applied to an object or action to which it is not literally applicable.", "example": "Using metaphors adds flavor to your descriptive writing."},
            {"word": "Rapport", "meaning": "A close and harmonious relationship in which the people concerned understand each other's feelings.", "example": "Establishing rapport with your audience keeps them engaged."},
            {"word": "Connection", "meaning": "A relationship in which a person, thing, or idea is linked or associated with something else.", "example": "Conversing helps build a warm connection with people."},
            {"word": "Listen", "meaning": "Give one's attention to a sound.", "example": "Active listening is just as important as speaking fluently."},
            {"word": "Explain", "meaning": "Make something clear to someone by describing it in more detail.", "example": "Could you explain the grammar rule behind this correction?"},
            {"word": "Inquire", "meaning": "Ask for information from someone.", "example": "Feel free to inquire if you have any questions about the syllabus."},
            {"word": "Describe", "meaning": "Give an account in words of someone or something.", "example": "Describe your favorite hobby in 5 sentences."},
            {"word": "Summarize", "meaning": "Give a brief statement of the main points of something.", "example": "Please summarize what you learned in today's lesson."}
        ]

        weeks = {}
        vocab_pool = placement_vocab if ("placement" in goal_lower or "interview" in goal_lower) else (ielts_vocab if "ielts" in goal_lower else comm_vocab)

        # Define day-specific content for Week 1 (Days 1 to 7) to avoid grouping
        placement_week1_days = {
            1: {
                "objective": "Grammar Foundation: Subject-Verb Agreement",
                "concepts": ["Subject-Verb Agreement", "Subject + Verb + Object structure", "Common Singular/Plural Pitfalls"],
                "study_material": [
                    "A singular subject needs a singular verb (e.g. 'He runs'). A plural subject needs a plural verb (e.g. 'They run').",
                    "Example: ✅ 'She prepares for the interview.' | ❌ 'She prepare for the interview.'"
                ],
                "grammar_exercises": [
                    "Correct: He don't like coding.",
                    "Correct: We was happy yesterday.",
                    "Correct: I am study for placements.",
                    "Correct: She go to office daily.",
                    "Correct: They is preparing for interviews."
                ],
                "speaking_task": "Record yourself answering: 'Tell me about yourself'. Limit it to 1 minute.",
                "writing_task": "Write: 'My career objective for placements'. Minimum 80 words.",
                "expected_outcome": "Understand SVO structure and basic subject-verb agreement in formal greetings."
            },
            2: {
                "objective": "Simple Present Tense & Talking about Routines",
                "concepts": ["Simple Present Tense", "Describing habits/routines", "Expressing factual statements"],
                "study_material": [
                    "Use simple present for things that are generally true or happen regularly.",
                    "Example: ✅ 'I code in Python every evening.' | ❌ 'I coding in Python every evening.'"
                ],
                "grammar_exercises": [
                    "Correct: She don't goes to college.",
                    "Correct: I has a great interest in software development.",
                    "Correct: They is practicing coding everyday.",
                    "Correct: He write code daily."
                ],
                "speaking_task": "Describe your daily routine as a student or professional in 1 minute.",
                "writing_task": "Write: 'Why I chose my branch/field of study'. Minimum 100 words.",
                "expected_outcome": "Fluency in describing habits, current skills, and routines in present tense."
            },
            3: {
                "objective": "Past Simple Tense & Discussing Past Achievements",
                "concepts": ["Simple Past Tense", "Regular vs Irregular Past Verbs", "Talking about completed actions"],
                "study_material": [
                    "Use past simple for actions completed at a specific time in the past.",
                    "Example: ✅ 'I completed the project last semester.' | ❌ 'I have completed the project last semester yesterday.'"
                ],
                "grammar_exercises": [
                    "Correct: I done the project last month.",
                    "Correct: She did not went to the lab.",
                    "Correct: We was working on a group task.",
                    "Correct: He graduate in 2024."
                ],
                "speaking_task": "Describe a successful college project you worked on. Speak for 1 minute.",
                "writing_task": "Write: 'A challenge I faced in a group project and how I resolved it'. Minimum 100 words.",
                "expected_outcome": "Correct usage of simple past tense to describe project history and past academic milestones."
            },
            4: {
                "objective": "Future Simple Tense & Career Aspirations",
                "concepts": ["Simple Future Tense", "Expressing future goals", "Using 'will' vs 'going to'"],
                "study_material": [
                    "Use 'will' for sudden decisions or general predictions. Use 'going to' for plans already made.",
                    "Example: ✅ 'I am going to join a startup next month.' | ❌ 'I will going to join a startup next month.'"
                ],
                "grammar_exercises": [
                    "Correct: I will going to attend the drive tomorrow.",
                    "Correct: She will has an interview next week.",
                    "Correct: We are join the company soon.",
                    "Correct: They will preparing for the test tomorrow."
                ],
                "speaking_task": "Speak about: 'Where do you see yourself in 3 years?'. Speak for 1-2 minutes.",
                "writing_task": "Write: 'My dream job and how I am preparing for it'. Minimum 100 words.",
                "expected_outcome": "Confidence in discussing future job plans, career growth, and goals in future tense."
            },
            5: {
                "objective": "Present Continuous & Perfect Tenses",
                "concepts": ["Present Continuous vs Present Perfect", "Discussing ongoing tasks and experiences", "State verbs vs action verbs"],
                "study_material": [
                    "Use present continuous for ongoing actions. Use present perfect for actions completed recently or experience.",
                    "Example: ✅ 'I have studied Java for two years.' | ❌ 'I am studying Java since two years.'"
                ],
                "grammar_exercises": [
                    "Correct: I am working on this project since last month.",
                    "Correct: She has finished the code yesterday.",
                    "Correct: They are knowing the answers.",
                    "Correct: We have been completed our coursework."
                ],
                "speaking_task": "Describe what you are currently learning or working on in a 1-minute recording.",
                "writing_task": "Write: 'A summary of my core technical skills and tools I have used'. Minimum 80 words.",
                "expected_outcome": "Understanding the difference between ongoing states, recently completed milestones, and general experiences."
            },
            6: {
                "objective": "Complex Sentences & Connectors for Flow",
                "concepts": ["Compound and Complex Sentences", "Using connectors: because, although, therefore, whereas", "Fluency and coherence"],
                "study_material": [
                    "Connectors make your answers sound mature and coherent instead of choppy and simple.",
                    "Example: ✅ 'Although I am a beginner, I am proactive.' | ❌ 'I am a beginner. But I am proactive.'"
                ],
                "grammar_exercises": [
                    "Correct: He is a good coder but he is lazy although.",
                    "Correct: Because she worked hard, so she got placed.",
                    "Correct: They failed, therefore, they didn't test the code.",
                    "Correct: Whereas I like coding, but he likes design."
                ],
                "speaking_task": "Compare front-end development vs back-end development using connectors in a 1-minute talk.",
                "writing_task": "Write: 'The role of technology in modern business'. Use at least 4 different connectors. Minimum 100 words.",
                "expected_outcome": "Ability to join ideas logically and present structured, complex arguments."
            },
            7: {
                "objective": "Weekly Review & Comprehensive Assessment",
                "concepts": ["Review of Week 1 grammar", "Self-reflection of weaknesses", "Formal interview introduction final polish"],
                "study_material": [
                    "Combine all elements from Week 1 (agreement, present/past/future tenses, complex structures).",
                    "Read your answers aloud to double-check pronunciation and stress."
                ],
                "grammar_exercises": [
                    "Correct: He don't know why she did went yesterday.",
                    "Correct: We was preparing since three hours yesterday.",
                    "Correct: She will goes to office tomorrow.",
                    "Correct: I look forward to meet the HR manager."
                ],
                "speaking_task": "Deliver your final, polished 1-minute self-introduction pitch including goal, skills, and background.",
                "writing_task": "Write: 'My self-reflection on grammar strengths and weaknesses'. Minimum 120 words.",
                "expected_outcome": "A complete, grammatically sound, and confidently delivered professional introduction pitch."
            }
        }

        ielts_week1_days = {
            1: {
                "objective": "IELTS Academic Writing Task 1: Overview & Graph Trends",
                "concepts": ["Overview structure", "Trend verbs and adverbs", "Introduction paraphrasing"],
                "study_material": [
                    "Writing Task 1 requires an introduction, overview of main trends, and detail paragraphs.",
                    "Example: ✅ 'The data illustrates a gradual rise.' | ❌ 'The graph show things going up.'"
                ],
                "grammar_exercises": [
                    "Correct: The graph show that sales increased.",
                    "Correct: There was a significant rise of the price.",
                    "Correct: The numbers decreased gradual.",
                    "Correct: The percentage of students are rising."
                ],
                "speaking_task": "Describe a trend you have noticed in your country's weather patterns recently. (1 min)",
                "writing_task": "Write a 1-paragraph overview of a line graph showing rising internet usage from 2000 to 2020. (80 words)",
                "expected_outcome": "Understand Task 1 format and describe upward/downward patterns accurately."
            },
            2: {
                "objective": "IELTS Academic Reading: Skimming & Scanning",
                "concepts": ["Skimming for main ideas", "Scanning for key words", "Answering True/False/Not Given"],
                "study_material": [
                    "Skim reading sections to locate paragraph themes. Scan to find dates, names, or numbers to answer questions.",
                    "Example: Look for synonyms of keywords in questions rather than exact words."
                ],
                "grammar_exercises": [
                    "Correct: According to text, the temperature rise.",
                    "Correct: Research indicate that species are dying.",
                    "Correct: The author do not agree with the theory.",
                    "Correct: There is many arguments against it."
                ],
                "speaking_task": "Summarize the main idea of a recent news article you read. (1 min)",
                "writing_task": "Write a summary of how skimming differs from scanning in reading comprehension. (80 words)",
                "expected_outcome": "Quickly identify key factual details in academic text extracts."
            },
            3: {
                "objective": "IELTS Writing Task 2: Essay Structures & Outlining",
                "concepts": ["Essay prompt analysis", "Structuring Introduction & Thesis statement", "Paragraph layouts"],
                "study_material": [
                    "Structure your Task 2 essay with an introduction (paraphrase + thesis), 2 body paragraphs, and a conclusion.",
                    "Example: State your stance clearly in the first paragraph."
                ],
                "grammar_exercises": [
                    "Correct: In my opinion, I agree with this essay.",
                    "Correct: Although many people support this, but others disagree.",
                    "Correct: The benefits of this choice is substantial.",
                    "Correct: Government should to ban smoking."
                ],
                "speaking_task": "State your opinion on: 'Should public transport be free?'. Speak for 1 minute.",
                "writing_task": "Write a thesis statement and introduction paragraph for the topic: 'Should university education be free?'. (80 words)",
                "expected_outcome": "Draft clear thesis statements and structured essay outlines."
            },
            4: {
                "objective": "IELTS Speaking Part 1: Familiar Topics & Intonation",
                "concepts": ["Answering simple personal questions", "Extending answers naturally", "Using range of vocabulary"],
                "study_material": [
                    "In Part 1, answer in 2-3 sentences. Don't give 1-word answers. Speak clearly with natural rising/falling intonation."
                ],
                "grammar_exercises": [
                    "Correct: I am liking to study English.",
                    "Correct: My hometown is very clean than other cities.",
                    "Correct: I live here since my childhood.",
                    "Correct: Cooking is a good hobby because I enjoy."
                ],
                "speaking_task": "Answer 3 common Part 1 questions: 'Where is your hometown?', 'Do you like reading?', 'How do you spend weekends?'",
                "writing_task": "Write extended written answers for the 3 speaking questions above. (90 words)",
                "expected_outcome": "Ability to answer Part 1 prompts fluently using correct present tenses and structures."
            },
            5: {
                "objective": "IELTS Writing Task 1: Comparing Data & Structures",
                "concepts": ["Making comparative sentences", "Linking data points", "Using words like 'whereas', 'whilst'"],
                "study_material": [
                    "When writing, group similar data and highlight major discrepancies or differences.",
                    "Example: 'While country A consumed 50 units, country B used only 10.'"
                ],
                "grammar_exercises": [
                    "Correct: In comparison of country A, country B...",
                    "Correct: The graph shows that sales fluctuated irregular.",
                    "Correct: The value was double than the first year.",
                    "Correct: Sales rose up to 50%."
                ],
                "speaking_task": "Compare your lifestyle today with your lifestyle 5 years ago in a 1-minute recording.",
                "writing_task": "Write 3 comparative sentences based on mock data showing car sales vs bus sales. (80 words)",
                "expected_outcome": "Use comparison words accurately to describe statistical variations."
            },
            6: {
                "objective": "IELTS Academic Reading: Identifying Writer's Views",
                "concepts": ["Yes/No/Not Given questions", "Identifying writer's opinion vs fact", "Context clues"],
                "study_material": [
                    "Read closely to determine if the author actively supports an idea, stands neutral, or opposes it."
                ],
                "grammar_exercises": [
                    "Correct: The author suggest to change the policy.",
                    "Correct: He is believing that science will solve it.",
                    "Correct: It is critical that we preserves forests.",
                    "Correct: The data is not supporting the claim."
                ],
                "speaking_task": "Discuss whether you agree with the author of a book you read. Speak for 1 minute.",
                "writing_task": "Write a short paragraph analyzing the writer's perspective on climate change in a mock text. (80 words)",
                "expected_outcome": "Differentiate between objective facts and writer's personal opinions in texts."
            },
            7: {
                "objective": "Weekly IELTS Assessment & Practice",
                "concepts": ["Combining Reading, Writing & Speaking elements", "Review of tenses and academic words"],
                "study_material": [
                    "Review your essays for grammatical range and correct spelling.",
                    "Focus on syllable stress in academic words."
                ],
                "grammar_exercises": [
                    "Correct: The number has increased gradually since last decade.",
                    "Correct: Although it is hot, but I went out.",
                    "Correct: The graph are indicating a decline.",
                    "Correct: I look forward to achieve a high score."
                ],
                "speaking_task": "Answer a complete Part 1 speaking mock card on your studies and hobbies.",
                "writing_task": "Write a complete Writing Task 1 response based on a simple table. (150 words)",
                "expected_outcome": "Completion of a grammatically accurate Task 1 response and fluent Part 1 answers."
            }
        }

        comm_week1_days = {
            1: {
                "objective": "Conversational Grammar: Subject-Verb Agreement",
                "concepts": ["SVO structure", "Verb agreement in conversation", "Polite daily greetings"],
                "study_material": [
                    "Ensure subject and verb match in oral chat: 'She speaks English well' (not 'She speak').",
                    "Use warm, polite greetings: 'How are you doing?' instead of mechanical 'How are you?'."
                ],
                "grammar_exercises": [
                    "Correct: Me and him went to market.",
                    "Correct: She don't like coffee.",
                    "Correct: We was watching a movie.",
                    "Correct: They is very friendly."
                ],
                "speaking_task": "Introduce yourself and describe your hobbies in a 1-minute recording.",
                "writing_task": "Write a friendly greeting email to a new pen pal. (80 words)",
                "expected_outcome": "Confident, grammatically correct introductions in casual settings."
            },
            2: {
                "objective": "Talking about Routines & Habitual Actions",
                "concepts": ["Present Simple in conversations", "Time adverbs: usually, always, rarely"],
                "study_material": [
                    "Use adverbs of frequency to describe routine events: 'I usually wake up at 7 AM.'"
                ],
                "grammar_exercises": [
                    "Correct: I am usually going to gym daily.",
                    "Correct: My brother like to read books.",
                    "Correct: They does not watch TV.",
                    "Correct: He walk his dog every morning."
                ],
                "speaking_task": "Describe your daily routine to a friend in 1 minute.",
                "writing_task": "Write: 'My favorite daily ritual'. Minimum 80 words.",
                "expected_outcome": "Use frequency adverbs and simple present tense to talk about daily habits."
            },
            3: {
                "objective": "Discussing Past Experiences & Stories",
                "concepts": ["Past Simple in conversational stories", "Regular vs Irregular verbs", "Linking past events"],
                "study_material": [
                    "When sharing a story, keep verbs in simple past and use sequencing words like 'first', 'then', 'after that'."
                ],
                "grammar_exercises": [
                    "Correct: Yesterday I went and bought some apples and eat them.",
                    "Correct: She did not called me last night.",
                    "Correct: We was very tired after the trip.",
                    "Correct: He see a movie two days ago."
                ],
                "speaking_task": "Tell a short, interesting story about a trip you took in the past. (1 min)",
                "writing_task": "Write a diary entry about a memorable day in your life. (100 words)",
                "expected_outcome": "Flow cleanly when recounting past events using correct past tense verbs."
            },
            4: {
                "objective": "Future Plans & Conversational Intentions",
                "concepts": ["Future structures: will, going to, present continuous for future", "Making social plans"],
                "study_material": [
                    "Use present continuous for social plans: 'We're meeting at 8 PM tonight.'"
                ],
                "grammar_exercises": [
                    "Correct: I will going to meet my friend tomorrow.",
                    "Correct: They are leave next Friday.",
                    "Correct: We will having a party this weekend.",
                    "Correct: She is go to buy a phone."
                ],
                "speaking_task": "Describe your plans for the upcoming weekend. Speak for 1 minute.",
                "writing_task": "Draft a text message inviting a group of friends for dinner. (80 words)",
                "expected_outcome": "Confidently discuss upcoming appointments, goals, and arrangements."
            },
            5: {
                "objective": "Continuous Actions & Experiences",
                "concepts": ["Present Continuous vs Present Perfect", "Talking about hobbies you've done for a long time"],
                "study_material": [
                    "Use present perfect to express duration of an ongoing habit: 'I've played guitar for five years.'"
                ],
                "grammar_exercises": [
                    "Correct: I am knowing him since childhood.",
                    "Correct: She has seen that movie yesterday.",
                    "Correct: We are living in this city since 2018.",
                    "Correct: They have been completed the assignment."
                ],
                "speaking_task": "Talk about a hobby you have practiced for a long time. (1 min)",
                "writing_task": "Write a short paragraph about how your hobbies have changed over the years. (80 words)",
                "expected_outcome": "Use perfect and continuous tenses correctly to talk about life history."
            },
            6: {
                "objective": "Cohesion & Flow: Transition Words in Speech",
                "concepts": ["Conversational connectors: so, because, but, although", "Structuring ideas logically"],
                "study_material": [
                    "Avoid choppy speech. Connect ideas: 'I wanted to go, but it was raining, so I stayed home.'"
                ],
                "grammar_exercises": [
                    "Correct: He is nice guy, because he always helps.",
                    "Correct: Although she was sick, but she came to class.",
                    "Correct: They arrived late, so therefore they missed the bus.",
                    "Correct: I like tea whereas my sister likes tea too."
                ],
                "speaking_task": "Give your opinion on: 'Do you prefer city life or country life? Why?' using connectors.",
                "writing_task": "Write: 'Why learning languages is beneficial'. Use at least 4 connectors. (100 words)",
                "expected_outcome": "Use transitional words naturally to maintain sentence connections and speech flow."
            },
            7: {
                "objective": "Weekly Conversational Review & Assessment",
                "concepts": ["Polishing general conversation tenses", "Pronunciation of daily words"],
                "study_material": [
                    "Synthesize present, past, future tenses, and connectors in a single conversation."
                ],
                "grammar_exercises": [
                    "Correct: He don't know where we was going yesterday.",
                    "Correct: She will goes to market with me tomorrow.",
                    "Correct: I look forward to hear your story.",
                    "Correct: We was talking since two hours."
                ],
                "speaking_task": "Record a 2-minute general introduction detailing your routines, background, and weekend plans.",
                "writing_task": "Write: 'My reflections on my conversational progress'. (100 words)",
                "expected_outcome": "A complete, fluent, and grammatically accurate self-description covering all basic tenses."
            }
        }

        def make_day(day_idx, week_idx, vocab_start):
            day_vocab = vocab_pool[vocab_start:vocab_start+5]
            if len(day_vocab) < 5:
                day_vocab = (vocab_pool + vocab_pool)[vocab_start:vocab_start+5]
            vocab_words = [item["word"] for item in day_vocab]

            if week_idx == 1:
                if "placement" in goal_lower or "interview" in goal_lower:
                    day_data = placement_week1_days[day_idx]
                elif "ielts" in goal_lower:
                    day_data = ielts_week1_days[day_idx]
                else:
                    day_data = comm_week1_days[day_idx]

                return {
                    "day": day_idx,
                    "objective": day_data["objective"],
                    "concepts": day_data["concepts"],
                    "study_material": day_data["study_material"],
                    "grammar_exercises": day_data["grammar_exercises"],
                    "vocabulary": day_vocab,
                    "pronunciation_practice": vocab_words,
                    "speaking_task": day_data["speaking_task"],
                    "writing_task": day_data["writing_task"],
                    "assessment": day_data.get("assessment", []),
                    "expected_outcome": day_data["expected_outcome"],
                    "progress_points": 4
                }
            else:
                objective, tasks, assessment, expected_outcome = Plan._get_dynamic_curriculum(day_idx, goal_lower, vocab_words)
                
                # Check for adaptive weak areas focus!
                if "Grammar" in weak_areas:
                    tasks.append("Grammar Practice: Complete today's sentence structure exercise to fix grammatical weak areas.")
                if "Pronunciation" in weak_areas:
                    tasks.append("Pronunciation Focus: Pronounce today's key vocabulary words focusing on syllable stress.")

                return {
                    "day": day_idx,
                    "objective": objective,
                    "tasks": tasks,
                    "assessment": assessment,
                    "expected_outcome": expected_outcome,
                    "progress_points": 4 if day_idx < 25 else 5
                }

        weeks["week_1"] = {
            "goal": f"Week 1: Build basic sentence structure & core grammar foundations for {goal}",
            "days": [make_day(d, 1, (d-1)*5) for d in range(1, 8)]
        }
        weeks["week_2"] = {
            "goal": f"Week 2: Focus on {goal} specialized vocabulary & active expression",
            "days": [make_day(d, 2, (d-1)*5) for d in range(8, 15)]
        }
        weeks["week_3"] = {
            "goal": f"Week 3: Polish dialogue flow, topic presentations & speaking comfort",
            "days": [make_day(d, 3, (d-1)*5) for d in range(15, 22)]
        }
        weeks["week_4"] = {
            "goal": f"Week 4: Execute mock evaluations, final checks & readiness drills",
            "days": [make_day(d, 4, (d-1)*5) for d in range(22, 31)]
        }

        plan = Plan(
            title=f"{level} {goal} Plan",
            goal=goal,
            duration=duration,
            difficulty=level,
            steps=steps,
            weeks=weeks,
            recommendations=recommendations,
            milestones=milestones,
            learning_level=level,
            weak_areas=weak_areas
        )
        plan.total_steps = len(steps)
        return plan

    @staticmethod
    def create_learning_plan(
        user_goal: str,
        weak_areas: List[str]
    ) -> Plan:
        """
        Create a plan focusing on specified weak areas.
        """
        goal = user_goal or "General English"
        weak_areas = weak_areas or []

        steps = []
        recommendations = []

        if "Grammar" in weak_areas:
            steps.append("Grammar Mastery: Review active tense structures and syntax rules")
            recommendations.append("Do 5 grammar corrections in the chat daily")
        
        if "Vocabulary" in weak_areas:
            steps.append("Vocabulary Expansion: Acquire context-specific idioms and terms")
            recommendations.append("Use the synonym and antonym search tool to broaden expression")

        if "Pronunciation" in weak_areas:
            steps.append("Pronunciation & Intonation: Work on phonetic clarity and speech flow")
            recommendations.append("Use the pronunciation helper to split hard words into syllables")

        if "Conversation" in weak_areas:
            steps.append("Conversational Comfort: Engage in simulated realistic topic chats")
            recommendations.append("Start a topic-based chat session daily and review agent feedback")

        # Fallback if no specific weak areas are targeted
        if not steps:
            steps.append("General English Roadmap: Work on overall grammar, vocab, and talking skills")
            recommendations.append("Spend 10 minutes checking daily word and practice conversation")

        steps.append("Progress Assessment: Evaluate improvements across all targeted disciplines")
        
        milestones = [
            "Identify and log progress on key weak areas weekly",
            "Complete all recommended practice routines successfully"
        ]

        plan = Plan(
            title=f"Custom Plan: {goal}",
            goal=goal,
            duration="30 Days",
            difficulty="Medium",
            steps=steps,
            recommendations=recommendations,
            milestones=milestones,
            weak_areas=weak_areas
        )
        plan.total_steps = len(steps)
        return plan

    @classmethod
    def generate_day_plan(cls, user_id: str, day_number: int) -> Dict:
        from app.services.memory_manager import MemoryManager
        profile = MemoryManager.get_profile(user_id)
        goal = profile.get("goal") or "General English"
        level = profile.get("learning_level") or "Beginner"
        weak_areas = profile.get("weak_areas", [])

        plan = cls.generate_learning_plan(
            user_id=user_id,
            goal=goal,
            duration="30 Days",
            level=level,
            weak_areas=weak_areas
        )

        if 1 <= day_number <= 7:
            week_key = "week_1"
            day_idx = day_number - 1
        elif 8 <= day_number <= 14:
            week_key = "week_2"
            day_idx = day_number - 8
        elif 15 <= day_number <= 21:
            week_key = "week_3"
            day_idx = day_number - 15
        elif 22 <= day_number <= 30:
            week_key = "week_4"
            day_idx = day_number - 22
        else:
            return {}

        week_data = plan.weeks.get(week_key, {})
        days_list = week_data.get("days", [])
        if 0 <= day_idx < len(days_list):
            day_data = days_list[day_idx]
            
            # Get completed tasks for today from memory
            completed_task_names = MemoryManager.get_current_day_completed_tasks(user_id)
            
            tasks_list = []
            if week_key == "week_1":
                # Vocabulary Learning
                vocab_list = day_data.get("vocabulary", [])
                if vocab_list:
                    vocab_words = ", ".join(v["word"] for v in vocab_list)
                    tasks_list.append(f"Vocabulary: Learn and define 5 new words: {vocab_words}")
                
                # Grammar Corrections
                grammar_exs = day_data.get("grammar_exercises", [])
                for ex in grammar_exs[:2]: # Show up to 2 exercises to keep dashboard clean
                    tasks_list.append(f"Grammar: {ex}")
                    
                # Pronunciation Practice
                pron_practice = day_data.get("pronunciation_practice", [])
                if pron_practice:
                    tasks_list.append(f"Pronunciation: Practice speaking: {', '.join(pron_practice)}")
                    
                # Speaking Task
                spk_task = day_data.get("speaking_task", "")
                if spk_task:
                    tasks_list.append(f"Speaking: {spk_task}")
                    
                # Writing Task
                wrt_task = day_data.get("writing_task", "")
                if wrt_task:
                    tasks_list.append(f"Writing: {wrt_task}")
                    
                # Assessment
                tasks_list.append("Assessment: Submit daily review & self-evaluation")
            else:
                tasks_list = list(day_data.get("tasks", []))
                
                # Add assessment if not present in tasks
                has_assessment = any("assessment" in t.lower() or "test" in t.lower() or "evaluation" in t.lower() for t in tasks_list)
                if not has_assessment:
                    tasks_list.append("Assessment: Complete daily review check")

            # Standardize return dictionary
            tasks_response = []
            for task_name in tasks_list:
                tasks_response.append({
                    "name": task_name,
                    "completed": task_name in completed_task_names
                })
                
            return {
                "day": day_number,
                "objective": day_data.get("objective", ""),
                "tasks": tasks_response,
                "assessment": day_data.get("assessment", "Daily 5-minute review") or "Daily 5-minute review",
                "expected_outcome": day_data.get("expected_outcome", "Improve overall language skills") or "Improve overall language skills",
                "vocabulary": day_data.get("vocabulary", []),
                "grammar_tasks": day_data.get("grammar_exercises", []),
                "speaking_task": day_data.get("speaking_task", "")
            }
        return {}