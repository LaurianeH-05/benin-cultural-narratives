# Community Adaptation Guide  
**Empowering Local Narrative Audits**  

## 1. Configure Your Analysis  
Edit `config_template.yml`:  
```yaml  
target:  
  base_url: "YOUR_TARGET_BASE_URL/page/{}/"  # e.g., "https://example.com/news/culture/page/{}/"  
  html_selectors:  
    article: "article"                 # HTML container for articles  
    title: ["h2", "entry-title"]       # Title element (tag + class)  
    date: ["time", "entry-date"]       # Date element  
    content: ["div", "entry-content"]  # Article body text  

terms:  
  traditional: "term_lists/traditional_terms.txt"  
  modern: "term_lists/modern_terms.txt"  

visualization:  
  colors:  
    traditional: "#008751"  # Green for traditional themes  
    modern: "#FFD100"       # Yellow for modern themes  
    other: "#E8112D"        # Red for uncategorized  
```  

## 2. Customize Term Lists  
Edit these files in `/term_lists`:  
- **Add/remove terms** reflecting your community’s cultural context  
- **Preserve formatting**: One term per line, UTF-8 encoding  

## 3. Run Analysis  
```bash  
# Install dependencies  
pip install -r ../requirements.txt  

# Scrape articles (adjust --pages as needed)  
python scraper_template.py --pages 5  

# Generate visualizations  
python analysis_template.py  
```  

## 4. Customize Visuals (Optional)  
Modify `analysis_template.py` to:  
- Adjust `width`/`height` in `WordCloud()`  
- Edit chart titles/labels for your cultural context  
- Add new visualizations (e.g., sentiment over time)  

---