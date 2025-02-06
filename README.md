# KatStalker

A Telegram bot designed to track the progress of students solving problems on [Kattis](https://open.kattis.com/) for a competitive programming course at Rey Juan Carlos University. Developed by the student association **Dijkstraidos**, this bot automates progress monitoring and sends updates via Telegram.

## Features ✨

- **Automatic Progress Tracking**: Scrapes Kattis affiliation pages to monitor student rankings and scores.
- **Real-Time Notifications**: Sends Telegram notifications for:
  - New users joining the affiliation.
  - Score increases or decreases.
  - Rank changes.
- **MongoDB Integration**: Stores chat and affiliation data for persistent tracking.
- **Modular Job System**: Easily extendable with custom jobs (e.g., `Scores` job for score updates).

## Installation 💻

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Dijkstraidos/kattis-telegram-bot.git
   cd kattis-telegram-bot
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the root directory with the following variables:
   ```ini
   DATABASE_URI=mongodb+srv://user:password@your-mongodb-uri
   DATABASE_NAME=katstalker
   TELEGRAM_TOKEN=your-telegram-bot-token
   JOBS=Scores  # Semi-colon separated list of jobs (e.g., "Scores;AnotherJob")
   DEBUG=False   # Set to True for debug mode
   ```

4. **Setup a job (optional)**
   
   Can create cronjob in a server to run this script periodically. You can also use [this GitHub Actions workflow](.github/workflows/main.yml) as a template to schedule this script at most every 5 minutes (GitHub Actions limitation).

## Configuration ⚙️

| Environment Variable | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `DATABASE_URI`       | MongoDB connection URI (e.g., `mongodb+srv://user:pass@cluster.example.com`). |
| `DATABASE_NAME`      | Name of the MongoDB database (default: `katstalker`).                       |
| `TELEGRAM_TOKEN`     | Token for your Telegram bot (obtain via [BotFather](https://t.me/BotFather)).|
| `JOBS`               | Enabled jobs (e.g., `Scores`). Multiple jobs are separated by `;`.          |
| `DEBUG`              | Enable debug logging (`True`/`False`).                                      |

## Usage 🚀

1. **Run the Bot**:
   ```bash
   python app/main.py
   ```

2. **Configure Affiliations**:
   - Add your Kattis affiliation URLs to the `affiliations` field in the MongoDB `chats` collection.
   - Example document in `chats` collection:
     ```json
     {
       "chat_id": "TELEGRAM_CHAT_ID",
       "affiliations": [
         { "url": "https://open.kattis.com/affiliation/your-affiliation-name" }
       ]
     }
     ```
   - Yuo can how your own MongoDB database using [MongoDB Cloud Services](https://cloud.mongodb.com) for free.

3. **Receive Updates**:
   The bot will automatically scrape Kattis and send updates to the configured Telegram chat.

## Project Structure 📁

```
.
├── app/
│   ├── app.py           # Main application logic
│   ├── db.py            # MongoDB database interactions
│   ├── logger.py        # Logging utilities
│   ├── main.py          # Entry point
│   ├── scrapper.py      # Kattis web scraper
│   ├── telegram.py      # Telegram message sender
│   └── jobs/
│       ├── factory.py   # Job factory
│       ├── job.py       # Base Job class
│       └── scores.py    # Scores update job logic
└── requirements.txt     # Python dependencies
```

## Contributing 🤝

Contributions are welcome! Follow these steps:
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit your changes: `git commit -m "Add your feature"`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Open a pull request.

## License 📄

Licensed under the [GNU General Public License v3.0](./LICENSE).

## Acknowledgments 🙏

- **Dijkstraidos**, the student association of Rey Juan Carlos University.
- **GRAFO**, a research group of Rey Juan Carlos Univserty collaborating in the course.
