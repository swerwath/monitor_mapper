import csv
from rtree import index
import re

csv_to_obj_fields = {
                     "FACILITY_NAME" : "name",
                     "TRI_FACILITY_ID" : "id",
                     "STREET_ADDRESS" : "address",
                     "LATITUDE" : "latitude",
                     "LONGITUDE" : "longitude",
                     "PARENT_COMPANY_NAME" : "company",
                    }

class ChemicalData():
    def __init__(self, name, quantity, unit):
        self.name = re.sub(r'\(.*\)', '', name).replace('"', '').split(" AND")[0]
        self.quantity = float(quantity)
        self.unit = unit

    def to_json_dict(self):
        return {'name' : self.name, 'quantity' : self.quantity, 'unit' : self.unit}

    def __repr__(self):
        return "(" + self.name + " " + str(self.quantity) + " " + self.unit + ")"

class TRIEntry():
    def __init__(self, csv_dict):
        self.data = {}
        for field in csv_to_obj_fields:
            self.data[csv_to_obj_fields[field]] = csv_dict[field]
        self.data["latitude"] = float(self.data["latitude"])
        self.data["longitude"] = float(self.data["longitude"])
        unit = csv_dict["UNIT_OF_MEASURE"].replace("Pounds", "lbs").replace("Grams", "g")
        self.chemicals = [ChemicalData(csv_dict["CHEMICAL"], csv_dict["TOTAL_RELEASES"], unit)]

    def to_json_dict(self):
        to_ret = self.data
        to_ret["chemicals"] = [c.to_json_dict() for c in self.chemicals]
        return to_ret

class TRIDatabase():
    def __init__(self, csv_path="./data/raw/TRI.csv"):
        raw_entries = []
        with open(csv_path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if float(row["TOTAL_RELEASES"]) > 0 and row["CLEAR_AIR_ACT_CHEMICAL"] == "YES":
                    raw_entries.append(TRIEntry(row))

        merged_entries = {}
        for entry in raw_entries:
            id = entry.data["id"]
            if id in merged_entries.keys():
                merged_entries[id].chemicals.append(entry.chemicals[0])
            else:
                merged_entries[id] = entry

        self.id_map = {i : e for i, e in enumerate(merged_entries.values())}
        self.idx = index.Index()
        for i in self.id_map:
            lat = self.id_map[i].data["latitude"]
            long = self.id_map[i].data["longitude"]
            coords = (lat, long, lat, long)
            self.idx.insert(i, coords)

    def get_facilities(self, bbox):
        facility_ids = self.idx.intersection(bbox)
        facility_objs = [self.id_map[fid] for fid in facility_ids]

        return facility_objs
