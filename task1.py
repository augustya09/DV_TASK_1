import csv
from collections import deque

stations_csv = "/content/sample_data/metro_stations_multiline.csv"

class Station:
    # Reading the CSV file & storing network connections
    def __init__(self):
        self.connections = {}  # {station: [('n1', 'l1'), (n2, 'l2'), ...]}

    def csvreader(self):
        # Fills self.connections dictionary
        with open(stations_csv, "r") as file:
            reader = csv.DictReader(file)
            for i in reader:
                station = i["STATION"]
                line = i["LINE"]
                next_station = i["NEXT_STATION"]

                # Bidirectional connections
                if station not in self.connections:
                    self.connections[station] = []
                if next_station not in self.connections:
                    self.connections[next_station] = []

                self.connections[station].append((next_station, line))
                self.connections[next_station].append((station, line))

    def show_stations(self):
        print("The stations are:")
        for i in self.connections:
            print(i)

class Metro:
    def __init__(self, connections):
        self.metro = connections  # Stores the metro map

    def shortest_path(self, start, end):
        if start not in self.metro or end not in self.metro:
            print("Invalid entry")
            return

        queue = deque([[start]])
        visited = set()

        while queue:
            path = queue.popleft()
            current = path[-1]
            if current == end:
                return path
            if current not in visited:
                for neighbor, _ in self.metro[current]:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
                visited.add(current)
        return None

    def get_line(self, station1, station2):
        for neighbor, line in self.metro[station1]:
            if neighbor == station2:
                return line
        return None

    def transfer_instructions(self, path):
        if not path:
            print("No path found")
            return

        print("STATIONS IN THE WAY:")
        print(" _ ".join(path))
        total_stations = len(path) - 1
        fare = total_stations * 100
        print("The total number of stations:", total_stations)
        print("The fare is:", fare, "rupees")
        print('DETAILED INSTRUCTIONS:')

        current_line = self.get_line(path[0], path[1])
        print("Start at", path[0], "on the", current_line, "line")

        for i in range(1, len(path) - 1):
            next_line = self.get_line(path[i], path[i + 1])
            if next_line != current_line:
                print('Change from', current_line, 'to', next_line, 'line at', path[i])
                current_line = next_line

        print("Arrive at", path[-1], "on the", current_line, "line")

class Ticket:
    def __init__(self, station_data):
        self.stations = list(station_data.keys())
        self.metro = Metro(station_data)

    def book_ticket(self):
        start = input("Enter the starting station: ")
        end = input("Enter the end station: ")

        if start not in self.stations or end not in self.stations:
            print("Invalid entry")
            return

        path = self.metro.shortest_path(start, end)
        self.metro.transfer_instructions(path)

# Main driver code
s = Station()
s.csvreader()
s.show_stations()

t = Ticket(s.connections)
t.book_ticket()
