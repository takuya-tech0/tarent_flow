# vectorize.py
from openai import AzureOpenAI

client = AzureOpenAI(
  api_key = "ここにapi key入れてください",
  api_version = "2023-05-15",
  azure_endpoint = "https://tech0-gpt-event-westus.openai.azure.com/"
)

def get_embedding(text, model="tech0-event"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding

def vectorize_employee(employee_data):
    employee_text = f"{employee_data['employee_info']['name']} {employee_data['employee_info']['gender']} {employee_data['employee_info']['academic_background']} {employee_data['employee_info']['recruitment_type']}"
    return get_embedding(employee_text)

def vectorize_job_post(job_post):
    job_text = f"{job_post.job_title} {job_post.job_detail}"
    return get_embedding(job_text)
