from agents.planAgent import PlanAgent
from agents.toolAgent import ToolAgent
from workflow.pipeline import Pipeline, AgenticWorkflow

def main():
    # Initialize agents
    plan_agent = PlanAgent()
    tool_agent = ToolAgent()
    
    # Set up the workflow pipeline
    pipeline = Pipeline(plan_agent, tool_agent)
    
    # User input loop
    while True:
        user_query = input("Enter your query (or type 'exit' to quit): ")
        if user_query.lower() == 'exit':
            break
        
        # Process the user query through the pipeline
        result = pipeline.run(user_query)
        
        # Display the result
        print("Result:", result)

if __name__ == "__main__":
    # For testing the agentic workflow end-to-end with a sample query
    workflow = AgenticWorkflow()
    query = "Find the weather, Summarize the news, Calculate 2+2"
    results = workflow.run(query)
    for item in results:
        print(f"Task: {item['task']}\nResult: {item['result']}\n")
    
    # Uncomment the following line to run the main user input loop
    # main()