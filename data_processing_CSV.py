import pandas as pd  # noqa: F401
import numpy as np  # noqa: F401

# These options ensure that no columns are cut, aka that all data are visible
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


def create_dataframe_from_csv(file_path):
    # Load CSV file into a DataFrame
    # data_local = pd.read_csv(file_path)
    try:
        data_local = pd.read_csv(file_path, encoding='ISO-8859-1', delimiter=',',nrows=100, on_bad_lines='skip')  # Try common encoding, csv seems to be uncommonly encoded
        # erstmal nur 100 Zeilen einlesen
    except UnicodeDecodeError as e:
        print(f"Error when reading the file: {e}")
        return None
    except pd.errors.ParserError as e:
        print(f"ParserError: {e}")
        return None

    # Print columns to verify they are correct
    print("Columns in CSV-file:", data_local.columns.tolist())
    """print("First 5 rows of the DataFrame:")
    print(data_local.head())"""

    # Initialize an empty list to store the data
    rows_local = []

    # Iterate through each row in the CSV file
    for index_local, row_local in data_local.iterrows():
        # Extract relevant data
        try:
            # Extrahieren der relevanten Daten
            gvkey_local = row_local.get('gvkey', np.nan)  # Identifier
            conm_local = row_local.get('conm', np.nan)  # Company Name
            datadate_local = pd.to_datetime(row_local.get('datadate', ''), dayfirst=True).strftime(
                '%m/%Y') if row_local.get('datadate', '') else np.nan
            revtq_local = row_local.get('revtq', np.nan)  # Revenue quarterly, must be transformed to monthly
            actq_local = row_local.get('actq', np.nan)  # Current assets quarterly
            atq_local = row_local.get('atq', np.nan)  # Total assets quarterly
            ceqq_local = row_local.get('ceqq', np.nan)  # Common equity quarterly
            ltq_local = row_local.get('ltq', np.nan)  # Long-Term debt quarterly
            gsector_local = row_local.get('gsector', np.nan)  # Industry sector (1st level)
            ggroup_local = row_local.get('ggroup', np.nan)  # Industry group  (2nd level)
            gind_local = row_local.get('gind', np.nan)  # Specific industry group (3rd level)
            priusa_local = row_local.get('priusa', np.nan)
            prirow_local = row_local.get('prirow', np.nan)
            loc_local = row_local.get('loc', np.nan)  # Location --> use later to separate Stoxx and S&P
            curcdq_local = row_local.get('curcdq', np.nan)  # Currency

            # Create a dictionary for each row
            row_dict_local = {
                'gvkey': gvkey_local,
                'conm': conm_local,
                'datadate': datadate_local,
                'e_score': None,  # Placeholder for E-Score
                'revtq': revtq_local,
                'actq': actq_local,
                'atq': atq_local,
                'ceqq': ceqq_local,
                'ltq': ltq_local,
                'lev': None,  # Placeholder for leverage
                'gsector': gsector_local,
                'ggroup': ggroup_local,
                'gind': gind_local,
                'priusa': priusa_local,
                'prirow': prirow_local,
                'loc': loc_local,
                'curcdq': curcdq_local
            }

            # Append the dictionary to the list
            rows_local.append(row_dict_local)

        except Exception as e:
            print(f"Issue in row {index_local}: {e}")
            continue

    # Create a DataFrame from the list of dictionaries
    df_local = pd.DataFrame(rows_local)

    return df_local


def add_employee_data(df_local, emp_file_path):
    # load CSV-file with employee numbers
    emp_data = pd.read_csv(emp_file_path, encoding='ISO-8859-1', delimiter=',')

    # only extract year from this CSV since it contains only annual data & will be matched annually to existing df
    emp_data['year'] = pd.to_datetime(emp_data['datadate'], dayfirst=True).dt.year

    # Datumsangaben im bestehenden DataFrame ebenfalls auf Jahr umstellen
    df_local['year'] = pd.to_datetime(df_local['datadate'], format='%m/%Y').dt.year

    # Merge employee numbers based on gvkey and year
    df_local = df_local.merge(emp_data[['gvkey', 'year', 'emp']], on=['gvkey', 'year'], how='left')

    return df_local


