import requests
from bs4 import BeautifulSoup
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
from stop_words import get_stop_words
import matplotlib.pyplot as plt
import time

BENIN_COLORS = {
    "traditional": "#008751",
    "modern": "#FFD100",
    "other": "#E8112D"
}

def scrape_ortb_culture(num_pages=10):
    base_url = "https://www.srtb.bj/category/culture/page/{}/"
    articles = []

    for page in range(1, num_pages+1):
        time.sleep(1)
        url = base_url.format(page)
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            for article in soup.find_all("article"):
                try:
                    title_tag = article.find("h2", class_="entry-title")
                    title = title_tag.find("a").text.strip() if title_tag and title_tag.find("a") else "No Title"
                    article_url = title_tag.find("a")["href"] if title_tag and title_tag.find("a") else "#"

                    date_tag = article.find("time", class_="entry-date")
                    raw_date = date_tag.text.strip() if date_tag else "Unknown"
                    from dateutil.parser import parse
                    try:
                        parsed_date = parse(raw_date, dayfirst=True, fuzzy=True)
                    except:
                        parsed_date = pd.NaT

                    preview_tag = article.find("div", class_="entry-content")
                    preview = preview_tag.text.strip() if preview_tag else "No Preview"

                    articles.append({
                        "title": title,
                        "url": article_url,
                        "date": parsed_date,
                        "preview": preview,
                        "raw_date": raw_date
                    })
                except AttributeError as e:
                    print(f"Skipping article due to missing elements: {str(e)}")
                    continue
                
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve page {page}: {str(e)}")
            continue

    print(f"Successfully scraped {len(articles)} articles")
    return pd.DataFrame(articles)

culture_df = scrape_ortb_culture(5)
print(culture_df[['title', 'date']].head())

culture_df.to_csv("benin_cultural_articles.csv", index=False, encoding="utf-8-sig")

print(f"Scraped {len(culture_df)} articles")
print("Sample data:\n", culture_df[["date", "title"]].head())


text = " ".join(culture_df["title"] + " " + culture_df["preview"])
text = text.lower().replace("é", "e").replace("è", "e")

french_stopwords = get_stop_words('fr')
custom_stopwords = {
    'title', 'affiche', 'mai', 'dimanche', 'japon', 'osaka', 'eteint', 
    'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi',
    'janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet',
    'août', 'septembre', 'octobre', 'novembre', 'décembre',
    'après', 'plus', 'comme', 'fait', 'sous'
}

all_stopwords = set(STOPWORDS).union(set(french_stopwords).union(set(custom_stopwords)))

text = " ".join(culture_df["title"] + " " + culture_df["preview"])
text = text.replace("Lire la suite", "").replace("\n", " ")


traditional_terms = ["vodun", "festival", "patrimoine", "masques", "ouidah"]
modern_terms = ["numérique", "jeunesse", "technologie"]
traditional_terms += ["tradition", "ancêtre", "rite"]
modern_terms += ["digital", "startup", "innovation"]


wc = WordCloud(
    width=1200,
    height=600, 
    background_color="white",
    stopwords=all_stopwords
)
def color_func(word, **kwargs):
    if word.lower() in ["vodun", "patrimoine", "festival", "masques", "ouidah", "bénin", "calavi", "béhanzin", "rite"]:
        return BENIN_COLORS["traditional"]
    elif word.lower() in ["numérique", "jeunesse", "télévision", "audio" ]:
        return BENIN_COLORS["modern"]
    else:
        return BENIN_COLORS["other"]
wc.generate(text)
wc.recolor(color_func=color_func)

traditional_count = sum(text.lower().count(term) for term in traditional_terms)
modern_count = sum(text.lower().count(term) for term in modern_terms)

print(f"\nCultural Narrative Balance:\nTraditional: {traditional_count}\nModern: {modern_count}")

plt.figure(figsize=(15, 8))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.title("Dominant Cultural Narratives in Benin Media", fontsize=20, pad=20)
plt.savefig("benin_culture_wordcloud.png", bbox_inches="tight")


plt.figure(figsize=(8, 6))
plt.bar(["Traditional", "Modern"], [traditional_count, modern_count], 
        color=[BENIN_COLORS["traditional"], BENIN_COLORS["modern"]])
plt.title("Traditional vs Modern Cultural Narratives")
plt.savefig("benin_narrative_balance.png")

if not culture_df["date"].isna().all():
    culture_df["year"] = culture_df["date"].dt.year
    yearly_counts = culture_df["year"].value_counts().sort_index()
    
    if not yearly_counts.empty:
        plt.figure(figsize=(10, 6))
        colors = [BENIN_COLORS["traditional"] if year < 2020 else BENIN_COLORS["modern"] 
                for year in yearly_counts.index]
        
        yearly_counts.plot(
            kind="bar", 
            title="Cultural Coverage Over Time",
            color=colors
        )
        plt.xlabel("Year")
        plt.ylabel("Number of Articles")
        plt.savefig("benin_culture_trends.png")
    else:
        print("No valid dates for temporal analysis")
else:
    print("All dates invalid - skipping temporal chart")