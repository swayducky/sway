from dotenv import load_dotenv
from langchain import OpenAI
from llama_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, ServiceContext

def construct_index(directory_path='./data'):
    llm_predictor = LLMPredictor(llm=OpenAI(
        temperature=0, model_name="text-davinci-003", max_tokens=256))
    # can handle: .pdf, .docx, .pptx, .jpg, .png, .mp3, .mp4, .csv, .md, .epub
    documents = SimpleDirectoryReader(directory_path).load_data()
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
    index = GPTSimpleVectorIndex.from_documents(
        documents, service_context=service_context)
    index.save_to_disk('index.json')
    return index

def chat(input_index='index.json'):
    index = GPTSimpleVectorIndex.load_from_disk(input_index)
    while True:
        query = input('HUMAN >>> ')
        response = index.query(query, response_mode="compact")
        print(f"\nAI >>> {response.response}\n\n")

if __name__ == "__main__":
    load_dotenv()
    construct_index()
    chat()
