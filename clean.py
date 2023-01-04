import csv
import json

d = {}


def hello(stringToInt):
    try:
        return int(stringToInt)
    except ValueError:
        return None


with open("stats.csv") as csvfile:
    reader = csv.reader(csvfile)
    rows = []
    for row in reader:
        rows.append(row)

    for j in range(2, len(rows)):
        row = rows[j]
        item = row[1]
        for i in range(2, len(row), 3):
            district = rows[0][i].lower()

            area = hello(row[i].replace(",", "").strip())
            production = hello(row[i+1].replace(",", "").strip())
            yield_ = hello(row[i+2].replace(",", "").strip())

            d.setdefault(district, {})
            d[district].setdefault(item, {})
            d[district][item]["production"] = production
            d[district][item]["area"] = area
            d[district][item]["yield"] = yield_

    # combine nawalpur and parasi
    d.setdefault("nawalparasi", {})
    d["nawalparasi"].setdefault(item, {})
    for key, item in d["nawalpur"].items():
        d["nawalparasi"][key] = item
    for key, item in d["parasi"].items():
        for k2, i2 in item.items():
            d["nawalparasi"][key][k2] = d["nawalparasi"][key][k2] + \
                i2 if d["nawalparasi"][key][k2] else None
    d.pop("nawalpur")
    d.pop("parasi")

    # remove province/country info
    to_remove = [key for key in d.keys() if "province" in key or "nepal" in key]
    for key in to_remove:
        d.pop(key)

    with open("out.json", "w") as output_file:
        json.dump(d, output_file)
