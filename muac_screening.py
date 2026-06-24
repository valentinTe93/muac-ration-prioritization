# --- Raw screening data ---
# Each record: [village_name, child_id, muac_mm, age_months]
screenings = [
    ["Bouake", "C001", 135, 18],
    ["Bouake", "C002", 118, 24],
    ["Korhogo", "C003", 110, 14],
    ["Korhogo", "C004", 142, 36],
    ["Daloa", "C005", 124, 20],
    ["Bouake", "C006", 109, 16],
    ["Korhogo", "C007", 130, 28],
    ["Daloa", "C008", 113, 22],
    ["Daloa", "C009", 145, 40],
    ["Bouake", "C010", 121, 19],
]

# --- Containers built up as we process the data ---
ranking = []                 # will hold [village_name, need_count] pairs
sam_cases = []                # full records classified as SAM
mam_cases = []                # full records classified as MAM
normal_cases = []             # full records classified as Normal
not_unique_village_names = [] # village name collected once per record (will contain duplicates)


# Classifies a single MUAC measurement into SAM / MAM / Normal
# based on the standard mm thresholds.
def classify_muac(muac_mm):
    if muac_mm >= 125:
        muac_class = 'Normal'
    elif muac_mm >= 115:
        muac_class = 'MAM'
    else:
        muac_class = 'SAM'
    return muac_class


# Unpacks a single record into its four fields so the rest
# of the code doesn't have to index into the list directly.
def screening_infos(record):
    village = record[0]
    child_id = record[1]
    muac_mm = record[2]
    age_months = record[3]
    return village, child_id, muac_mm, age_months


# Classifies one record and appends the FULL record (not just
# the MUAC value) into the matching list: sam_cases, mam_cases,
# or normal_cases. This is what lets us reuse these lists later
# instead of re-scanning all of screenings.
def class_list_builder(record):
    _, _, muac_mm, _ = screening_infos(record)
    class_type = classify_muac(muac_mm)
    if class_type == 'SAM':
        sam_cases.append(record)
    elif class_type == 'MAM':
        mam_cases.append(record)
    else:
        normal_cases.append(record)


# Counts how many SAM + MAM cases belong to one village.
# Reuses the sam_cases/mam_cases lists already built by
# class_list_builder, instead of re-looping through all of
# screenings and reclassifying every child again.
def village_ration_need(village_name):
    sam_count = 0
    mam_count = 0
    for record in sam_cases:
        village, _, _, _ = screening_infos(record)
        if village == village_name:
            sam_count += 1
    for record in mam_cases:
        village, _, _, _ = screening_infos(record)
        if village == village_name:
            mam_count += 1
    return sam_count + mam_count


# Single pass over screenings:
# - prints each child's classification line
# - prints an extra urgent-referral line for SAM cases
# - sorts the record into sam_cases / mam_cases / normal_cases
# - records the village name (with duplicates) for later dedup
for record in screenings:
    village, child_id, muac_mm, age_months = screening_infos(record)
    classification = classify_muac(muac_mm)
    base_printable = village + ' - ' + child_id + ': ' + classification + ' (MUAC: ' + str(muac_mm) + 'mm, age: ' + str(age_months) + 'mo)'
    if classification == 'SAM':
        print(base_printable + '\nURGENT REFERRAL NEEDED for ' + child_id)
    else:
        print(base_printable)
    class_list_builder(record)
    not_unique_village_names.append(village)

# Removes duplicates from the village name list using set(),
# then converts back to a list since set() has no guaranteed order.
village_names = list(set(not_unique_village_names))

# For each unique village, get its ration need count and store
# it alongside the village name as a [name, count] pair.
for village in village_names:
    need_count = village_ration_need(village)
    ranking.append([village, need_count])

# Sorts the [name, count] pairs by count (index 1), highest need
# first, without mutating village_names or screenings.
village_ranking_sorted = sorted(ranking, key=lambda x: x[1], reverse=True)

# Final delivery-priority report: one line per village, highest
# need first, followed by the total SAM count across all villages.
for village in village_ranking_sorted:
    print('Village_name : ' + village[0] + ' -- ' + 'need_count : ' + str(village[1]))
print('Total number of SAM cases is : ' + str(len(sam_cases)))


# Bonus: computes the average MUAC value across a given list
# of records (e.g. sam_cases or normal_cases), to compare how
# far apart the two groups sit on average.
def average_muac(records):
    total = 0
    for record in records:
        _, _, muac_mm, _ = screening_infos(record)
        total += muac_mm
    return total / len(records)

print('Average MUAC - SAM group : ' + str(average_muac(sam_cases)))
print('Average MUAC - Normal group : ' + str(average_muac(normal_cases)))
