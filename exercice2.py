import pandas as pd
from datetime import datetime
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Application de transport public.')
    parser.add_argument('stop_id', type=int, help='Numéro de l\'arrêt')
    parser.add_argument('-d', '--datetime', type=str, help='Date et heure au format YYYY-MM-DD HH:MM:SS')
    return parser.parse_args()

args = parse_args()
stop_id = args.stop_id
input_datetime = args.datetime

if input_datetime:
    date_time_courant = datetime.strptime(input_datetime, '%Y-%m-%d %H:%M:%S')
else:
    date_time_courant = datetime.now()

# Charger les données
stops = pd.read_excel('./data/stops.xlsx')
stop_times = pd.read_excel('./data/stop_times.xlsx')
trips = pd.read_excel('./data/trips.xlsx')
routes = pd.read_excel('./data/routes.xlsx')

# Filtrer les passages pour l'arrêt spécifié
stop_times_stop_id = stop_times[stop_times['stop_id'] == stop_id]

# Ajouter une colonne datetime aux heures de passage
stop_times_stop_id['arrival_time'] = pd.to_datetime(stop_times_stop_id['arrival_time'], format='%H:%M:%S')

# Filtrer les passages futurs
stop_times_future = stop_times_stop_id[stop_times_stop_id['arrival_time'].dt.time >= date_time_courant.time()]

# Joindre les données pour obtenir les lignes et routes correspondantes
result = stop_times_future.merge(trips, on='trip_id').merge(routes, on='route_id')
result = result.sort_values('arrival_time')

# result.to_excel("cool.xlsx")

# Afficher les résultats
if result.empty:
    print("Aucun passage prévu pour cet arrêt après l'heure spécifiée.")
else:
    print(f"Prochains passages à l'arrêt {stop_id} après {date_time_courant}:")
    for _, row in result.iterrows():
        print(f"Ligne {row['route_id']} ({row['route_long_name']}- {row['trip_id']}), Passage à {row['arrival_time'].strftime('%H:%M:%S')}")

# python exercice2.py stop_id -d date_time
# python exercice2.py 10034 -d "2024-07-30 14:30:00"
