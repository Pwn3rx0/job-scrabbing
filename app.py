import csv
import io
import random
import time

import requests
import streamlit as st
from bs4 import BeautifulSoup


st.set_page_config(page_title="LinkedIn Jobs Scraper", page_icon="💼", layout="centered")

st.title("💼 LinkedIn Jobs Scraper")
st.write("اكتب اسم الوظيفة اللي عايز تدور عليها، واختار المكان وعدد الصفحات، واضغط بحث.")

# ============================================================
#   نموذج الإدخال
# ============================================================
with st.form("search_form"):
    keywords_input = st.text_input(
        "اسم الوظيفة (أو أكتر من وظيفة مفصولة بفاصلة)",
        placeholder="Data Analyst, Python Developer",
    )
    location = st.text_input("المكان", value="Egypt")
    pages_per_keyword = st.slider(
        "عدد الصفحات لكل وظيفة (كل صفحة ~25 وظيفة)",
        min_value=1,
        max_value=10,
        value=4,
    )
    submitted = st.form_submit_button(" ندوس بحث يخويا ؟")

# ============================================================
#   دالة السكرابنج
# ============================================================
def scrape_linkedin_jobs(keywords, location, pages_per_keyword, progress_callback=None):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/126.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    all_jobs = []
    seen_job_ids = set()

    total_steps = len(keywords) * pages_per_keyword
    step = 0

    for keyword in keywords:
        for page in range(pages_per_keyword):
            step += 1
            if progress_callback:
                progress_callback(
                    step / total_steps,
                    f"بيدور على '{keyword}' - صفحة {page + 1}/{pages_per_keyword}",
                )

            start = page * 25
            url = (
                "https://www.linkedin.com/jobs-guest/jobs/api/"
                f"seeMoreJobPostings/search?keywords={keyword}"
                f"&location={location}&start={start}"
            )

            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code != 200:
                    break

                soup = BeautifulSoup(response.content, "html.parser")
                job_cards = soup.find_all("li")
                if not job_cards:
                    break

                for card in job_cards:
                    link_elem = card.find("a", class_="base-card__full-link")
                    if not link_elem:
                        continue

                    job_link = link_elem["href"].split("?")[0]
                    job_id = (
                        job_link.split("-")[-1]
                        if "-" in job_link
                        else job_link.split("/")[-1]
                    )

                    if job_id in seen_job_ids:
                        continue
                    seen_job_ids.add(job_id)

                    title_elem = card.find("h3", class_="base-search-card__title")
                    title = title_elem.text.strip() if title_elem else "N/A"

                    company_elem = card.find("h4", class_="base-search-card__subtitle")
                    company = company_elem.text.strip() if company_elem else "N/A"

                    location_elem = card.find("span", class_="job-search-card__location")
                    loc = location_elem.text.strip() if location_elem else "N/A"

                    date_elem = card.find("time")
                    post_date = (
                        date_elem["datetime"]
                        if date_elem and date_elem.has_attr("datetime")
                        else (date_elem.text.strip() if date_elem else "N/A")
                    )

                    all_jobs.append(
                        {
                            "Job ID": job_id,
                            "Category Keyword": keyword,
                            "Job Title": title,
                            "Company": company,
                            "Location": loc,
                            "Post Date": post_date,
                            "Job Link": job_link,
                        }
                    )

                time.sleep(random.uniform(1.0, 2.0))

            except Exception:
                break

    return all_jobs


# ============================================================
#   تنفيذ البحث
# ============================================================
if submitted:
    keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]

    if not keywords:
        st.error("اكتب اسم وظيفة واحدة على الأقل.")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()

        def update_progress(fraction, message):
            progress_bar.progress(fraction)
            status_text.text(message)

        with st.spinner("جاري البحث..."):
            jobs = scrape_linkedin_jobs(keywords, location, pages_per_keyword, update_progress)

        progress_bar.empty()
        status_text.empty()

        if not jobs:
            st.warning("مفيش نتائج. جرب كلمة بحث تانية أو قلل عدد الصفحات.")
        else:
            st.success(f"تم العثور على {len(jobs)} وظيفة")

            st.dataframe(jobs, use_container_width=True)

            # تجهيز ملف CSV للتحميل
            fieldnames = [
                "Job ID",
                "Category Keyword",
                "Job Title",
                "Company",
                "Location",
                "Post Date",
                "Job Link",
            ]
            csv_buffer = io.StringIO()
            writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(jobs)

            safe_keyword = keywords[0].lower().replace(" ", "_")
            st.download_button(
                label="⬇ تحميل النتائج CSV",
                data=csv_buffer.getvalue().encode("utf-8-sig"),
                file_name=f"linkedin_jobs_{safe_keyword}_dataset.csv",
                mime="text/csv",
            )
