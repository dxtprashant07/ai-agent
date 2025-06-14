from agents.planAgent import PlanAgent
from agents.toolAgent import ToolAgent
import langgraph
from langgraph.graph import StateGraph
from pydantic import BaseModel
from typing import List, Dict
from spellchecker import SpellChecker  # Importing SpellChecker

class WorkflowState(BaseModel):
    query: str
    tasks: List[str] = []
    results: List[Dict] = []
    corrected: bool = False  # Track if tasks have been corrected

def planning_node(state):
    if not state.corrected:  # Only plan if tasks haven't been corrected
        planner = PlanAgent()
        state.tasks = planner.analyze_query(state.query)
    return state

def reflection_node(state):
    if not state.corrected:  # Only correct typos once
        spell = SpellChecker()
        weather_typos = ['temprature', 'tempratute', 'tempraturee', 'tempratuer']
        new_tasks = []
        for task in state.tasks:
            corrected_words = [spell.correction(word) if spell.correction(word) is not None else word for word in task.split()]
            corrected_task = ' '.join(corrected_words)
            for typo in weather_typos:
                if typo in corrected_task.lower():
                    corrected_task = corrected_task.replace(typo, 'temperature')
                    print(f"Reflection: Modifying task '{task}' to '{corrected_task}'.")
            new_tasks.append(corrected_task)
        state.tasks = [task for task in new_tasks if task.strip()]
        state.corrected = True
    return state

def execution_node(state):
    if not state.tasks:
        return state
    tool_agent = ToolAgent()
    results = []
    for task in state.tasks:
        result = tool_agent.execute_task(task)
        results.append({'task': task, 'result': result})
    state.results = results
    return state

# Build the workflow graph using LangGraph's StateGraph
workflow = StateGraph(state_schema=WorkflowState)
workflow.add_node('planning', planning_node)
workflow.add_node('reflection', reflection_node)
workflow.add_node('execution', execution_node)

workflow.add_edge('planning', 'reflection')
workflow.add_edge('reflection', 'execution')

workflow.set_entry_point('planning')

def run_langgraph_workflow(query):
    # First pass: task planning and correction
    state = WorkflowState(query=query)
    planning_result = planning_node(state)
    reflection_result = reflection_node(planning_result)
    
    # Filter out empty and refinement tasks
    valid_tasks = [task for task in reflection_result.tasks if task.strip() and task != 'Refined task example']
    
    # Execute valid tasks
    if valid_tasks:
        execution_state = WorkflowState(query="", tasks=valid_tasks)
        final_result = execution_node(execution_state)
        return final_result.results if hasattr(final_result, 'results') else []
    return []

if __name__ == "__main__":
    query = input("Enter your query: ")
    results = run_langgraph_workflow(query)
    for item in results:
        print(f"Task: {item['task']}\nResult: {item['result']}\n")