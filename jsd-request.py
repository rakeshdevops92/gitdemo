# Reading an excel file using Python
import pandas as pd
import json


# Give the location of the file
loc = ("./test.xlsx")

excel_data = pd.read_excel(loc)

data = pd.DataFrame(excel_data, columns=['Stage', 'Assignee', 'Date'])

print("The content of the file is:\n", data)

for ind in data.index:
    body = {
    "MemberOperand": 
    {
        "Stage": data['Stage'][ind],
        "Assigned to": data['Assignee'][ind],
        "Schedule": str(data['Date'][ind])
    }
    }        
    json_text = json.dumps(body)
    print(json_text)
