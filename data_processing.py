import pandas as pd  # noqa: F401
import numpy as np  # noqa: F401


# Function for extracting ESG data from the MS Sustainalytics excel file
def extract_esg_data(file_path, max_companies=3, max_data_points=10):
    # load excel file
    xls = pd.ExcelFile(file_path)
    sheet = xls.parse(xls.sheet_names[0])

    # initialize a list to save data
    data = []

    # variables for loop
    current_company_count = 0
    row_index = 3  # begin at row 5 (index 3, should be 4 but then all data are shifted down 1. Don't know why this
    # works but it does)
    col_index = 1  # begin at column B (index 1) --> B5 is the first ISIN-cell

    while current_company_count < max_companies:
        # read relevant cells
        isin = sheet.iloc[row_index, col_index]  # ISIN in column B (index 1) (Start at B5)
        conm = sheet.iloc[row_index + 1, col_index]  # company name in column B (Start at B6)
        datadate = sheet.iloc[row_index + 2, col_index]  # data of data disclosure in column B (Start at B7)
        e_score = sheet.iloc[row_index + 2, col_index + 1]  # E-score in column C (index 2) (Start at C7)

        # check if cells are empty or contain "-N/A"
        if pd.notna(isin) and "-N/A" not in [isin, e_score]:
            data_points_count = 0
            row_data_index = row_index + 2  # start at first date

            while data_points_count < max_data_points and row_data_index < len(sheet):
                datadate = sheet.iloc[row_data_index, col_index]  # date
                e_score = sheet.iloc[row_data_index, col_index + 1]  # E-Score (column C)

                if pd.notna(datadate) and pd.notna(e_score) and "-N/A" not in [datadate, e_score]:
                    # Handle date conversion
                    try:
                        # Attempt to convert the date assuming it's an Excel date number
                        datadate = pd.to_datetime(datadate, origin='1899-12-30', unit='D')

                        # Check if the conversion was successful
                        if not pd.isna(datadate):
                            formatted_date = datadate.strftime("%m/%Y")
                        else:
                            formatted_date = "Invalid Date"

                    except Exception as e:
                        # In case of any unexpected error during conversion
                        formatted_date = "Invalid Date"
                        print(f"Error converting date: {e}")

                    # Put data in list
                    data.append({
                        "isin": isin,
                        "conm": conm,
                        "datadate": formatted_date,  # formatted as MM/YYYY
                        "e_score": e_score
                    })

                    # íncrease data point counter
                    data_points_count += 1

                # next row for same ISIN
                row_data_index += 1

            # count processed companies
            current_company_count += 1

        # jump to next ISIN, between ISINs there is always one column with the E-scores so skip that
        col_index += 2  # i.e. B -> D -> F and so on

    # create data frame from list
    df = pd.DataFrame(data)
    return df


# Example usage of the function
file_path = 'Data/esg_env_risk_score_ms.xlsx'
df = extract_esg_data(file_path)
print(df)


