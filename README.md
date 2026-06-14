# 🛠️ Custom SEO & Web Automations

A collection of automated scripts and GitHub Actions workflows designed to monitor web health and track SEO performance.

---

## 🗂️ Project Structure

The repository is organized into independent, modular automation tools:

*   **`automations/`**: Core directory containing the automation tools.
    *   `broken_link_checker/`: Scans websites to detect and report dead or broken links.
    *   `keyword_ranking_tracker/`: Tracks search engine keyword positions over time.
*   **`.github/workflows/`**: CI/CD workflows to run these automations on a schedule via GitHub Actions.

---

## 🚀 Features & Modules

### 🔗 1. Broken Link Checker
Scans target URLs to find broken links (404s, timeouts, etc.) and generates clean reports.
*   **Outputs:** Generates both `broken_links_report.csv` and `broken_links_report.html` for easy viewing.
*   **Configuration:** Managed via `automations/broken_link_checker/config.yaml`.

### 📈 2. Keyword Ranking Tracker
Monitors search engine ranking performance for a predefined list of target keywords.
*   **Keywords:** Managed via `automations/keyword_ranking_tracker/keywords.txt`.
*   **Configuration:** Managed via `automations/keyword_ranking_tracker/config.yaml`.

---

## ⚙️ Setup & Installation

Each tool operates independently with its own dependencies. 

1. **Clone the repository:**
```bash
   git clone [https://github.com/itusebastian/your-repo-name.git](https://github.com/itusebastian/your-repo-name.git)
   cd your-repo-name
