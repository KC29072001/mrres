
# # main.py
# from fastapi import FastAPI, HTTPException
# from typing import Dict, Any
# from backend.agents.industry_res_ag import IndustryResearchAgent
# from backend.agents.usecase_gen_ag import UseCaseGeneratorAgent
# from backend.agents.resource_col_ag import ResourceCollectorAgent
 

# app = FastAPI()

# @app.post("/analyze")
# async def analyze_company(request: Dict[str, Any]):
#     try:
#         # Extract input data
#         company_name = request.get("company_name")
#         industry = request.get("industry")

#         if not company_name or not industry:
#             raise HTTPException(status_code=400, detail="Company name and industry are required")

#         # Initialize agents
#         research_agent = IndustryResearchAgent()
#         usecase_agent = UseCaseGeneratorAgent()
#         resource_agent = ResourceCollectorAgent()

#         # Execute research pipeline
#         research_results = await research_agent.process({
#             'company_name': company_name,
#             'industry': industry
#         })

#         usecase_results = await usecase_agent.process({
#             'industry_data': research_results['industry_analysis'],
#             'company_data': research_results['company_profile']
#         })

#         resource_results = await resource_agent.process({
#             'use_cases': usecase_results['use_cases']
#         })

#         return {
#             **research_results,
#             **usecase_results,
#             **resource_results
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from backend.agents.industry_res_ag import IndustryResearchAgent
from backend.agents.usecase_gen_ag import UseCaseGenerationAgent
from backend.agents.resource_col_ag import ResourceCollectionAgent
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Request model
class CompanyRequest(BaseModel):
    company_name: str
    industry: str

# Initialize configuration
def get_config():
    return {
        "firecrawl_api_key": os.getenv("FIRECRAWL_API_KEY"),
        "kaggle_api_key": os.getenv("KAGGLE_API_KEY"),
        "github_token": os.getenv("GITHUB_TOKEN")
    }

# @app.post("/analyze")
# async def analyze_company(request: CompanyRequest):
#     try:
#         # Get configuration
#         config = get_config()
        
#         # Initialize agents with config
#         industry_agent = IndustryResearchAgent(config)
#         usecase_agent = UseCaseGenerationAgent(config)
#         resource_agent = ResourceCollectionAgent(config)

#         # Execute research pipeline
#         industry_data = await industry_agent.execute(request.company_name)
        
#         # Combine industry data with user-provided industry
#         industry_data["industry_type"] = request.industry
        
#         # Generate use cases based on industry data
#         use_case_data = await usecase_agent.execute(industry_data)
        
#         # Collect resources for the use cases
#         resource_data = await resource_agent.execute(use_case_data["use_cases"])

#         # Structure the response according to frontend expectations
#         response = {
#             "company_profile": {
#                 "name": request.company_name,
#                 "description": industry_data.get("description", ""),
#                 "focus_areas": industry_data.get("focus_areas", []),
#                 "technologies": industry_data.get("technologies", [])
#             },
#             "industry_analysis": {
#                 "industry_type": request.industry,
#                 "market_position": industry_data.get("market_position", ""),
#                 "key_trends": use_case_data.get("market_standards", []),
#                 "competitors": industry_data.get("competitors", [])
#             },
#             "use_cases": [
#                 {
#                     "title": use_case["name"],
#                     "description": use_case.get("description", ""),
#                     "benefits": use_case.get("benefits", []),
#                     "implementation_complexity": use_case.get("complexity", "Medium")
#                 }
#                 for use_case in use_case_data["use_cases"]
#             ],
#             "resources": [
#                 {
#                     "use_case": use_case["name"],
#                     "datasets": [
#                         {
#                             "name": dataset["name"],
#                             "url": dataset["url"]
#                         }
#                         for dataset in resource_data.get("datasets", [])
#                         if dataset.get("use_case_id") == use_case.get("id")
#                     ],
#                     "github_repos": [
#                         {
#                             "name": repo["name"],
#                             "url": repo["url"]
#                         }
#                         for repo in resource_data.get("code_repositories", [])
#                         if repo.get("use_case_id") == use_case.get("id")
#                     ]
#                 }
#                 for use_case in use_case_data["use_cases"]
#             ]
#         }

#         return response

#     except Exception as e:
#         # Log the error for debugging
#         import logging
#         logging.error(f"Error processing request: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))

# backend/main.py changes:
@app.post("/analyze")
async def analyze_company(request: CompanyRequest):
    try:
        config = get_config()
        
        # Initialize agents
        industry_agent = IndustryResearchAgent(config)
        usecase_agent = UseCaseGenerationAgent(config)
        resource_agent = ResourceCollectionAgent(config)

        # Execute pipeline
        industry_data = await industry_agent.execute(request.company_name)
        
        # Add user-provided industry
        if request.industry:
            industry_data["industry_type"] = request.industry
            
        # Generate use cases
        use_case_data = await usecase_agent.execute(industry_data)
        
        # Collect resources
        resource_data = await resource_agent.execute(use_case_data["use_cases"])

        return {
            "company_profile": {
                "name": request.company_name,
                "description": industry_data.get("description", ""),
                "focus_areas": industry_data.get("focus_areas", []),
                "technologies": industry_data.get("technologies", [])
            },
            "industry_analysis": {
                "industry_type": request.industry,
                "market_position": industry_data.get("market_position", ""),
                "key_trends": use_case_data.get("market_standards", []),
                "competitors": industry_data.get("competitors", [])
            },
            "use_cases": [
                {
                    "title": use_case["name"],
                    "description": use_case.get("description", ""),
                    "benefits": use_case.get("benefits", []),
                    "implementation_complexity": use_case.get("complexity", "Medium")
                }
                for use_case in use_case_data["use_cases"]
            ],
            "resources": resource_data
        }

    except Exception as e:
        import logging
        logging.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)