##### v12 mergen geht nicht

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
        data_local = pd.read_csv(
            file_path,
            encoding='ISO-8859-1',
            delimiter=',',
            nrows=1500,
            on_bad_lines='skip',
            dtype={'gvkey': str, 'isin': str},
        )  # otherwise python cuts gvkey's leading zeros and it might not be unique anymore
        # Try common encoding, csv seems to be uncommonly encoded
    except UnicodeDecodeError as e:
        print(f"Error when reading the file: {e}")
        return None
    except pd.errors.ParserError as e:
        print(f"ParserError: {e}")
        return None


    # Print columns to verify they are correct
    print("Columns in CSV-file:", data_local.columns.tolist())

    # Initialize an empty list to store the data
    rows_local = []

    # Iterate through each row in the CSV file
    for index_local, row_local in data_local.iterrows():
        # Extract relevant data
        try:
            # extraction
            gvkey_local = row_local.get('gvkey', np.nan)  # Identifier
            isin_local = row_local.get('isin', np.nan)  # ISIN, use as identifier to match excel & csv
            conm_local = row_local.get('conm', np.nan)  # Company Name
            datadate_raw = row_local.get('datadate', np.nan)

            # only transform if date is valid
            if pd.notnull(datadate_raw):
                datadate_local = pd.to_datetime(datadate_raw, dayfirst=True).strftime('%m/%Y')
                year_local = pd.to_datetime(datadate_raw, dayfirst=True).year
            else:
                datadate_local = np.nan
                year_local = np.nan
            revtq_local = row_local.get('revtq', np.nan)  # Revenue quarterly, must be transformed to monthly
            actq_local = row_local.get('actq', np.nan)  # Current assets quarterly, must be transformed to monthly
            atq_local = row_local.get('atq', np.nan)  # Total assets quarterly, must be transformed to monthly
            ceqq_local = row_local.get('ceqq', np.nan)  # Common equity quarterly, must be transformed to monthly
            ltq_local = row_local.get('ltq', np.nan)  # Long-Term debt quarterly, must be transformed to monthly
            gsector_local = row_local.get('gsector', np.nan)  # Industry sector (1st level)
            ggroup_local = row_local.get('ggroup', np.nan)  # Industry group  (2nd level)
            gind_local = row_local.get('gind', np.nan)  # Specific industry group (3rd level)
            priusa_local = row_local.get('priusa', np.nan)
            prirow_local = row_local.get('prirow', np.nan)
            loc_local = row_local.get('loc', np.nan)  # Location --> use later to separate Stoxx and S&P
            curcdq_local = row_local.get('curcdq', np.nan)  # Currency

            # Calculation of leverage (Long Term Debt quarterly / common equity quarterly)
            if ceqq_local != 0 and not pd.isna(ceqq_local):
                leverage_local = ltq_local / ceqq_local
            else:
                leverage_local = np.nan

            # Create a dictionary for each row
            row_dict_local = {
                'gvkey': gvkey_local,
                'isin': isin_local,
                'conm': conm_local,
                'datadate': datadate_local,
                'year': year_local,
                'e_score': None,  # Placeholder for E-Score
                'revtq': revtq_local,
                'actq': actq_local,
                'atq': atq_local,
                'ceqq': ceqq_local,
                'ltq': ltq_local,
                'lev': leverage_local,
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
    emp_data = pd.read_csv(emp_file_path, encoding='ISO-8859-1', delimiter=',', dtype={'gvkey': str})

    # only extract year from this CSV since it contains only annual data & will be matched annually to existing df
    emp_data['year'] = pd.to_datetime(emp_data['datadate'], dayfirst=True).dt.year

    # Datumsangaben im bestehenden DataFrame ebenfalls auf Jahr umstellen
    df_local['year'] = pd.to_datetime(df_local['datadate'], format='%m/%Y').dt.year

    # Merge employee numbers based on gvkey and year
    # df_local = df_local.merge(emp_data[['gvkey', 'year', 'emp']], on=['gvkey', 'year'], how='left')
    df_merged = df_local.merge(
        emp_data[['gvkey', 'year', 'emp']],
        on=['gvkey', 'year'],
        how='left'
    )

    return df_merged


def expand_quarterly_to_monthly(df):
    expanded_rows = []
    for _, row in df.iterrows():
        # Iterate over the three months in the quarter
        for month_offset in range(3):
            new_row = row.copy()
            # Adjust the date to the correct month within the quarter
            quarterly_date = pd.to_datetime(row['datadate'], format='%m/%Y')
            monthly_date = quarterly_date + pd.DateOffset(months=month_offset)
            new_row['datadate'] = monthly_date.strftime('%m/%Y')

            # Divide quarterly figures by 3 to approximate monthly data
            new_row['revtq'] = row['revtq'] / 3
            new_row['actq'] = row['actq'] / 3
            new_row['atq'] = row['atq'] / 3
            new_row['ceqq'] = row['ceqq'] / 3
            new_row['ltq'] = row['ltq'] / 3

            expanded_rows.append(new_row)

    # Create a new DataFrame with the expanded data
    df_monthly = pd.DataFrame(expanded_rows)
    return df_monthly


def extract_esg_data(file_path, max_companies=3, max_data_points=12):
    # Load Excel file
    xls = pd.ExcelFile(file_path)
    sheet = xls.parse(xls.sheet_names[0])

    # Initialize a list to store extracted data
    data = []

    # Variables for loop
    current_company_count = 0
    row_index = 3  # begin at row 5 (index 3)
    col_index = 1  # begin at column B (index 1)

    while col_index < sheet.shape[1]:
        # read relevant cells
        isin = sheet.iloc[row_index, col_index]  # ISIN in column B (index 1)
        conm = sheet.iloc[row_index + 1, col_index]  # company name in column B (Start at B6)

        if pd.isna(isin) or pd.isna(conm):
            # Skip if ISIN or company name is missing
            col_index += 2
            continue

        if max_companies is not None and current_company_count >= max_companies:
            break

        data_points_count = 0
        row_data_index = row_index + 2  # start at first date

        while row_data_index < len(sheet):
            datadate = sheet.iloc[row_data_index, col_index]  # date
            e_score = sheet.iloc[row_data_index, col_index + 1]  # E-Score (column C)

            if pd.notna(datadate) and pd.notna(e_score) and "-N/A" not in [datadate, e_score]:
                try:
                    datadate = pd.to_datetime(datadate, origin='1899-12-30', unit='D')
                    formatted_date = datadate.strftime("%m/%Y")
                except Exception as e:
                    formatted_date = "Invalid Date"
                    print(f"Error converting date at row {row_data_index}: {e}")

                data.append({
                    "isin": isin,
                    "conm": conm,
                    "datadate": formatted_date,  # formatted as MM/YYYY
                    "e_score": e_score
                })

                data_points_count += 1
                if max_data_points is not None and data_points_count >= max_data_points:
                    break

            # next row for same ISIN
            row_data_index += 1

        current_company_count += 1
        # move to the next ISIN column
        col_index += 2

        # create data frame from list
    df = pd.DataFrame(data)

    # Debugging: Ausgabe der ersten paar Zeilen des extrahierten DataFrames
    print("Erste 10 Zeilen des extrahierten ESG DataFrames:")
    print(df.head(10))

    return df


def add_esg_scores(df_local, esg_file_path):
    df_esg = extract_esg_data(esg_file_path)

    # Ensure both DataFrames have 'isin' and 'datadate' as string type
    df_local['isin'] = df_local['isin'].astype(str)
    df_esg['isin'] = df_esg['isin'].astype(str)

    df_local['datadate'] = df_local['datadate'].astype(str)
    df_esg['datadate'] = df_esg['datadate'].astype(str)

    # Debugging: Ausgabe der ersten paar Zeilen des df_local und df_esg DataFrames
    print("Erste 5 Zeilen von df_local:")
    print(df_local.head(5))

    # Firmen ohne ISIN-Übereinstimmung herausfiltern
    df_local_filtered = df_local[df_local['isin'].isin(df_esg['isin'])]

    # Merge ESG-Daten in den Haupt-DataFrame auf Basis von ISIN und datadate
    df_merged = df_local_filtered.merge(
        df_esg[['isin', 'datadate', 'e_score']],
        on=['isin', 'datadate'],
        how='left'
    )

    # Überprüfen, ob der Merge korrekt funktioniert hat
    print("Spalten nach dem Merge:", df_merged.columns.tolist())
    print("Erste 5 Zeilen des zusammengeführten DataFrames:")
    print(df_merged.head(5))

    return df_merged
