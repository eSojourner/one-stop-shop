# Program Description
---
This program was designed to facilitate sermon translation from English to Spanish. It has four different modes of operation: 
1. **One-Stop-Shop**: intakes English .mp3 file, produces an English transcript (.txt file), a Spanish translation (.txt file), narrates the Spanish translation (.mp3 file)
2. **Translation and Narration**: intakes English .txt file, produces Spanish translation, narrates Spanish translation
3. **Translation** only
4. **Narration** only

It uses OpenAI's whisper library to transcribe, a locally hosted Ollama model to translate, and a text-to-speech library that uses Google Translate (gTTS)

# Upcoming Features 
---
- programmatic formatting of transcripts into Word documents
- local text-to-speech narration that supports voice cloning 
