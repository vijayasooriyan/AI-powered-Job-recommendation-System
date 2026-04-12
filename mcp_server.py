from mcp.server.fastmcp import FastMCP
from src.job_api import fetch_linkedin_jobs
from src.job_api import fetch_naukri_jobs

mcp = FastMCP("Job Recommender MCP")

@mcp.tool()
async def fetch_linkedin(listofkey):
    return fetch_linkedin_jobs(listofkey)

@mcp.tool()
async def fetch_naukri(listofkey):
    return fetch_naukri_jobs(listofkey)

if __name__ == "__main__":
    mcp.run(transport='stdio')

