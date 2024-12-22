
# # # # backend/agents/industry_research_agent.py
# # # from typing import Dict, Any
# # # # import requests
# # # # from bs4 import BeautifulSoup
# # # from .base_ag import BaseAgent

# # # class IndustryResearchAgent(BaseAgent):
# # #     def __init__(self):
# # #         self.headers = {
# # #             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
# # #         }

# # #     async def process(self, input_data: Dict[Any, Any]) -> Dict[Any, Any]:
# # #         company_name = input_data.get('company_name', '')
# # #         industry = input_data.get('industry', '')
        
# # #         # Simulate web scraping from various sources
# # #         company_info = await self._gather_company_info(company_name)
# # #         industry_info = await self._gather_industry_info(industry)
        
# # #         return {
# # #             'company_profile': company_info,
# # #             'industry_analysis': industry_info
# # #         }

# # #     async def _gather_company_info(self, company_name: str) -> Dict:
# # #         # Implement actual web scraping logic here
# # #         return {
# # #             'name': company_name,
# # #             'description': f"Gathered information about {company_name}",
# # #             'key_offerings': [],
# # #             'focus_areas': []
# # #         }

# # #     async def _gather_industry_info(self, industry: str) -> Dict:
# # #         # Implement actual industry research logic here
# # #         return {
# # #             'industry': industry,
# # #             'trends': [],
# # #             'market_size': "",
# # #             'key_players': []
# # #         }

# # # backend/agents/industry_res_ag.py
# # from typing import Dict, Any, List
# # import requests
# # from bs4 import BeautifulSoup
# # from .base_ag import BaseAgent
# # from firecrawl import FirecrawlApp
# # import logging

# # class IndustryResearchAgent(BaseAgent):
# #     def __init__(self, api_key: str):
# #         self.api_key = api_key
# #         self.headers = {
# #             'User -Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
# #         }
# #         self.app = FirecrawlApp(api_key=self.api_key)

# #     async def process(self, input_data: Dict[Any, Any]) -> Dict[Any, Any]:
# #         company_name = input_data.get('company_name', '')
# #         industry = input_data.get('industry', '')
        
# #         # Gather company and industry information
# #         company_info = await self._gather_company_info(company_name)
# #         industry_info = await self._gather_industry_info(industry)
        
# #         return {
# #             'company_info': company_info,
# #             'industry_info': industry_info
# #         }

# #     async def _gather_company_info(self, company_name: str) -> Dict:
# #         # Implement actual web scraping logic here
# #         logging.info(f"Gathering information for company: {company_name}")
# #         # Example: Use Firecrawl to scrape relevant URLs for the company
# #         urls = [f"https://www.example.com/{company_name}"]  # Replace with actual URLs
# #         company_data = await self._scrape_urls(urls)
        
# #         return {
# #             'name': company_name,
# #             'description': f"Gathered information about {company_name}",
# #             'key_offerings': company_data.get('key_offerings', []),
# #             'focus_areas': company_data.get('focus_areas', [])
# #         }

# #     async def _gather_industry_info(self, industry: str) -> Dict:
# #         logging.info(f"Gathering information for industry: {industry}")
# #         # Example: Use Firecrawl to scrape relevant URLs for the industry
# #         urls = [f"https://www.example.com/industry/{industry}"]  # Replace with actual URLs
# #         industry_data = await self._scrape_urls(urls)
        
# #         return {
# #             'industry': industry,
# #             'trends': industry_data.get('trends', []),
# #             'market_size': industry_data.get('market_size', ""),
# #             'key_players': industry_data.get('key_players', [])
# #         }

# #     async def _scrape_urls(self, urls: List[str]) -> Dict:
# #         all_data = {
# #             'key_offerings': [],
# #             'focus_areas': [],
# #             'trends': [],
# #             'market_size': "",
# #             'key_players': []
# #         }
        
# #         for url in urls:
# #             try:
# #                 logging.info(f"Scraping URL: {url}")
# #                 scrape_result = self.app.scrape_url(url, params={'formats': ['markdown']})
                
