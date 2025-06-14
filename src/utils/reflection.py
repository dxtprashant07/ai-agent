def log_feedback(feedback):
    # Function to log feedback for reflection
    with open('feedback_log.txt', 'a') as f:
        f.write(feedback + '\n')

def assess_performance(agent_name, performance_metrics):
    # Function to assess the performance of an agent
    print(f"Performance metrics for {agent_name}:")
    for metric, value in performance_metrics.items():
        print(f"{metric}: {value}")

def handle_error(error_message):
    # Function to handle errors and log them
    with open('error_log.txt', 'a') as f:
        f.write(error_message + '\n')
    print(f"Error logged: {error_message}")