"""
Logic to scrape individual Upwork job details.
"""
from bs4 import BeautifulSoup
from bs4 import Tag

async def parse_job_detail(html: str):
    """
    Parses the full job detail page HTML and returns a dict with all required fields.
    """
    soup = BeautifulSoup(html, "html.parser")
    # Extract job title
    job_title = soup.find("h1", {"data-test": "job-title"})
    job_title = job_title.get_text(strip=True) if job_title else None
    # Extract description
    desc = soup.find("div", {"data-test": "job-description-text"})
    description = desc.get_text(strip=True) if desc else None
    # Extract category
    category = None
    cat_tag = soup.find("a", {"data-test": "job-category"})
    if cat_tag:
        category = cat_tag.get_text(strip=True)
    # Extract client location
    client_location = None
    loc_tag = soup.find("strong", {"data-test": "client-location"})
    if loc_tag:
        client_location = loc_tag.get_text(strip=True)
    # Extract client details
    client_details = {}
    spent = soup.find("span", {"data-test": "client-spend"})
    jobs_posted = soup.find("span", {"data-test": "client-jobs-posted"})
    hire_rate = soup.find("span", {"data-test": "client-hire-rate"})
    if spent:
        client_details["totalSpent"] = spent.get_text(strip=True)
    if jobs_posted:
        client_details["jobsPosted"] = jobs_posted.get_text(strip=True)
    if hire_rate:
        client_details["hireRate"] = hire_rate.get_text(strip=True)
    # Extract budget
    budget = None
    budget_tag = soup.find("span", {"data-test": "job-budget"})
    if budget_tag:
        budget = budget_tag.get_text(strip=True)
    # Extract project type
    project_type = None
    proj_type_tag = soup.find("span", {"data-test": "job-type"})
    if proj_type_tag:
        project_type = proj_type_tag.get_text(strip=True)
    # Extract posted time
    posted_time = None
    posted_tag = soup.find("span", {"data-test": "job-posted"})
    if posted_tag:
        posted_time = posted_tag.get_text(strip=True)
    # Extract skills
    skills = [s.get_text(strip=True) for s in soup.find_all("a", {"data-test": "job-skill"})]
    # Extract jobId (from meta or url, fallback to None)
    job_id = None
    meta_id = soup.find("meta", {"name": "upwork:job_id"})
    if isinstance(meta_id, Tag):
        job_id = meta_id.get("content")
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