
# Django Q&A App

A question and answer application built with Django, designed to facilitate community-driven knowledge sharing.

## Features

- Users can post questions and provide answers.
- Voting system for questions and answers.
- Search functionality to find relevant content.
- User profiles with activity tracking.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/marcinnowakowski/django-qna-mit.git
   cd django-qna-mit
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**

   ```bash
   python3 manage.py migrate
   ```

5. **Create a superuser (optional):**

   ```bash
   python3 manage.py createsuperuser
   ```

6. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

   Access the application at `http://127.0.0.1:8000/`.

## Usage

- **Post a Question:** Navigate to the "Ask Question" page, fill in the details, and submit.
- **Answer a Question:** Browse questions, select one, and provide your answer in the response section.
- **Vote:** Use the upvote/downvote buttons to rate questions and answers.
- **Search:** Enter keywords in the search bar to find relevant questions and answers.

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository.**
2. **Create a new branch:**

   ```bash
   git checkout -b feature-name
   ```

3. **Make your changes and commit them:**

   ```bash
   git commit -m 'Add new feature'
   ```

4. **Push to the branch:**

   ```bash
   git push origin feature-name
   ```

5. **Create a pull request.**

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Inspired by various Q&A platforms.
- Built with [Django](https://www.djangoproject.com/).
