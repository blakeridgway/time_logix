# TimeLogix

TimeLogix is a simple, intuitive Tkinter-based time tracking application designed to help contractors log and manage their working hours effectively. This tool was created so I could keep proper track of time worked under a contract for a company, ensuring accurate record-keeping and easy export of session data for billing and reporting purposes.

## Features

- **Start/Stop Tracking:** Easily log your work sessions with start and stop buttons.
- **Session Logging:** View session start times, end times, and durations both in \(H:MM:SS\) and decimal hours.
- **CSV Export:** Export your session data to a CSV file for further processing or billing.
- **Simple UI:** A clean and minimal user interface built using Tkinter.

## Requirements

- Python 3.x
- Tkinter (usually included with standard Python installations)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/timelogix.git
   cd timelogix
   ```

2. **(Optional) Create and Activate a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**

   There are no additional dependencies beyond the Python Standard Library. However, ensure you have the latest version of Python installed.

## Usage

Run the application using Python:

```bash
python time_logix.py
```

### How to Use

1. **Start Tracking:**
   - Click the **Start Tracking** button to log the starting time of your work session.
2. **Stop Tracking:**
   - Click the **Stop Tracking** button to end the session. The app will display and log the duration in both formats, e.g., `1:30:00` and `1.50 hours`.
3. **Export Sessions:**
   - Once you’re finished working, click the **Export Sessions** button to save your session data into `working_sessions.csv`.

## Customizations

- **Decimal Hours:** The app calculates hours worked in decimal format using a helper function.
- **CSV File Export:** Sessions are exported to a CSV file with headers: `Start Time`, `End Time`, `Duration (H:MM:SS)`, and `Decimal Hours`.

## Contributing

Contributions are welcome! Feel free to fork the repository, make changes, and submit pull requests. For any major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please contact [blake@blakeridgway.com](mailto:blake@blakeridgway.com).
