import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

#Vi importer datasetet customer_data med pandas
filename = 'restaurant-and-market-health-inspections.csv'
in_data = pd.read_csv(filename, sep=',', header=0, names=None)

#Vi sjekker hvor mange rader som eksisterer i datasettet, navn og data typer av kolonner med null verdier.
#restaurant-and-market-health-inspections.csv inneholder ikke noen null verdier. Som betyr at vi ikke trenger å benytte data cleaning
in_data.info()

#Vi samler alle verdiene fra pe_description og teller antall risk verdier, disse printer vi til terminalen
show_risk = pd.crosstab(index=in_data['pe_description'], columns='sum').sort_values(by=['sum'],ascending=False)
print(show_risk)

#lag en egen kolonne som ikke inkluderer parantesene denne printer vi på skjermen, skal brukes senere.
in_data['risk_level'] = in_data['pe_description'].apply(lambda x: x.split(")")[1])

#Vi benytter seaborn bibloteket til å tegne en graf utifra pe_description verdiene
sns.set(rc={'figure.figsize':(16,9.5)})
risk_graph = sns.countplot(x="pe_description", data=in_data, order = in_data['pe_description'].value_counts().index, palette="Blues_d")
risk_graph.set_xticklabels(risk_graph.get_xticklabels(),rotation=90)
risk_graph.tick_params(labelsize=10)

#Vi lagrer alle "RESTURANT (0-30) SEATS HIGH RISK" verdiene i en seperat datasett å bruker dette videre
risk_data = in_data.loc[in_data['pe_description'] == "RESTAURANT (0-30) SEATS HIGH RISK"]
risk_data.head()

restaurant_risk = pd.crosstab(index=risk_data['facility_name'], columns='sum').sort_values(by=['sum'],ascending=False).head(20)
total_risk = pd.crosstab(index=in_data['risk_level'], columns='sum').sort_values(by=['sum'],ascending=False)

#Vis total_risk og restaurant_risk verdi om vi vil
#print(restaurant_risk)
#print(total_risk)

#Vi bruker risk_level kolonnen vi lagde tidligere for å vise summen av resultatene.
sum_risk = in_data.groupby(['risk_level']).size().reset_index(name='sum')
sum_risk.head()

#Vi lager en percent kolonne som vi bruker for å regne prosent antall av risks.
sum_risk['percent'] =  sum_risk['sum']/sum_risk['sum'].sum()
sum_risk.head()

#Juster graf størrelse og print dem ut
plot = sum_risk.plot.pie(y='percent')
plt.figure(figsize=(15, 15))
riskbar_plot = sns.barplot(x="percent", y="risk_level", data=sum_risk)
plt.show()