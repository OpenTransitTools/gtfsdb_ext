import re
import csv
import sys
import requests
from . import utils


def to_csv(json, output, pr_string="Park & Ride"):
    writer = None
    sorted_json = sorted(json, key=lambda x: x.get('name'))
    for i, r in enumerate(sorted_json):
        name = r.get('name')
        if name:
            alias = ""

            # if the name lacks any "PR", "Park and Ride", etc... indication, append "Park & Ride" to it
            #abbrev_regex = ["\\sPR(\\s|$)", "\\sP\\+R(\\s|$)", "\\sP\\&R(\\s|$)"]
            abbrev_regex = ["\\sPR(\\s|$)", "\\sP+R(\\s|$)", "\\sP&R(\\s|$)"]
            pr_regex = abbrev_regex + ["park and", "park &", "parking"]
            if all(not re.search(x, name, flags=re.IGNORECASE) for x in pr_regex):
                alias = utils.to_alias_json(name, name + " PR")
                name = f"{name} {pr_string}"
            else:
                # rename abbreviated "PR","P&R", "P+R" etc... to "Park & Ride"
                if any(re.search(x, name, flags=re.IGNORECASE) for x in abbrev_regex):
                    alias = utils.to_alias_json(name, name + " PR")
                    if "PR" in name.upper():
                        name = re.sub("\\sPR(\\s|$)", " " + pr_string + " ", name, flags=re.IGNORECASE).strip()
                    for pr in ["P+R", "P&R"]:
                        if pr in name.upper():
                            name = name.replace(pr, pr_string)
                            break
                else:
                    # name didn't have a "PR" shorthand above, so add PR as an alias to help find using shorthand
                    alias = utils.to_alias_json(name, name + " PR")

                    # note: rename Park and Ride names from OSM to Park & Ride
                    if "Park and Ride" in name:
                        name = re.sub("Park and Ride", pr_string, name, flags=re.IGNORECASE).strip()

            rec = utils.make_pelias_csv_record(
                id=f"pr-{i+1}",
                name=name,
                lat=r.get('y'), lon=r.get('x'),
                layer="pr", source="transit",
                aliases=alias
            )

            if writer is None:
                writer = csv.DictWriter(output, fieldnames=rec.keys())
                writer.writeheader()

            writer.writerow(rec)



#def query(url="https://maps.trimet.org/rtp/routers/default/park_and_ride"):
def query(url="https://ws.trimet.org/rtp/routers/default/park_and_ride"):
    ret_val = None
    response = requests.get(url)
    ret_val = response.json()
    return ret_val


def main():
    #import pdb; pdb.set_trace()
    json = query()
    file = sys.argv[1] if len(sys.argv) > 1 else "print"
    if file.lower() in ("p", "print"):
        import io
        output = io.StringIO()
        to_csv(json, output)
        print(output.getvalue())
    else:
        with open(file, 'w') as output:
            to_csv(json, output)

