from app.config import Settings
from app.services.llm import LLMService
from app.services.vector_store import KnowledgeVectorStore


class CoachService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.llm = LLMService(settings)
        self.vector_store = KnowledgeVectorStore(settings)

    def _context(self, query: str) -> str:
        results = self.vector_store.query(query, limit=5)
        if not results:
            return "No local knowledge base context found."
        return "\n\n".join(
            f"Source {index + 1}: {result['text']}"
            for index, result in enumerate(results)
        )

    def generate_plan(self, goal: str, focus_patterns: str, duration_days: int) -> str:
        context = self._context(f"{goal}\n{focus_patterns}")
        return self.llm.complete(
            system=(
                "You are AlgoGym, a local-first algorithm training coach. "
                "Create practical, habit-oriented training plans from local notes. "
                "Prefer short daily work, review loops, and pattern mastery."
            ),
            user=(
                f"Goal: {goal}\n"
                f"Focus patterns: {focus_patterns}\n"
                f"Duration days: {duration_days}\n\n"
                f"Local knowledge context:\n{context}\n\n"
                "Return a concise JSON array of daily plan objects with day, focus, "
                "warm_up, main_workout, review, and reflection fields."
            ),
        )

    def generate_workout(self, goal: str, focus: str) -> str:
        context = self._context(f"{goal}\n{focus}")
        return self.llm.complete(
            system=(
                "You are AlgoGym. Generate daily algorithm workouts that feel like "
                "fitness programming: warm-up, main work, review, and reflection."
            ),
            user=(
                f"Goal: {goal}\nFocus: {focus}\n\n"
                f"Local knowledge context:\n{context}\n\n"
                "Return concise sections for warm_up, main_workout, review, and "
                "reflection_prompt. Include problem-selection criteria, not full answers."
            ),
        )

    def generate_hint(
        self,
        problem: str,
        current_attempt: str,
        level: int,
        unlock_solution: bool = False,
    ) -> str:
        bounded_level = min(max(level, 1), 3)
        context = self._context(problem)
        level_rules = {
            1: "Return only a trigger keyword, such as 'think sliding window'.",
            2: "Return the pattern name and a high-level approach only.",
            3: "Return pseudocode only, with no working implementation code.",
        }
        solution_rule = (
            "The user explicitly unlocked the solution, so implementation code is allowed."
            if unlock_solution
            else "Do not include implementation code or a complete solution."
        )
        return self.llm.complete(
            system=(
                "You are AlgoGym's hint coach. Never reveal a complete solution by "
                "default. Keep hints incremental and focused on learning."
            ),
            user=(
                f"Hint level: {bounded_level}\n"
                f"Rule: {level_rules[bounded_level]}\n\n"
                f"Solution policy: {solution_rule}\n\n"
                f"Problem:\n{problem}\n\n"
                f"Current attempt:\n{current_attempt}\n\n"
                f"Local knowledge context:\n{context}\n\n"
                "Return the hint only."
            ),
            temperature=0.2,
        )
