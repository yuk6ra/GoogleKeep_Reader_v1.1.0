import gkeepapi
import re

# find Google Account ID and Password
with open("Secret.txt", "r", encoding="utf-8") as Secret:
    reader = Secret.read().split()
    account_id = reader[0]
    password = reader[1]

keep = gkeepapi.Keep()

# pass login
keep.login(account_id, password)

date_type = re.compile(r"""(
    (^\d{4})        # First 4 digits number
    (\D)            # Something other than numbers
    (\d{1,2})       # 1 or 2 digits number
    (\D)            # Something other than numbers
    (\d{1,2})       # 1 or 2 digits number
    )""",re.VERBOSE)

# find the keyword of query="Test"
g_memo = keep.find(query=date_type,labels=[keep.findLabel('TEST_Label')])
# indicate the found memos


dict = {}

for memo_data in g_memo:
    title = memo_data.title
    text = memo_data.text
    d = {title : text}
    dict.update(d)

for date,content in dict.items():

    # Hit data to "hit_date"
    hit_date = date_type.search(date)
    bool_value = bool(hit_date)
    if bool_value is True:
        split = hit_date.groups()
        # Tuple unpacking
        year, month, day = int(split[1]),int(split[3]),int(split[5])

        if year > 3000 or month <= 12 or day <= 31:
            print(year, month, day)
            print(content)
            # not Japan time zone
            print(str(memo_data.timestamps.created),"\n")
        else:
            continue