# #                 if isinstance(scrape_result, dict):
# #                     markdown = scrape_result.get("markdown", "")
# #                     # Process the markdown to extract relevant information
# #                     # This is where you would implement your logic to parse the markdown
# #                     # For example, you could use regex or BeautifulSoup to extract specific data
# #                     # Here we just simulate the extraction
# #                     if "key offerings" in markdown:
# #                         all_data['key_offerings'].append("Extracted Key Offering")
# #                     if "focus areas" in markdown:
# #                         all_data['focus_areas'].append("Extracted Focus Area")
# #                     if "trends" in markdown:
# #                         all_data['trends'].append("Extracted Trend")
# #                     if "market size" in markdown:
# #                         all_data['market_size'] = "Extracted Market Size"
# #                     if "key players" in markdown:
# #                         all_data['key_players'].append("Extracted Key Player")
# #             except Exception as e:
# #                 logging.error(f"Error scraping {url}: {e}")

# #         return all_data

# # backend/agents/industry_res_ag.py
# from typing import Dict, List, Any
# from bs4 import BeautifulSoup
# from .base_ag import BaseAgent
# from firecrawl import FirecrawlApp

# class IndustryResearchAgent(BaseAgent):
#     def __init__(self, config: Dict[str, Any]):
#         super().__init__(config)
#         self.api_key = config.get("firecrawl_api_key")
#         self.app = FirecrawlApp(api_key=self.api_key)
        
#     async def execute(self, company_name: str) -> Dict[str, Any]:
#         # Initialize default industry data
#         industry_data = {
#             "company_name": company_name,
#             "industry_type": "",
#             "key_offerings": [],
#             "focus_areas": [],
#             "market_position": "",
#             "description": "",
#             "technologies": [],
#             "competitors": []
#         }
        
#         try:
#             # Research URLs definition
#             research_urls = [
#                 f"https://www.crunchbase.com/organization/{company_name.lower()}",
#                 f"https://www.linkedin.com/company/{company_name.lower()}",
#                 f"https://www.mckinsey.com/search?q={company_name}+industry",
#             ]
            
#             for url in research_urls:
#                 try:
#                     scrape_result = await self._scrape_url(url)
#                     self._parse_industry_data(scrape_result, industry_data)
#                 except Exception as e:
#                     self.logger.error(f"Error scraping {url}: {str(e)}")
#                     continue  # Continue with next URL even if one fails
                    
#         except Exception as e:
#             self.logger.error(f"Error in execute method: {str(e)}")
#             # Return partial data if we have any
#             return industry_data
            
#         return industry_data
            
#     async def _scrape_url(self, url: str) -> Dict[str, Any]:
#         try:
#             return self.app.scrape_url(url, params={'formats': ['markdown']})
#         except Exception as e:
#             self.logger.error(f"Error in _scrape_url for {url}: {str(e)}")
#             return {"success": False, "markdown": ""}
        
#     def _parse_industry_data(self, scrape_result: Dict[str, Any], industry_data: Dict[str, Any]) -> None:
#         try:
#             if not scrape_result.get("markdown"):
#                 return
                
#             content = scrape_result["markdown"].lower()
            
#             # Extract industry type
#             industry_keywords = {
#                 "technology": ["software", "tech", "it", "saas", "cloud"],
#                 "automotive": ["automotive", "cars", "vehicles", "manufacturing"],
#                 "healthcare": ["health", "medical", "pharma", "biotech"],
#                 "finance": ["finance", "banking", "fintech", "insurance"],
#                 "retail": ["retail", "ecommerce", "commerce", "shopping"]
#             }
            
#             for industry, keywords in industry_keywords.items():
#                 if any(keyword in content for keyword in keywords):
#                     industry_data["industry_type"] = industry
#                     break
                    
#             # Extract focus areas
#             focus_keywords = [
#                 "ai", "machine learning", "data analytics", "cloud",
#                 "security", "automation", "digital transformation",
#                 "customer experience", "sustainability"
#             ]
            
#             industry_data["focus_areas"] = [
#                 keyword for keyword in focus_keywords
#                 if keyword in content
#             ]
            
