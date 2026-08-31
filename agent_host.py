import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import ollama

# 1. Setup the connection to your local MCP server
server_params = StdioServerParameters(
    command="python3",
    args=["mcp_server.py"], # This tells the agent to run your server script
)

async def run_agent():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # The "Bug Report" we want to classify (You can change this later)
            # user_input = "The login button is completely unresponsive on Safari mobile and it keeps throwing a 500 error when I click it."
            # Instead of a hardcoded string, ask the user for input
            print("\n--- ALGO BUG CLASSIFIER ---")
            user_input = input("Paste the bug description here and press Enter: ")

            # Fetch context from our MCP Server (The "Tools")
            team_info = await session.call_tool("get_team_directory", {})
            rules = await session.call_tool("get_severity_rules", {})

            # The "Persona" / Instructions for Llama 3
            prompt = f"""
            You are an expert Bug Triage Agent at ALGO.
            Use the following context to classify the bug report:
            
            TEAM DIRECTORY:
            {team_info.content}
            
            SEVERITY RULES:
            {rules.content}
            
            BUG DESCRIPTION:
            {user_input}
            
            Please provide:
            1. Affected Area
            2. Suggested Severity (P0-P3)
            3. Assigned Developer
            4. Reasoning (Short explanation)
            """

            # Send everything to Llama 3 (Ollama)
            response = ollama.chat(model='llama3', messages=[
                {'role': 'user', 'content': prompt}
            ])

            print("\n--- AI AGENT BUG CLASSIFICATION ---")
            print(response['message']['content'])

            # Optional: Save the result using our MCP Tool
            await session.call_tool("save_bug_report", {"content": response['message']['content']})

if __name__ == "__main__":
    asyncio.run(run_agent())