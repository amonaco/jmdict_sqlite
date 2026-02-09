import { useState } from "react";
import Login from "./Login";
import Flashcard from "./Flashcard";

export default function App() {
  const [logged, setLogged] = useState(
    !!localStorage.getItem("token")
  );

  return (
    <div>
      <h1>JLPT Flashcards</h1>
      {logged ? (
        <Flashcard />
      ) : (
        <Login onLogin={() => setLogged(true)} />
      )}
    </div>
  );
}
