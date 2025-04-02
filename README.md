# TimeLogix

TimeLogix is a modern, intuitive time tracking application designed to help contractors log and manage their working hours effectively. This tool was created to keep proper track of time worked, ensuring accurate record-keeping and easy export of session data for billing, reporting, and invoice generation.

## Features

-   **Start/Stop Tracking:** Easily log your work sessions with start and stop buttons.
-   **Session Logging:** View session start times, end times, and durations in H:MM:SS format.
-   **Project Management:** Assign time entries to specific projects.
-   **CSV Export:** Export session data to a CSV file for further processing or reporting.
-   **PDF Invoice Generation:** Generate professional PDF invoices based on logged time entries.
-   **Customizable Settings:** Configure company and client information, along with an hourly rate, for accurate invoice generation.
-   **Modern UI:** Built using CustomTkinter for a sleek and user-friendly experience.
-   **Scrollable Interface:** Ensures all elements are accessible, even on smaller screens.

## Requirements

-   Python 3.x
-   CustomTkinter: `pip install customtkinter`
-   reportlab: `pip install reportlab`
-   csv (Included with Python)
-   tkinter (Included with Python)

## Installation

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/blakeridgway/time_logix.git
    cd time_logix
    ```

2.  **(Optional) Create and Activate a Virtual Environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
   or

    ```bash
    pip install customtkinter reportlab
    ```

## Usage

Run the application using Python:

```bash
python time_logix.py
```

### How to Use

1.  **Start Tracking:**

    *   Click the **Start** button to begin tracking your work session.

2.  **Stop Tracking:**

    *   Click the **Stop** button to end the session. The application will log the start and end times and calculate the duration.

3.  **Enter Task Description and Project:**

    *   Provide a brief description of the work completed and select the appropriate project from the dropdown menu.

4.  **Add New Project:**

    *   Enter a new project name in the "New Project" field and click "Add Project". The new project will be added to the project dropdown.

5.  **Export Data:**

    *   Click the "Export to CSV" button to save your session data to a CSV file ("working\_sessions.csv").
    *   Click the "Export to PDF" button to generate an invoice as a PDF file (named "invoice\_\*.pdf", where \* is the incrementing invoice number).

6.  **Update Settings:**

    *   Fill out the company name, company address, client name, client address, and hourly rate fields.
    *   Click "Update Settings" to save these values. These settings will be used when generating PDF invoices.

7.  **Calculate Total Time:**

    *   Click "Calculate Total Time" to display the sum of all recorded session durations.

8.  **Exit:**

    *   Click "Exit" to close the application.

## Contributing

Contributions are welcome! Feel free to fork the repository, make changes, and submit pull requests. For any major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please contact [blake@blakeridgway.com](mailto:blake@blakeridgway.com).
