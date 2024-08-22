# nicht vergessen bei Anaconda prompt: conda activate Masterthesis
import os
from data_processing_CSV import create_dataframe_from_csv
from data_processing_CSV import add_employee_data


def main():
    # Pfad zur Excel-Datei angeben

    # print("Aktuelles Arbeitsverzeichnis:", os.getcwd())

    file_path = 'C:\\Users\\Sophie\\Masterthesis\\stoxx_quarterly_fundamentals.csv'
    emp_file_path = 'C:\\Users\\Sophie\\Masterthesis\\stoxx_employees.csv'


    # ESG-Daten extrahieren
    df_fundamentals = create_dataframe_from_csv(file_path)
    df_emp = add_employee_data(df_fundamentals, emp_file_path)


    # Den resultierenden DataFrame anzeigen
    print(df_emp)

    # Kopf der Tabelle anzeigen
    print("Spalten im DataFrame:", df_emp.columns.tolist())

    # Eine spezifische Zeile anzeigen (z.B. die erste Zeile)
    print("\nErste Zeile im DataFrame:")
    print(df_emp.iloc[15])


if __name__ == "__main__":
    main()