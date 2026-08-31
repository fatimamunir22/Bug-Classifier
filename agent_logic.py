import asyncio
import ollama
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_classification_agent(user_input):
    # Get absolute paths to avoid Windows "File Not Found" errors
    python_exe = sys.executable 
    # Get the directory where THIS script is
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(current_dir, "mcp_server.py")
    
    server_params = StdioServerParameters(
        command=python_exe,
        args=[script_path],
        env=os.environ.copy() 
    )

    try:
        # On Windows, sometimes initialization takes a second
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                # Call Tools
                team_info = await session.call_tool("get_team_directory", {})
                rules = await session.call_tool("get_severity_rules", {})

                prompt = f"""
                You are an expert Bug Triage Agent at HUBBLE42.
                TEAM DIRECTORY: {team_info.content}
                SEVERITY RULES: {rules.content}
                BUG DESCRIPTION: {user_input}
                """

                response = ollama.chat(model='llama3', messages=[
                    {'role': 'user', 'content': prompt}
                ])

                await session.call_tool("save_bug_report", {"content": response['message']['content']})
                return response['message']['content']

    except Exception as e:
        # THIS IS IMPORTANT: It will now tell us exactly what is wrong
        import traceback
        error_details = traceback.format_exc()
        print(error_details) # Check your terminal for this!
        return f"Error connecting to MCP Server: {str(e)}"

if __name__ == "__main__":
    # Test it in terminal
    test_input = "The login button is broken"
    print(asyncio.run(run_classification_agent(test_input)))
