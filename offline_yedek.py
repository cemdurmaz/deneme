"""Ollama çalışmazsa sınıf tartışması için SADECE anahtar-kelime araması.
UYARI: Bu program embedding, RAG veya LangChain işlemi yapmaz.
"""
from pathlib import Path
from quality_utils import lexical_score
from config import DATA_DIR

if __name__ == "__main__":
    question = input("Soru: ") or "Kütüphane hafta içi kaçta kapanır?"
    docs = []
    for path in sorted(DATA_DIR.glob("*.txt")):
        txt = path.read_text(encoding="utf-8")
        docs.append((lexical_score(question, txt), path.name, txt))
    print("ÇEVRİMDIŞI YEDEK / YALNIZCA KELİME BENZERLİĞİ")
    for score, source, content in sorted(docs, reverse=True)[:3]:
        print(round(score, 3), source, content[:145].replace("\n", " "))
