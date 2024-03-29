# gcp-spanner-python
Python examples for Google Cloud Spanner


# Features
You can do the followings with it:

## Transaction type
 - List out...
 - Updates

# How to set up demo?
You can run the demo locally with a few easy steps.

1. Clone the repository

```bash
git clone https://github.com/DataElevated/gcp-spanner-python.git
```

2. Create Anaconda Python Environment

```bash
conda create --name gcp-spanner-python --clone base
```

3. Activate the environment

```bash
conda activate gcp-spanner-python
```

4. Install dependencies

```bash
pip install -r requirements.txt
```

4. Create `.env` file in root and add your variables

```bash
-- TODO
```

5. Run the app

```bash

```

That's All!!! Now open [localhost:3000](http://localhost:3000/) to see the app.

# Built With
- [Anaconda Python](https://www.anaconda.com/products/individual?modal=nucleus): Python environment for data engineering and data science. 

# License
This project is licensed under the MIT License - see the [`LICENSE`](LICENSE) file for details.

# Upcoming Features
Demo has the potentials to grow further. Here are some of the upcoming features planned(not in any order):

- ✔️ Add the ability to time different transactions.
- ✔️ Add the ability to create sample data.

# PowerShell and Google SDK
## In SDK
gsutil ls -lR gs://ddoctest/data/1-staged/Production/Transactions |findstr TOTAL

## PowerShell
PS E:\Project\Spanner\Phase1\Data\1-staged\Production\Transactions> (Get-ChildItem -File *.csv | Measure-Object).Count