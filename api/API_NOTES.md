Typical Flow
1. Create User

POST /users?name=John

2. Get Flashcard

GET /flashcard/1/N5

3. Answer

POST /answer?user_id=1&entry_id=100&correct=true

Next Upgrades (Easy)

Join kanji, reading, gloss

Spaced repetition (SM-2)

Difficulty weights

Multiple choice generation

Auth tokens

Audio pronunciation

“Due cards” query

Right now it’s a clean backend skeleton that scales well.
