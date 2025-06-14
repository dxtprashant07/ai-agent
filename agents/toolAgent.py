import os
import requests
from dotenv import load_dotenv
from .tools import WeatherTool, SearchTool, PythonREPLTool, LLMResponseTool

load_dotenv()


class ToolAgent:
    def __init__(self):
        self.weather_tool = WeatherTool()
        self.search_tool = SearchTool()
        self.python_repl = PythonREPLTool()
        self.llm_tool = LLMResponseTool()

    def get_detailed_response(self, task, search_result):
        """Combine search results with LLM response for detailed answers."""
        llm_prompt = f"""Query: {task}
Search Results: {search_result}
Please provide a detailed response combining the search results with additional context and explanation."""
        
        llm_response = self.llm_tool.generate_response(llm_prompt)
        return f"Based on search and analysis:\n\n{llm_response}"

    def execute_task(self, task):
        task_lower = task.lower()
        
        # Handle calculations first (most specific)
        if any(op in task_lower for op in ['+', '-', '*', '/', '=']):
            try:
                import re
                match = re.search(r'([-+*/\d\s\.]+)', task_lower)
                if match:
                    expr = match.group(1)
                    result = eval(expr)
                    return f"The result is {result}."
            except Exception:
                pass
        
        # Handle weather queries
        elif 'weather' in task_lower or 'temperature' in task_lower:
            import re
            cities = []
            in_cities = re.findall(r'in ([a-zA-Z\s,]+)', task_lower)
            if in_cities:
                for city_group in in_cities:
                    cities.extend([c.strip() for c in re.split(r'(?:,|\sand\s)', city_group)])
            
            if not cities:
                return "Could not identify city name in the query. Please specify a city (e.g., 'temperature in London')."
            
            results = []
            for city in cities:
                result = self.weather_tool.get_weather(city)
                results.append(result)
            return "\n".join(results)
            
        # Handle programming tasks
        elif any(word in task_lower for word in ['python', 'function', 'program', 'code']):
            if 'write' in task_lower or 'create' in task_lower:
                return self.llm_tool.generate_response(task)
            return self.python_repl.execute(task)
        
        # Handle creative tasks with LLM
        elif any(word in task_lower for word in ['write', 'poem', 'story', 'essay', 'creative']):
            return self.llm_tool.generate_response(task)
            
        # Handle search queries
        elif task_lower.startswith(('what', 'who', 'when', 'where', 'why', 'how')):
            result = self.search_tool.search(task)
            if "No relevant results found" in result:
                return self.llm_tool.generate_response(task)
            return result
            
        # Default to LLM for general queries
        else:
            return self.llm_tool.generate_response(task)


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def modify_task(self, task_index, new_task):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index] = new_task
        else:
            raise IndexError("Task index out of range.")

    def delete_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            del self.tasks[task_index]
        else:
            raise IndexError("Task index out of range.")

    def execute_tasks(self):
        results = []
        for task in self.tasks:
            result = self.execute_task(task)
            results.append(result)
        return results

    def execute_task(self, task):
        # Placeholder for task execution logic
        return f"Executed task: {task}"