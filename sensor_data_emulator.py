
# Importation des modules nécessaires
import threading
import random
import time
from blessed import Terminal  # Librairie pour gérer l'affichage dans le terminal

# Initialisation du terminal pour l'affichage
term = Terminal()

class SensorData:
    """
    Classe qui simule les données des capteurs (profondeur, température, pression).
    Elle utilise un verrouillage pour assurer des mises à jour thread-safe.
    """
    def __init__(self):
        self.lock = threading.Lock()  # Verrou pour la gestion des données dans des threads différents
        self.depth = 50.0  # Valeur initiale de la profondeur
        self.temperature = 20.0  # Valeur initiale de la température
        self.pressure = 1.0  # Valeur initiale de la pression

    def update(self):
        """
        Met à jour les valeurs des capteurs avec des variations réalistes.
        La profondeur, la température et la pression sont ajustées de manière aléatoire
        pour simuler un environnement dynamique.
        """
        with self.lock:  # Assurer qu'un seul thread accède aux données à la fois
            self.depth += random.uniform(-0.5, 0.5)  # Variations aléatoires de la profondeur
            self.depth = max(0, min(100, self.depth))  # Limite la profondeur entre 0 et 100
            # Température influencée par la profondeur, avec du bruit aléatoire
            self.temperature = 25 - (self.depth * 0.1) + random.uniform(-0.2, 0.2)
            # Pression influencée par la profondeur, avec du bruit aléatoire
            self.pressure = 1.0 + (self.depth / 10.0) + random.uniform(-0.1, 0.1)

    def get_data(self):
        """
        Récupère les valeurs des capteurs de manière sécurisée.
        """
        with self.lock:  # Assurer qu'un seul thread accède aux données à la fois
            return self.depth, self.temperature, self.pressure

def update_sensor_data(sensor_data, interval):
    """
    Fonction qui met à jour les données des capteurs de manière périodique.
    Utilise un timer pour effectuer l'update toutes les X secondes.
    """
    sensor_data.update()
    timer = threading.Timer(interval, update_sensor_data, args=(sensor_data, interval))
    timer.daemon = True  # Le thread sera tué quand le programme principal se termine
    timer.start()

def main():
    """
    Fonction principale qui initialise le tableau de bord du terminal et met à jour les
    données des capteurs à intervalle régulier.
    """
    sensor_data = SensorData()  # Initialisation de la classe SensorData
    update_interval = 0.5  # Intervalle de mise à jour des données (en secondes)
    update_sensor_data(sensor_data, update_interval)  # Lancer les mises à jour périodiques

    # Démarre l'interface utilisateur dans le terminal (en mode plein écran et sans curseur)
    with term.fullscreen(), term.hidden_cursor():
        while True:
            # Récupère les dernières valeurs des capteurs
            depth, temp, press = sensor_data.get_data()

            # Effacer l'écran à chaque itération pour rafraîchir l'affichage
            print(term.clear)

            # Affichage du tableau de bord
            print(term.bold_blue(term.center("🔵 Tableau de bord des capteurs 🔵\n")))
            print(term.green(term.center(f"🌡 Température : {temp:.2f} °C")))
            print(term.cyan(term.center(f"🌊 Profondeur : {depth:.2f} m")))
            print(term.magenta(term.center(f"⚙️  Pression : {press:.2f} bar")))

            # Affichage des instructions à l'utilisateur
            print(term.yellow(term.center("\n(Appuyez sur 'q' pour quitter)")))

            # Attente de l'entrée de l'utilisateur avec une lecture non-bloquante
            with term.cbreak():
                inp = term.inkey(timeout=0.5)  # Lecture non-bloquante
                if inp.lower() == 'q':  # Quitter le programme si l'utilisateur appuie sur 'q'
                    break

if __name__ == "__main__":
    try:
        main()  # Lancer l'application principale
    except KeyboardInterrupt:
        print("\nSortie du programme.")  # Gérer l'interruption du programme