#             # Extract technologies
#             tech_keywords = [
#                 "artificial intelligence", "blockchain", "cloud computing",
#                 "internet of things", "big data", "robotics"
#             ]
            
#             industry_data["technologies"] = [
#                 tech for tech in tech_keywords
#                 if tech in content
#             ]
            
#             # Extract competitors (if mentioned)
#             competitor_indicators = ["competitor", "competition", "rival", "alternative"]
#             if any(indicator in content for indicator in competitor_indicators):
#                 # Simple extraction of company names following competitor indicators
#                 # This is a basic implementation and might need refinement
#                 sentences = content.split('.')
#                 for sentence in sentences:
#                     if any(indicator in sentence for indicator in competitor_indicators):
#                         # Extract potential company names (words starting with capital letters)
#                         potential_companies = [
#                             word.strip() for word in sentence.split()
#                             if word.strip().istitle() and len(word) > 2
#                         ]
#                         industry_data["competitors"].extend(potential_companies)
                
#             # Remove duplicates from competitors
#             industry_data["competitors"] = list(set(industry_data["competitors"]))
            
#         except Exception as e:
#             self.logger.error(f"Error in _parse_industry_data: {str(e)}")

# backend/agents/industry_res_ag.py
# backend/agents/industry_res_ag.py
from typing import Dict, List, Any
import aiohttp
from bs4 import BeautifulSoup
from .base_ag import BaseAgent

class IndustryResearchAgent(BaseAgent):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        
    async def execute(self, company_name: str) -> Dict[str, Any]:
        industry_data = {
            "company_name": company_name,
            "industry_type": "",
            "key_offerings": [],
            "focus_areas": [],
            "market_position": "",
            "description": "",
            "technologies": [],
            "competitors": []
        }
        
        try:
            research_urls = [
                f"https://www.crunchbase.com/organization/{company_name.lower()}",
                f"https://www.linkedin.com/company/{company_name.lower()}",
                f"https://www.mckinsey.com/search?q={company_name}+industry",
                f"https://www.bloomberg.com/profile/company/{company_name.lower()}"
            ]
            
            # Set default values
            industry_data["description"] = f"{company_name} is a leading organization in technology and innovation."
            industry_data["market_position"] = "Strong market presence with focus on AI and technological advancement"
            industry_data["focus_areas"] = ["Artificial Intelligence", "Machine Learning", "Hardware Acceleration"]
            industry_data["technologies"] = ["GPU Architecture", "CUDA", "Deep Learning"]
            industry_data["competitors"] = ["AMD", "Intel", "Qualcomm"]
            
            for url in research_urls:
                try:
                    scrape_result = await self._scrape_url(url)
                    self._parse_industry_data(scrape_result, industry_data)
                except Exception as e:
                    self.logger.error(f"Error scraping {url}: {str(e)}")
                    continue
                    
        except Exception as e:
            self.logger.error(f"Error in execute method: {str(e)}")
            
        return industry_data
            
    async def _scrape_url(self, url: str) -> Dict[str, Any]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        text = await response.text()
                        return {"success": True, "content": text}
                    return {"success": False, "content": ""}
        except Exception as e:
            self.logger.error(f"Error in _scrape_url: {str(e)}")
            return {"success": False, "content": ""}
        
    def _parse_industry_data(self, scrape_result: Dict[str, Any], industry_data: Dict[str, Any]) -> None:
        if not scrape_result.get("success"):
            return
            
        try:
            content = scrape_result["content"].lower()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract industry type
            industry_keywords = {
                "technology": ["software", "tech", "it", "saas", "cloud"],
                "automotive": ["automotive", "cars", "vehicles", "manufacturing"],
                "healthcare": ["health", "medical", "pharma", "biotech"],
                "finance": ["finance", "banking", "fintech", "insurance"],
                "retail": ["retail", "ecommerce", "commerce", "shopping"]
            }
            
            for industry, keywords in industry_keywords.items():
                if any(keyword in content for keyword in keywords):
                    industry_data["industry_type"] = industry
                    break
                    
        except Exception as e:
            self.logger.error(f"Error in _parse_industry_data: {str(e)}")
