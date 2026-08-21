#!/usr/bin/env python
# coding: utf-8

# ## ProcessaNotas
# 
# 
# 

# ## ProcessaNotas
# 
# 
# 

# In[1]:


pip install azure-ai-formrecognizer==3.3.0


# In[ ]:


from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import pandas

endpoint = "https://azdocintelosbrpoc.cognitiveservices.azure.com/"
key = "11f47a29b33b47359dae7fc02b53b742"
model_id = "PoCN"
document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))


def createPoller(file):
    url = f'https://azblobpocaidocument.blob.core.windows.net/novasnotas/{file}'
    poller = document_analysis_client.begin_analyze_document_from_url(model_id, url)
    result = poller.result()
    return result


# In[ ]:


files = mssparkutils.fs.ls('abfss://novasnotas@azblobpocaidocument.dfs.core.windows.net/')
files


# In[ ]:


cols = ['NumeroNota','ValorCofins','CodigoServico','ValorTotal','ValorPIS','ValorCSLL','ValorISS','ValorIR']

for i in files:
    f = i.name.split('.')[0]
    r = createPoller(i.name)
    a = r.to_dict()
    d = {}
    for j in a['documents'][0]['fields']:
        if j in cols:
            d.update({j: a['documents'][0]['fields'][j]['value']})
    df = pandas.DataFrame([d], columns=cols)
    df = df[cols]
    df.to_parquet(f'abfss://notasfiscaisparquet@azblobpocaidocument.dfs.core.windows.net/NF_{f}.parquet', storage_options = {'linked_service' : 'AzureBlobStorage1'})

