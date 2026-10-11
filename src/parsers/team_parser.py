"""
Corporate Team, Executive Bio, and Competencies Extractor.
Follows the Zero Snippet Policy: captures complete competence and practice area blocks.
"""

import re
from bs4 import BeautifulSoup
from typing import List
from models import TeamMember

COMPETENCE_HEADERS = [
    "kompetens", "verksamhetsområden", "verksamhetsomraden",
    "expertis", "area of practice", "practice areas",
    "specialties", "inriktning", "specialisering"
]

class TeamBioParser:
    def __init__(self, html_content: str):
        self.soup = BeautifulSoup(html_content, "html.parser")

    def extract_members(self) -> List[TeamMember]:
        """
        Extracts individual executive and team profiles from team roster cards or bio pages.
        """
        members: List[TeamMember] = []

        # Find person cards or structured blocks
        candidate_blocks = self.soup.find_all(
            ["div", "article", "section", "li"],
            class_=re.compile(r"person|team|member|employee|staff|card|profile|medarbetare|advokat", re.I)
        )

        for block in candidate_blocks:
            # 1. Extract Name (often in h2, h3, h4, or strong)
            name_el = block.find(["h2", "h3", "h4", "h5", "strong", "a"], class_=re.compile(r"name|title|heading", re.I))
            if not name_el:
                name_el = block.find(["h2", "h3", "h4"])
            
            if not name_el:
                continue

            name = name_el.get_text(strip=True)
            if not name or len(name.split()) < 2 or len(name) > 60:
                continue

            # 2. Extract Title / Role
            title = None
            title_el = block.find(class_=re.compile(r"title|role|position|befattning|yrke", re.I))
            if title_el and title_el != name_el:
                title = title_el.get_text(strip=True)

            # 3. Extract Email (mailto)
            email = None
            mail_link = block.find("a", href=re.compile(r"^mailto:", re.I))
            if mail_link:
                email = mail_link["href"].replace("mailto:", "").split("?")[0].strip()

            # 4. Extract Phone (tel)
            phone = None
            tel_link = block.find("a", href=re.compile(r"^tel:", re.I))
            if tel_link:
                phone = tel_link["href"].replace("tel:", "").strip()

            # 5. Extract Full Competence Block (Zero Snippet Policy)
            competencies = []
            for header_kw in COMPETENCE_HEADERS:
                header_el = block.find(lambda tag: tag.name in ["h3", "h4", "h5", "strong", "p", "div"] and header_kw in tag.get_text().lower())
                if header_el:
                    # Look for following ul or container
                    parent_container = header_el.find_parent(["div", "section"]) or block
                    list_items = parent_container.find_all("li")
                    for li in list_items:
                        item_text = li.get_text(strip=True)
                        if item_text and item_text not in competencies:
                            competencies.append(item_text)

            # Bio text summary
            bio_text = None
            p_tags = block.find_all("p")
            for p in p_tags:
                txt = p.get_text(strip=True)
                if len(txt) > 30 and (not title or txt != title):
                    bio_text = txt
                    break

            members.append(TeamMember(
                name=name,
                title=title,
                email=email,
                phone=phone,
                bio_summary=bio_text,
                competencies=competencies
            ))

        # Deduplicate by name
        unique_members = []
        seen = set()
        for m in members:
            if m.name.lower() not in seen:
                seen.add(m.name.lower())
                unique_members.append(m)

        return unique_members
