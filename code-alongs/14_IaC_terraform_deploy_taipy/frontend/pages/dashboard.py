import taipy.gui.builder as tgb
from backend.update import filter_data
from backend.data_processing import df, filter_df_municipality
from frontend.charts import create_municipality_bar


df_municipality = filter_df_municipality(df)
number_municipalities = 5
municipality_title = number_municipalities

selected_educational_area = "DATA/IT"
educational_area_title = selected_educational_area
municipality_chart = create_municipality_bar(
    df_municipality.head(5), ylabel="Kummun", xlabel="# ANSÖKTA UTBILDNINGAR"
)


with tgb.Page() as dashboard_page:
    with tgb.part(class_name="container stack-large card"):
        tgb.navbar()
        with tgb.part(class_name="card"):
            tgb.text("# MYH dashboard 2024", mode="md")
            tgb.text(
                "En dashboard för att visa statistik och information om ansökningar 2024",
                mode="md",
            )

        with tgb.layout(columns="2 1"):
            with tgb.part(class_name="card") as column_chart:
                tgb.text(
                    "## Antal ansökningar YH utbildningar per kommun (topp {municipality_title}) för {educational_area_title}",
                    mode="md", class_name= "title-chart"
                )

                tgb.chart(figure="{municipality_chart}")

            with tgb.part(class_name="card") as column_filter:
                tgb.text("## Filter data", mode="md")
                tgb.text("Filter antal kommuner", mode="md")

                tgb.slider(
                    value="{number_municipalities}",
                    min=5,
                    max=len(df_municipality),
                    continuous=False,
                )

                tgb.text("Välj utbildningsområde", mode="md")
                tgb.selector(
                    value="{selected_educational_area}",
                    lov=df["Utbildningsområde"].unique(),
                    dropdown=True,
                )

                tgb.button("Filter data", on_action=filter_data)
                
        