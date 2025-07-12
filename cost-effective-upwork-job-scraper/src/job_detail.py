"""
Logic to scrape individual Upwork job details.
"""
from bs4 import BeautifulSoup, Tag

async def parse_job_detail(html: str):
    """
    Parses the full job detail page HTML and returns a dict with all required fields.
    """
    soup = BeautifulSoup(html, "html.parser")
    
    # Extract job title - try multiple selectors
    job_title = None
    title_selectors = [
        "h1[data-test='job-title']",
        "h1.job-title",
        "h1",
        "[data-test='job-title']"
    ]
    for selector in title_selectors:
        title_elem = soup.select_one(selector)
        if title_elem:
            job_title = title_elem.get_text(strip=True)
            break
    
    # Extract description - try multiple selectors
    description = None
    desc_selectors = [
        "[data-test='job-description-text']",
        ".job-description",
        ".description",
        "[data-test='job-description']"
    ]
    for selector in desc_selectors:
        desc_elem = soup.select_one(selector)
        if desc_elem:
            description = desc_elem.get_text(strip=True)
            break
    
    # Extract category
    category = None
    cat_selectors = [
        "a[data-test='job-category']",
        ".job-category",
        "[data-test='job-category']"
    ]
    for selector in cat_selectors:
        cat_elem = soup.select_one(selector)
        if cat_elem:
            category = cat_elem.get_text(strip=True)
            break
    
    # Extract client location
    client_location = None
    loc_selectors = [
        "strong[data-test='client-location']",
        ".client-location",
        "[data-test='client-location']"
    ]
    for selector in loc_selectors:
        loc_elem = soup.select_one(selector)
        if loc_elem:
            client_location = loc_elem.get_text(strip=True)
            break
    
    # Extract client details
    client_details = {}
    client_selectors = {
        "totalSpent": ["span[data-test='client-spend']", ".client-spend"],
        "jobsPosted": ["span[data-test='client-jobs-posted']", ".client-jobs-posted"],
        "hireRate": ["span[data-test='client-hire-rate']", ".client-hire-rate"]
    }
    
    for key, selectors in client_selectors.items():
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                client_details[key] = elem.get_text(strip=True)
                break
    
    # Extract budget
    budget = None
    budget_selectors = [
        "span[data-test='job-budget']",
        ".job-budget",
        "[data-test='job-budget']"
    ]
    for selector in budget_selectors:
        budget_elem = soup.select_one(selector)
        if budget_elem:
            budget = budget_elem.get_text(strip=True)
            break
    
    # Extract project type
    project_type = None
    proj_selectors = [
        "span[data-test='job-type']",
        ".job-type",
        "[data-test='job-type']"
    ]
    for selector in proj_selectors:
        proj_elem = soup.select_one(selector)
        if proj_elem:
            project_type = proj_elem.get_text(strip=True)
            break
    
    # Extract posted time
    posted_time = None
    posted_selectors = [
        "span[data-test='job-posted']",
        ".job-posted",
        "[data-test='job-posted']"
    ]
    for selector in posted_selectors:
        posted_elem = soup.select_one(selector)
        if posted_elem:
            posted_time = posted_elem.get_text(strip=True)
            break
    
    # Extract skills
    skills = []
    skill_selectors = [
        "a[data-test='job-skill']",
        ".job-skill",
        "[data-test='job-skill']",
        ".skill-tag"
    ]
    for selector in skill_selectors:
        skill_elems = soup.select(selector)
        for skill_elem in skill_elems:
            skill_text = skill_elem.get_text(strip=True)
            if skill_text and skill_text not in skills:
                skills.append(skill_text)
        if skills:  # If we found skills with this selector, break
            break
    
    # Extract jobId from meta or URL
    job_id = None
    meta_id = soup.find("meta", {"name": "upwork:job_id"})
    if isinstance(meta_id, Tag):
        job_id = meta_id.get("content")
    
    # If no job_id from meta, try to extract from URL
    if not job_id:
        # Look for job ID in the page URL or other elements
        url_elem = soup.find("link", {"rel": "canonical"})
        if url_elem and isinstance(url_elem, Tag):
            url = url_elem.get("href", "")
            if isinstance(url, str) and "~" in url:
                job_id = url.split("~")[-1].split("/")[0]
    
    return {
        "jobTitle": job_title,
        "description": description,
        "category": category,
        "clientLocation": client_location,
        "clientDetails": client_details,
        "budget": budget,
        "projectType": project_type,
        "postedTime": posted_time,
        "skillsRequired": skills,
        "jobId": job_id,
    } 