from agents.planAgent import PlanAgent
from agents.toolAgent import ToolAgent
from utils.reflection import log_feedback

class WorkflowPipeline:
    def __init__(self):
        self.plan_agent = PlanAgent()
        self.tool_agent = ToolAgent()

    def run(self, user_query):
        # Step 1: Split the user query into sub-tasks
        tasks = self.plan_agent.analyze_query(user_query)
        
        # Step 2: Iteratively refine and execute tasks
        for task in tasks:
            refined_task = self.refine_task(task)
            result = self.tool_agent.execute_task(refined_task)
            self.handle_feedback(refined_task, result)

    def refine_task(self, task):
        # Logic to modify, delete, or add tasks as needed
        # Placeholder for task refinement logic
        return task

    def handle_feedback(self, task, result):
        # Log feedback and assess performance
        log_feedback(task, result)

class AgenticWorkflow:
    def __init__(self):
        self.planner = PlanAgent()
        self.tool_agent = ToolAgent()

    def run(self, query):
        tasks = self.planner.analyze_query(query)
        results = []
        for task in tasks:
            result = self.tool_agent.execute_task(task)
            results.append({'task': task, 'result': result})
        return results

if __name__ == "__main__":
    pipeline = WorkflowPipeline()
    user_query = input("Enter your query: ")
    pipeline.run(user_query)