import json
import os
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP
mcp = FastMCP("BugClassifierServer")

# WINDOWS FIX: Get the absolute path to the directory where THIS script is located
# This ensures the 'data' folder is found no matter how the script is called.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

@mcp.tool()
def get_team_directory() -> str:
    """Read the team.json file and return the developer directory."""
    path = os.path.join(DATA_DIR, "team.json")
    # WINDOWS FIX: Always use encoding="utf-8" to avoid crash on special characters
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@mcp.tool()
def get_severity_rules() -> str:
    """Read the rules.md file and return the severity guidelines."""
    path = os.path.join(DATA_DIR, "rules.md")
    # WINDOWS FIX: Always use encoding="utf-8"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@mcp.tool()
def save_bug_report(content: str) -> str:
    """Save the final classified bug report to a local text file."""
    output_path = os.path.join(DATA_DIR, "classified_bugs.txt")
    with open(output_path, "a", encoding="utf-8") as f:
        f.write(f"\n--- NEW CLASSIFICATION ---\n{content}\n")
    return f"Successfully saved report to {output_path}"

if __name__ == "__main__":
    mcp.run()
