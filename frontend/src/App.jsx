import { useEffect, useState } from "react";

export default function App() {
  const [items, setItems] = useState([]);
  const [name, setName] = useState("");
  const [error, setError] = useState(null);

  async function load() {
    try {
      const res = await fetch("/api/items");
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setItems(await res.json());
      setError(null);
    } catch (e) {
      setError(e.message);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function add(e) {
    e.preventDefault();
    if (!name.trim()) return;
    await fetch("/api/items", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    });
    setName("");
    load();
  }

  async function remove(id) {
    await fetch(`/api/items/${id}`, { method: "DELETE" });
    load();
  }

  return (
    <main style={{ maxWidth: 480, margin: "3rem auto", fontFamily: "system-ui" }}>
      <h1>Items</h1>
      {error && <p style={{ color: "crimson" }}>API error: {error}</p>}
      <form onSubmit={add}>
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="New item"
        />
        <button type="submit">Add</button>
      </form>
      <ul>
        {items.map((i) => (
          <li key={i.id}>
            {i.name} <button onClick={() => remove(i.id)}>x</button>
          </li>
        ))}
      </ul>
    </main>
  );
}
