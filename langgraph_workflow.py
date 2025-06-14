from typing import List, Dict
from pydantic import BaseModel
from agents.planAgent import PlanAgent
from agents.toolAgent import ToolAgent
from spellchecker import SpellChecker

class WorkflowState(BaseModel):
    query: str
    tasks: List[str] = []
    results: List[Dict] = []

def planning_node(state):
    planner = PlanAgent()
    state.tasks = planner.analyze_query(state.query)
    return state

def reflection_node(state):
    spell = SpellChecker()
    weather_typos = ['tempreture', 'temprature', 'tempratute', 'tempraturee', 'tempratuer', 'wheather']
    valid_tasks = []
    
    for task in state.tasks:
        task_lower = task.lower()
        corrected_task = task
        
        # Check for weather-related queries first
        has_weather_typo = any(typo in task_lower for typo in weather_typos)
        if has_weather_typo or 'weather' in task_lower or 'temperature' in task_lower:
            # Fix common weather typos
            for typo in weather_typos:
                if typo in task_lower:
                    corrected_task = task_lower.replace(typo, 'temperature')
                    print(f"Reflection: Fixing typo in '{task}' to '{corrected_task}'")
            
            # Ensure "in" is present for city
            if 'in' not in corrected_task:
                city = corrected_task.replace('temperature', '').replace('weather', '').strip()
                corrected_task = f"temperature in {city}"
                
            valid_tasks.append(corrected_task)
            continue
            
        # Handle other task types
        if any(keyword in task_lower for keyword in ['search', 'what', 'how', 'why', 'calculate', 'python']):
            valid_tasks.append(task)
        else:
            # For general queries, pass through as-is
            valid_tasks.append(task)
    
    state.tasks = valid_tasks
    return state

def execution_node(state):
    if not state.tasks:
        return WorkflowState(
            query=state.query,
            tasks=[],
            results=[{
                'task': 'No valid tasks',
                'result': 'Please provide valid tasks like:\n- Weather queries (e.g., "weather in London")\n- Math calculations (e.g., "calculate 2 + 2")\n- News updates (e.g., "summarize the news")'
            }]
        )
    
    tool_agent = ToolAgent()
    results = []
    for task in state.tasks:
        result = tool_agent.execute_task(task)
        results.append({'task': task, 'result': result})
    state.results = results
    return state

def run_workflow(state):
    # Run each node in sequence
    state = planning_node(state)
    state = reflection_node(state)
    state = execution_node(state)
    return state

def run_langgraph_workflow(query):
    try:
        initial_state = WorkflowState(query=query)
        final_state = run_workflow(initial_state)
        return final_state.results
    except Exception as e:
        return [{'task': 'Error', 'result': f'An error occurred: {str(e)}'}]

if __name__ == "__main__":
    query = input("Enter your query: ")
    results = run_langgraph_workflow(query)
    for item in results:
        print(f"Task: {item['task']}\nResult: {item['result']}\n")