# nicht vergessen bei Anaconda prompt: conda activate Masterthesis
import os
import pandas as pd
# from data_processing_CSV import create_dataframe_from_csv
from data_processing_CSV import add_employee_data
from data_processing_CSV import expand_quarterly_to_monthly
# from data_processing_CSV import add_esg_scores
from data_processing_CSV import extract_esg_data
from data_processing_CSV import update_e_score
from data_processing_CSV import manual_check
from merge_data import parse_esg_data
from data_processing_from_merged_data import create_dataframe_from_csv
from data_processing_from_merged_data import simpledf


def main():
    ########## CREATE OUTPUT DIRECTORY AND MERGE EXCEL AND CSV ##########
    # only use once
    # Define the path to the data files
    a=0
    """esg_score_file = os.path.join('data', 'esg_env_risk_score_ms.xlsx')
    stoxx_quarterly_file = os.path.join('data', 'stoxx_quarterly_fundamentals.csv')
    stoxx_employees_file = os.path.join('data', 'stoxx_employees.csv')

    # Read the stoxx quarterly data
    stoxx_quarterly = pd.read_csv(stoxx_quarterly_file)

    # Rename 'datadate' to 'date'
    stoxx_quarterly.rename(columns={'datadate': 'date'}, inplace=True)

    # Parse 'date' as datetime
    stoxx_quarterly['date'] = pd.to_datetime(stoxx_quarterly['date'], format='%d/%m/%Y')

    # Move the 'isin' and 'conm' columns to the front
    cols = list(stoxx_quarterly.columns.values)
    cols.pop(cols.index('isin'))
    cols.pop(cols.index('conm'))
    stoxx_quarterly = stoxx_quarterly[['isin', 'conm'] + cols]

    # Read the stoxx employees data
    stoxx_employees = pd.read_csv(stoxx_employees_file)

    # Rename 'datadate' to 'date'
    stoxx_employees.rename(columns={'datadate': 'date'}, inplace=True)

    # Parse 'date' as datetime
    stoxx_employees['date'] = pd.to_datetime(stoxx_employees['date'], format='%d/%m/%Y')

    # Move the 'isin' and 'conm' columns to the front
    cols = list(stoxx_employees.columns.values)
    cols.pop(cols.index('isin'))
    cols.pop(cols.index('conm'))
    stoxx_employees = stoxx_employees[['isin', 'conm'] + cols]

    # Extract ESG data from the excel file
    esg_risk = pd.DataFrame(parse_esg_data(esg_score_file))

    # Merge stoxx quarterly data with ESG risk data
    data = pd.merge(stoxx_quarterly, esg_risk, on=['date', 'isin'], how='outer')

    # Merge the result with the stoxx employees data
    data = pd.merge(data, stoxx_employees, on=['date', 'isin'], how='outer')

    # Sort columns alphabetically
    data = data.reindex(sorted(data.columns), axis=1)

    # Print or save the merged data
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'merged_data.csv')
    data.to_csv(output_file, index=False)

    print("Merged data saved to:", output_file)"""

    ########## DATA PROCESSING FROM MERGED CSV FILE ##########

    file_path = 'C:\\Users\\Sophie\\Masterthesis\\output\\merged_data.csv'
    #df = create_dataframe_from_csv(file_path)
    #print(df)
    data=pd.read_csv(file_path)

    data = data.dropna(subset=['e_score'])
    print(data)





""""# Define paths to each file used
    file_path = 'C:\\Users\\Sophie\\Masterthesis\\stoxx_quarterly_fundamentals.csv'
    emp_file_path = 'C:\\Users\\Sophie\\Masterthesis\\stoxx_employees.csv'
    esg_MS_file_path = 'C:\\Users\\Sophie\\Masterthesis\\esg_env_risk_score_ms.xlsx'

    # Create dataframes from quarterly fundamentals
    df_fundamentals = create_dataframe_from_csv(file_path)

    # Expand these to monthly data
    df_fundamentals_monthly = expand_quarterly_to_monthly(df_fundamentals)

    # Add employee data to dataframe
    df_emp = add_employee_data(df_fundamentals_monthly, emp_file_path)

    # Extract ESG data from excel and add ESG data to existing dataframe
    df_esg = extract_esg_data(esg_MS_file_path)

    # Den resultierenden DataFrame anzeigen
    print(df_emp)
    print(df_esg)

    # Kopf der Tabelle anzeigen
    print("Spalten im DataFrame:", df_emp.columns.tolist())

    # Eine spezifische Zeile anzeigen (z.B. die erste Zeile)
    print("\nErste Zeile im DataFrame:")
    print(df_emp.iloc[15])

    # Update df_emp by overwriting e_score from df_esg
    df_merged = update_e_score(df_emp, df_esg)
    print(df_merged)

    # check if data transfer was successful
    df_check = manual_check(df_emp, df_esg, 'NL0000334118', '09/2011')
    print(df_check)
"""

if __name__ == "__main__":
    main()
