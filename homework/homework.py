"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """

    import glob
    import os
    import pandas as pd

    def load_input(input_directory):
        files = glob.glob(f"{input_directory}/*")
        dataframes = []
    
        for file in files:
            
            df_temp = pd.read_csv(file)
                    
            dataframes.append(df_temp)

        dataframe = pd.concat(dataframes, ignore_index=True)

        return dataframe
    
    def save_output(dataframe, output_directory, nombre):
        os.makedirs(output_directory, exist_ok=True)

        target_file = os.path.join(output_directory, nombre)

        if os.path.exists(target_file):
            os.remove(target_file)

        dataframe.to_csv(
            target_file,
            sep=",",
            index=False,
        )

    df = load_input("files/input")

    # Dataframe para client
    df_client = df[["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"]].copy()
    df_client["job"] = df_client["job"].str.replace({".": "", "-": "_"})
    df_client["education"] = df_client["education"].str.replace(".", "_")
    df_client["education"] = df_client["education"].replace("unknown", pd.NA)
    df_client["credit_default"] = (df_client["credit_default"] == "yes").astype(int)
    df_client["mortgage"] = (df_client["mortgage"] == "yes").astype(int)

    #Dataframe para campaign
    df_campaign = df[["client_id", "number_contacts", "contact_duration", "previous_campaign_contacts", "previous_outcome", "campaign_outcome"]].copy()
    df_campaign["last_contact_date"] = "2022-" + df["month"].astype(str) + "-" + df["day"].astype(str)
    df_campaign["last_contact_date"] = pd.to_datetime(df_campaign["last_contact_date"], format="%Y-%b-%d")
    df_campaign["previous_outcome"] = (df_campaign["previous_outcome"] == "success").astype(int)
    df_campaign["campaign_outcome"] = (df_campaign["campaign_outcome"] == "yes").astype(int)

    # Dataframe para economics
    df_economics = df[["client_id", "cons_price_idx", "euribor_three_months"]].copy()
    
    save_output(df_client, "files/output", "client.csv")
    save_output(df_campaign, "files/output", "campaign.csv")
    save_output(df_economics, "files/output", "economics.csv")

    return


if __name__ == "__main__":
    clean_campaign_data()
