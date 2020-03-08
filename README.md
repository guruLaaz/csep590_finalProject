# NHL Fantasy Draft

**Running the code:**

```shell script
python main.py

# more options:
python main.py --help
```

**Downloading data:**

Downloads fantasy data for a given year (default 2019) and stores it in `data` directory.

- Prereqs:
    ```shell script
    pip install requests
    ```
- Running the script:
    ```shell script
    python download_data.py --help
    ```

**Adding new strategies:**
1. Implement `Strategy` by adding a new file in `./strategies`
2. Modify `./data/teams.txt` file