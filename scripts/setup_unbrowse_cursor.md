# Unbrowse setup for Cursor

Use these steps to install Unbrowse and add it as a skill in Cursor.

---

## Quick: add Unbrowse skill to Cursor (already have Node/npm)

From the **project root** (or any folder where you want the skill):

```powershell
npx -y skills add unbrowse-ai/unbrowse --yes --agent cursor
```

This installs the Unbrowse skill into `.agents/skills/unbrowse` for Cursor. Then run `unbrowse health` (after global install below) to verify.

---

## Full setup in one go

### 1. Install Unbrowse (global, for repeat use)

```powershell
npm install -g unbrowse@latest
```

### 2. One-time setup (accept ToS when prompted)

```powershell
npx unbrowse setup
```

When you see **"Do you accept the Terms of Service? (y/n):"** type **y** and Enter.

If you get **"Browser engine install failed"**, you can still continue; use the server/API. To skip the browser step next time: `npx unbrowse setup --skip-browser`.

### 3. Add the skill in Cursor

From the project root:

```powershell
npx -y skills add unbrowse-ai/unbrowse --yes --agent cursor
```

Skill is installed at `.agents/skills/unbrowse` and is available to Cursor.

### 4. Check the install

```powershell
unbrowse health
```

Server runs at `http://localhost:6969` when started (see Unbrowse docs).

---

## Upgrade later

```powershell
npm install -g unbrowse@latest
unbrowse setup
```

---

## Non-interactive setup (CI / script)

To avoid the ToS prompt:

```powershell
$env:UNBROWSE_AGENT_EMAIL = "your-email@example.com"
npx unbrowse setup
```

Optional: skip browser engine install:

```powershell
npx unbrowse setup --skip-browser
```

---

## Troubleshooting

- **"Browser engine install failed"**  
  Run with `--skip-browser` to continue without the local browser engine. You can still use the Unbrowse server/API.

- **`unbrowse` command not found after global install**  
  Add npm global bin to PATH: `npm config get prefix` (e.g. `C:\Users\You\AppData\Roaming\npm`); add that path to your system/user PATH.

- **Skill not showing in Cursor**  
  Ensure you ran `npx -y skills add unbrowse-ai/unbrowse --yes --agent cursor` from the project root; the skill lives under `.agents/skills/unbrowse`. Restart Cursor if needed.
