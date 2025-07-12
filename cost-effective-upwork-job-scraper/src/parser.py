"""
BeautifulSoup scraping logic for Upwork job listings.
"""
from bs4 import BeautifulSoup

async def parse_job_listings(html: str):
    """
    Parses the job listings from the search results HTML.
    Returns a list of job summary dicts (with jobLink, jobTitle, etc.).
    """
    soup = BeautifulSoup(html, "html.parser")
    jobs = []
    
    # Find all job tiles based on the actual Upwork structure
    job_tiles = soup.find_all("article", {"data-test": "JobTile"})
    
    for job_tile in job_tiles:
        # Extract job title and link
        title_link = job_tile.find("a", {"data-test": "job-tile-title-link"})
        if not title_link:
            continue
            
        job_title = title_link.get_text(strip=True)
        job_link = "https://www.upwork.com" + title_link.get("href", "")
        
        # Extract job ID from the data-test-key attribute
        job_id = job_tile.get("data-test-key")
        
        # Extract posted time
        posted_time_elem = job_tile.find("small", {"data-test": "job-pubilshed-date"})
        posted_time = None
        if posted_time_elem:
            time_text = posted_time_elem.get_text(strip=True)
            if "Posted" in time_text:
                posted_time = time_text.replace("Posted", "").strip()
        
        # Extract budget/project type
        job_type_elem = job_tile.find("li", {"data-test": "job-type-label"})
        budget = None
        project_type = None
        if job_type_elem:
            type_text = job_type_elem.get_text(strip=True)
            if "Hourly:" in type_text:
                project_type = "Hourly"
                budget = type_text.replace("Hourly:", "").strip()
            elif "Fixed price" in type_text:
                project_type = "Fixed-Price"
                # Look for budget in the next li element
                budget_elem = job_tile.find("li", {"data-test": "is-fixed-price"})
                if budget_elem:
                    budget_text = budget_elem.get_text(strip=True)
                    if "Est. budget:" in budget_text:
                        budget = budget_text.replace("Est. budget:", "").strip()
        
        # Extract experience level
        experience_elem = job_tile.find("li", {"data-test": "experience-level"})
        experience_level = experience_elem.get_text(strip=True) if experience_elem else None
        
        # Extract skills/tokens
        skills = []
        token_buttons = job_tile.find_all("button", {"data-test": "token"})
        for token in token_buttons:
            skill_text = token.get_text(strip=True)
            if skill_text and skill_text != "+1" and skill_text != "+2":
                skills.append(skill_text)
        
        jobs.append({
            "jobTitle": job_title,
            "jobLink": job_link,
            "jobId": job_id,
            "postedTime": posted_time,
            "budget": budget,
            "projectType": project_type,
            "experienceLevel": experience_level,
            "skillsRequired": skills,
        })
    
    return jobs 