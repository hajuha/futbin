import time
import requests
from bs4 import BeautifulSoup
import pickle
import threading
from decouple import config

class SoccerGuru():
    def __init__(self):
        self.URL_BASE = "https://www.futwiz.com/en/fifa22/players?page="

        # {overall_stats: [[name, rating]]}
        self.allplayers = {}
        self.lock1 = threading.Lock()
        self.lock2 = threading.Lock()
        self.player_count = 0

    def create_pickle(self):
        player_dict = self.allplayers
        self._begin_thread()
        self._pickle_object(player_dict)

    def unload_pickle(self):
        player_dict = self._unpickle_object()
        return player_dict

    def filter(self, player_dict, rating_cap=100, league="", country="", position=""):
        new_player_dict = dict()
        for key, value in player_dict.items():
            for i in value:
                if int(i[1]) <= rating_cap and (league == i[2] or league == "") and (country == i[3] or country == "") and (position == i[4] or position == ""):
                    if key in new_player_dict:
                        new_player_dict[key].append(i)
                    else:
                        new_player_dict[key] = [i]

        return new_player_dict

    def filter_exact_rating(self, player_dict, rating_cap=100, league="", country=""):
        new_player_dict = dict()
        for key, value in player_dict.items():
            for i in value:
                if int(i[1]) == rating_cap and (league == i[2] or league == "") and (str(country) == str(i[3]) or country == ""):
                    if key in new_player_dict:
                        new_player_dict[key].append(i)
                    else:
                        new_player_dict[key] = [i]

        return new_player_dict

    def _get_player_dict(self):
        return self.allplayers

    def _get_players(self, start, end):
        for i in range(start, end):
            # print("Currently getting page: " + str(i))
            URL = self.URL_BASE + str(i)
            page = requests.get(URL)

            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find(class_="playersearchresults")
            players = results.find_all("tr", class_="table-row")

            for player_row in players:
                self.lock2.acquire()
                self.player_count += 1
                self.lock2.release()
                league = player_row.find(
                    "p", class_="team").find_all("a")[1].text
                league = league.replace(" ", "")
                position = list(player_row.children)[7].text.strip()
                country = player_row.find("img", class_="nation").attrs['src'].split(".")[
                    0].split("/")[-1]
                name = player_row.find("b").text
                stats = player_row.find_all(class_="stat")
                rating = player_row.find(class_="otherversion22-txt").text
                overall_stats = 0
                for stat in stats:
                    overall_stats += int(stat.text)

                if overall_stats in self.allplayers:
                    self.lock1.acquire()
                    self.allplayers[overall_stats].append(
                        [name, rating, league, country, position])
                    self.lock1.release()
                else:
                    self.lock1.acquire()
                    self.allplayers[overall_stats] = [
                        [name, rating, league, country, position]]
                    self.lock1.release()

    def _get_players_from_csv(self):

        import csv

        nations = {
            'ENG': "14",
            'FRA': "18",
            "GER": "21",
            "SPA": "45",
            'NED': '34',
            'POR': '38',
            'ITA': '27',
            'ARG': '52',
            'BRA': '54',
            'BEL': '7',
            'DEN': '13',
            'MEX': '83',
            'URU': '60',
            'CRO': '10',
            'RUS': '40',
            'USA': '95',
            'JPN': '163',
            'CHE': '47',
            'AUT': '4',
            'SRB': '51',
            'HRV': '10',
            'NGA': '133',
            'CDI': '108',
            'HUN': '23',
            'BUL': '9',
            'CZE': '12'
        }

        with open('guru.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    self.lock2.acquire()
                    self.player_count += 1
                    self.lock2.release()

                    league = row[1]
                    position = row[5]
                    country = row[2]
                    country = country.upper()
                    nation_code = nations.get(country, None)
                    name = row[0]
                    rating = str(row[3])
                    overall_stats = int(row[4])

                    if overall_stats in self.allplayers:
                        self.lock1.acquire()
                        self.allplayers[overall_stats].append(
                            [name, rating, league, nation_code, position])
                        self.lock1.release()
                    else:
                        self.lock1.acquire()
                        self.allplayers[overall_stats] = [
                            [name, rating, league, nation_code, position]]
                        self.lock1.release()

    def _pickle_object(self, player_dict):
        dbfile = open(config('DRAFT_PICKLE_FILE_NAME'), 'ab')
        pickle.dump(player_dict, dbfile)
        dbfile.close()

    def _unpickle_object(self):
        dbfile = open(config('PICKLE_FILE_NAME'), 'rb')
        player_dict = pickle.load(dbfile)
        dbfile.close()
        return player_dict

    def _begin_thread(self):
        time_1 = time.time()
        for i in range(0, 10):
            t = threading.Thread(target=self._get_players, args=(81*i, 81*i+81))
            t.start()

        t_1 = threading.Thread(target=self._get_players_from_csv)
        t_1.start()
        for thread in threading.enumerate()[1:]:
            thread.join()
        time_2 = time.time()

        print(time_2-time_1)
        print("Completed")


def print_top(max_rating=100, league="", country="", show_number=10):
    a = SoccerGuru()
    player_dict = a.unload_pickle()
    player_dict = a.filter(player_dict, max_rating, league, country)
    overall_list = list(player_dict.keys())
    overall_list.sort(reverse=True)
    overall_list = reversed(overall_list)

    print("Displayed in form: [name, rating, league, country id, position]")
    for i in range(show_number):
        try:
            overall = next(overall_list)
            print("Overall base stats is " +
                  str(overall) + ": ", player_dict[overall])
        except:
            break


def create():
    a = SoccerGuru()
    a.create_pickle()


# League could be ENG 1, ICO, FRA 1, ESP 1, MEX 1 etc.
# Country is a string number e.g. '45', '52' which maps to a specific country. cbb writing code for that.
# Show_number prints the number of cards with the top overall base stats
# print_top(100, league="", country="", show_number=10)
# create()
