import csv
from rtree import index

CSV_PATH = './data/raw/ej_organizations.csv'

class CommunityDatabase():
    def __init__(self, csv_path=CSV_PATH):
        raw_entries = []
        with open(csv_path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row["Name"] = row["\ufeffOrganization"]
                raw_entries.append(row)

        self.id_map = {i : e for i, e in enumerate(raw_entries)}
        self.idx = index.Index()
        for i in self.id_map:
            lat = float(self.id_map[i]["Latitude"])
            long = float(self.id_map[i]["Longitude"])
            coords = (lat, long, lat, long)
            self.idx.insert(i, coords)

    def get_organizations(self, bbox):
        ids = self.idx.intersection(bbox)
        objs = [self.id_map[fid] for fid in ids]

        # Dedupe organizations by their name
        to_ret = []
        for obj in objs:
            if not obj["Name"] in [o["Name"] for o in to_ret]:
                to_ret.append(obj)

        return to_ret
