import csv
from dimagi.utils.chunked import chunked
from corehq.util.log import with_progress_bar
from corehq.apps.es.users import UserES
from corehq.apps.users.dbaccessors.all_commcare_users import get_all_user_rows
from corehq.apps.users.models import CommCareUser
from corehq.apps.locations.models import SQLLocation
from corehq.apps.users.util import user_location_data


# PART 1 : Run this to gather all the affected users into a csv file
headers = [
    "_id",
    "username",
    "domain",
    "location_id",
    "commcare_primary_case_sharing_id",
    "user_data_location_id",
]

to_update = []
for es_user in UserES().scroll():
    user_location_id = es_user.get("location_id")
    assigned_locations = es_user.get("assigned_locations")
    sharing_id = es_user.get("user_data", {}).get("commcare_primary_case_sharing_id")
    user_data_location_id = es_user.get("user_data", {}).get("commcare_location_id")
    user_data_location_ids = es_user.get("user_data", {}).get("commcare_location_ids")

    if (
        (user_location_id and not sharing_id)
        or (user_location_id and not user_data_location_id)
        or (assigned_locations and not user_data_location_ids)
    ):
        to_update.append(es_user)


with open("no_primary_case_sharing_id.csv", "w") as f:
    writer = csv.DictWriter(f, headers)
    writer.writeheader()
    for row in to_update:
        writer.writerow(
            {
                "_id": row["_id"],
                "username": row.get("username"),
                "domain": row.get("domain"),
                "location_id": row.get("location_id"),
                "commcare_primary_case_sharing_id": sharing_id,
                "user_data_location_id": row.get("user_data", {}).get("commcare_location_id"),
                "user_data_location_ids": row.get("user_data", {}).get("commcare_location_ids"),
            }
        )


# PART 2: Run from here to update the users with the proper ids
with open("no_primary_case_sharing_id.csv", "r") as f:
    reader = csv.DictReader(f)
    to_save = []
    for row in with_progress_bar(reader, len(to_update)):
        save_it = False
        try:
            user = CommCareUser.get(row["_id"])
        except KeyError:
            print(row["_id"])
            continue

        if not user.user_data.get("commcare_primary_case_sharing_id"):
            user.user_data.update({"commcare_primary_case_sharing_id": user.location_id})
            save_it = True
        if not user.user_data.get("commcare_location_id"):
            user.user_data.update({"commcare_location_id": user.location_id})
            save_it = True
        if not user.user_data.get("commcare_location_ids"):
            user.user_data.update({"commcare_location_ids": user_location_data(user.assigned_location_ids)})
            save_it = True

        if save_it:
            to_save.append(user)

print(len(to_save), " docs to save")
saved = 0
for docs_to_save in chunked(to_save, 100):
    CommCareUser.get_db().bulk_save(docs_to_save)
    saved += len(docs_to_save)
    print("saved: ", saved, "of: ", len(to_save))
print("done")
