# ♟️ Chess.com Live Tracker (⛔ Project Stopped)

This project is **stopped**. Discord integration required breaking Discord's Terms of Service (self-bot / account token method), so development has been discontinued.

Monitor Chess.com players in real time using Chess.com's internal APIs and RSocket.

This project automatically detects when a player comes online, starts a game, connects to the live game stream, and receives real-time game events. It is an educational reverse engineering project built for research and learning.

## ✅ Completed

* [X] Detect online/offline status
* [X] Detect when a player starts playing
* [X] Automatically fetch live game ID
* [X] Fetch game information
* [X] Detect game variant
* [X] Detect time control
* [X] Connect to Chess.com's RSocket server
* [X] Subscribe to live game events
* [X] Receive raw live event payloads
* [X] Receive raw TCN (Two Character Notation) moves
* [X] Receive player activity events
* [X] Reverse engineer Chess.com's live RSocket protocol
* [X] Discover Chess.com's TCN move format
* [X] MIT Licensed

## ⛔ Why Stopped

Discord Rich Presence needed either:

- Local Discord app (limited features)
- Direct Gateway connection with account token (self-bot — violates Discord ToS)

Since the second method isn't allowed, this project won't continue.

## Project Flow

```text
Player UUID
      │
      ▼
Presence API
      │
      ▼
Playing?
      │
      ▼
Game API
      │
      ▼
RSocket
      │
      ▼
Live Events
      │
      ▼
Raw TCN Moves
```

## Technologies

* Python
* Requests
* aiohttp
* rsocket-py
* Chess.com Internal APIs
* RSocket

## Disclaimer

This project is **not affiliated with Chess.com**. Educational and research only.

## License

MIT Licen

# ♟️ Chess.com Live Tracker

Monitor Chess.com players in real time using Chess.com's internal APIs and RSocket.

This project automatically detects when a player comes online, starts a game, connects to the live game stream, and receives real-time game events. It is an educational reverse engineering project built for research and learning.

## ✅ Completed

* [X] Detect online/offline status
* [X] Detect when a player starts playing
* [X] Automatically fetch live game ID
* [X] Fetch game information
* [X] Detect game variant
* [X] Detect time control
* [X] Connect to Chess.com's RSocket server
* [X] Subscribe to live game events
* [X] Receive raw live event payloads
* [X] Receive raw TCN (Two Character Notation) moves
* [X] Receive player activity events
* [X] Reverse engineer Chess.com's live RSocket protocol
* [X] Discover Chess.com's TCN move format
* [X] MIT Licensed

## 🚧 In Progress

* [ ] Decode TCN using `chess-tcn`
* [ ] Convert TCN to UCI
* [ ] Convert TCN to PGN
* [ ] Display SAN moves (`e4`, `Nf3`, etc.)
* [ ] Build board using `python-chess`
* [ ] Display live FEN
* [ ] Display verified live clocks
* [ ] Parse all RSocket event types
* [ ] Automatic reconnection
* [ ] Improve error handling

## 📌 Planned

* [ ] Detect game finished
* [ ] Export PGN
* [ ] Export JSON
* [ ] Export FEN history
* [ ] Track multiple players
* [ ] Opening detection
* [ ] Game statistics
* [ ] Discord Rich Presence
* [ ] Discord Bot
* [ ] Live board image generation
* [ ] Shareable game snapshots
* [ ] Automatic game screenshots
* [ ] Automatic game archive
* [ ] Unit tests

## Project Flow

```text
Player UUID
      │
      ▼
Presence API
      │
      ▼
Playing?
      │
      ▼
Game API
      │
      ▼
RSocket
      │
      ▼
Live Events
      │
      ▼
Raw TCN Moves
      │
      ▼
TCN Decoder
      │
      ▼
UCI / PGN
      │
      ▼
python-chess
      │
      ▼
Board • FEN • SAN
```

## Technologies

* Python
* Requests
* aiohttp
* rsocket-py
* Chess.com Internal APIs
* RSocket
* chess-tcn
* python-chess

## Installation

```bash
git clone https://github.com/yourusername/chess-live-tracker.git
cd chess-live-tracker

pip install -r requirements.txt

npm install chess-tcn
```

## Future Ideas

* Show your current Chess.com game in Discord Rich Presence.
* Generate a live chess board image after every move.
* Automatically create shareable game snapshots.
* Save completed games with PGN and board images.
* Build integrations for Discord and other community platforms.

## Why this project?

Chess.com does not provide a public API for live games. This project explores Chess.com's internal services to understand how live games work and provides a foundation for building real-time applications, Discord integrations, analytics tools, and protocol research.

## Disclaimer

This project is **not affiliated with Chess.com**. It is an independent educational and research project intended for learning, protocol analysis, and experimentation.

## License

This project is licensed under the **MIT License**.
