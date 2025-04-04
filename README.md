# Translate SRT

This is an example implementation for translating .srt files using the ChatGPT API.

## Setup

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/).

2. Clone this repository.

3. Install the requirements:

   ```bash
   $ pip install openai
   $ pip install asyncio
   ```

4. Define your [API key](https://beta.openai.com/account/api-keys).

   ```bash
   $ export OPENAI_API_KEY=...
   ```

5. Define your languages.

   ```bash
   $ export SOURCE_LANGUAGE="English"
   $ export TARGET_LANGUAGE="Korean"
   ```

6. Obtain the source subtitles and save it as `input.srt`.

7. Run the app:

   ```bash
   $ python run.py

8. The translated subtitle file is generated as `output.srt`.
