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
