# 🚀 Google Form AutoFill and Submit

This script automates the process of filling and submitting Google Forms. It's customizable and supports multiple field types, making repetitive submissions effortless.

## How to Use

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script:
   ```bash
   python main.py <google-form-url>
   ```
   - Use `-r` to only fill required fields:
     ```bash
     python main.py <google-form-url> -r
     ```

## Limitations

- Works only for non-authenticated Google Forms.
- Doesn't support file uploads.
- Works only on single section forms

## Credits

Developed by Nauman Sajjad.

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Contributions

Contributions are welcome! Feel free to fork the repo and submit a pull request.
