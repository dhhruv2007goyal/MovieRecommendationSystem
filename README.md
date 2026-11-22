# Movie Recommendation System

A content-based movie recommendation web application built with
**Python** and **Streamlit**. Select a movie to receive five similar
recommendations. The project processes movie metadata, converts it into
text features using `CountVectorizer`, and uses cosine similarity to
identify similar movies.

Movie posters are fetched from the **OMDb API** when an API key is
configured. Recommendations still work without an API key, but real
posters may not load.

## Project structure

Keep the files and folders arranged as follows:

``` text
Movie-Recommendation-System/
│
├── app.py
├── movies.pkl
├── similarity_compressed.pkl
├── requirements.txt
├── requirements-model.txt
├── README.md
│
├── datasets/
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
│
└── notebooks/
    └── model.ipynb
```

### Important files

-   `app.py` --- Streamlit application.
-   `movies.pkl` --- processed movie information, including movie IDs,
    titles and text tags.
-   `similarity_compressed.pkl` --- precomputed cosine-similarity
    matrix.
-   `datasets/` --- original TMDB CSV files used to rebuild the
    processed data and similarity matrix.
-   `notebooks/model.ipynb` --- notebook containing the data
    preprocessing, feature extraction and similarity calculation
    workflow.
-   `requirements.txt` --- dependencies required to run the Streamlit
    application.
-   `requirements-model.txt` --- additional dependencies used for model
    development in the notebook.

Keep both `.pkl` files in the same directory as `app.py`. Keep both CSV
files inside the `datasets/` folder, using the exact filenames shown
above.

## Requirements

-   Python 3 installed.
-   Internet access if you want to fetch movie posters from OMDb.
-   An OMDb API key for real posters (optional).

## Run the application on Windows

1.  Open the project folder in VS Code.

2.  Open **Terminal → New Terminal**. Make sure the terminal is in the
    project root (the folder containing `app.py`).

3.  Create a virtual environment:

    ``` powershell
    py -m venv .venv
    ```

4.  Activate it:

    ``` powershell
    .\.venv\Scripts\Activate.ps1
    ```

    If PowerShell blocks activation, allow it for the current terminal
    session:

    ``` powershell
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    .\.venv\Scripts\Activate.ps1
    ```

    Alternatively, in Command Prompt:

    ``` bat
    .venv\Scripts\activate.bat
    ```

5.  Install the application dependencies:

    ``` powershell
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

6.  (Optional) Set your OMDb API key in the same PowerShell terminal:

    ``` powershell
    $env:OMDB_API_KEY="YOUR_OMDB_API_KEY"
    ```

7.  Run the application:

    ``` powershell
    streamlit run app.py
    ```

## Run the application on macOS

1.  Open the project folder in VS Code.

2.  Open **Terminal → New Terminal**. Make sure the terminal is in the
    project root (the folder containing `app.py`).

3.  Create a virtual environment:

    ``` bash
    python3 -m venv .venv
    ```

4.  Activate it:

    ``` bash
    source .venv/bin/activate
    ```

5.  Install the application dependencies:

    ``` bash
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

6.  (Optional) Set your OMDb API key in the same Terminal session:

    ``` bash
    export OMDB_API_KEY="YOUR_OMDB_API_KEY"
    ```

7.  Run the application:

    ``` bash
    streamlit run app.py
    ```

## Open and stop the application

After starting Streamlit, open the local address printed in the
terminal. It is usually:

<http://localhost:8501>

To stop the application, return to the terminal and press **Ctrl + C**.

When running it again later, activate the virtual environment and set
the OMDb API key again if needed, then run `streamlit run app.py`.

## OMDb API key

The application reads the API key from the `OMDB_API_KEY` environment
variable.

-   Set the variable in the terminal **before** starting Streamlit.
-   The Windows PowerShell and macOS commands above apply only to the
    current terminal session. Set the variable again in a new terminal
    session.
-   Do not hardcode your API key in `app.py` or commit it to Git.
-   If no key is configured, or OMDb does not return a poster for a
    title, the app can still provide recommendations without the real
    poster.

## Rebuild the recommendation data using the notebook

The existing `.pkl` files are already used by the application, so you do
**not** need to run the notebook just to launch the app.

To regenerate the `.pkl` files from the TMDB datasets:

1.  Make sure both CSV files are in `datasets/`:

    -   `tmdb_5000_movies.csv`
    -   `tmdb_5000_credits.csv`

2.  Activate the project's virtual environment.

3.  Install the notebook dependencies:

    ``` bash
    pip install -r requirements-model.txt
    ```

4.  Open `notebooks/model.ipynb` in Jupyter Notebook or VS Code.

5.  Run all cells from top to bottom.

The notebook saves the regenerated `movies.pkl` and
`similarity_compressed.pkl` files in the project root, alongside
`app.py`. **Existing files with these names will be overwritten**, so
make backups first if you want to preserve the current versions.

After the notebook finishes successfully, run the app as described
above.

## How it works

1.  The notebook loads and merges the TMDB movies and credits datasets.
2.  It extracts information such as overview, genres, keywords, cast and
    director.
3.  These fields are combined into text tags and processed.
4.  `CountVectorizer` converts the tags into numerical feature vectors.
5.  Cosine similarity calculates similarity scores between movie pairs.
6.  The resulting movie data and similarity matrix are saved as pickle
    files.
7.  The Streamlit application loads those files and displays the five
    most similar movies for the selected title.

The similarity matrix is precomputed and saved in
`similarity_compressed.pkl`, so the application does not need to
recalculate it every time it starts.
