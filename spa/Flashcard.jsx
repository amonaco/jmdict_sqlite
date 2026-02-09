import { useEffect, useState } from "react";
import { apiFetch } from "./api";

export default function Flashcard() {
  const [card, setCard] = useState(null);
  const userId = localStorage.getItem("user_id");

  const loadCard = async () => {
    const data = await apiFetch(`/flashcard/${userId}/N5`);
    setCard(data);
  };

  const answer = async (correct) => {
    await apiFetch("/answer", {
      method: "POST",
      body: JSON.stringify({
        user_id: userId,
        entry_id: card.entry_id,
        correct,
      }),
    });
    loadCard();
  };

  useEffect(() => {
    loadCard();
  }, []);

  if (!card) return <div>Loading...</div>;

  return (
    <div>
      <h2>Flashcard</h2>
      <p>{card.question}</p>

      <button onClick={() => answer(true)}>Correct</button>
      <button onClick={() => answer(false)}>Wrong</button>
    </div>
  );
}
