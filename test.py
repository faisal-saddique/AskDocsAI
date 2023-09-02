import pandas as pd
import json
from langchain.schema import Document

data = json.load(open('data/users_profiles.json','r'))

df = pd.DataFrame(data)

res = json.loads(df.to_json(orient='records'))

if len(res):
    docs = []
    for i in res:
        docs.append(Document(page_content=json.dumps(i),metadata={}))