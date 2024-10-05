from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import Counter
from selenium.webdriver.chrome.options import Options

def extract_skills_selenium(freelancer_url, driver):
    driver.get(freelancer_url)
    
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))
        )
        driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()

        skills_elements = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "skill-name d-flex vertical-align-middle air3-token nowrap"))
        )
        
        skills = [skill.text.strip() for skill in skills_elements]
        return skills

    except Exception as  e:
        print("Error extracting skills:")
        print(e)
        return []

def group_skills_selenium(freelancer_urls):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    all_skills = []

    for url in freelancer_urls:
        print(f"Extracting skills from {url}")
        skills = extract_skills_selenium(url, driver)
        all_skills.extend(skills)

    driver.quit()


    skill_counts = Counter(all_skills)

    return skill_counts

# List of freelancer profile URLs
freelancer_urls = [
    "https://www.upwork.com/freelancers/techarchpankaj?referrer_url_path=%2Fnx%2Fsearch%2Ftalent%2F"
    # Add more freelancer URLs here
]

skill_counts = group_skills_selenium(freelancer_urls)

for skill, count in skill_counts.items():
    print(f"{skill}: {count}")
