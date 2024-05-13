## Visual Assistance
This is a voice-activated visual assistance application that uses speech recognition and object detection to provide help in various situations. The application listens for specific keywords and performs actions accordingly. It can describe the surroundings, send help messages, and more.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
- Python 3.8 or higher
- An Azure API Key for the speech recognition feature
- An OpenAI API Key for the text-to-speech feature

### Installing
1. Clone the repository to your local machine.
2. Install the required Python packages by running the following command in your terminal:
```bash
pip install -r requirements.txt
```
3. Set up your environment variables in a .env file. You will need to provide your Azure API Key and OpenAI API Key.

### Usage
Run the main.py file to start the application. The application will start listening for the following keywords:

- "start": Starts the application.
- "stop": Stops the application.
- "describe": Describes the surroundings using the object detection feature.
- "help": Sends a help message.

### Code Structure
- `main.py`: The main entry point of the application.
- `app/`: Contains utility functions and classes.
- `model_data/`: Contains the object detection model and related code.
- `audio/`: Contains audio files generated by the application.
- `images/`: Contains image files used by the application.
`model_data/`: Contains the object detection code.

## Contributing

First off, thank you for considering contributing to this project! It's people like you that make this project such a great tool.

### Code of Conduct
This project and everyone participating in it is governed by the Code of Conduct. By participating, you are expected to uphold this code.

### How Can I Contribute?
**Reporting Bugs**
- Ensure the bug was not already reported by searching on GitHub under [Issues](https://github.com/DeepeshKalura/vision-assistance/issues).

- If you're unable to find an open issue addressing the problem, open a new one. Be sure to include a title and clear description, as much relevant information as possible, and a code sample or an executable test case demonstrating the expected behavior that is not occurring.

**Suggesting Enhancements**
If you have a suggestion that is not a bug and may add something new to the project, you can open an issue in the same way as you would report a bug.

### Pull Requests
- Fork the repository and create your branch from main.
- If you've added code that should be tested, add tests.
- If you've changed APIs, update the documentation.
- Ensure the test suite passes.
Make sure your code lints.
- Issue that pull request!

### Styleguides
**Git Commit Messages**
- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

**Python Styleguide**
All Python must adhere to PEP 8.

### Thank You
Your contributions to the community are greatly appreciated. Every little bit helps and credit will always be given.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.