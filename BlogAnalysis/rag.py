import os
from dotenv import load_dotenv
from langchain.schema import Document, HumanMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from BlogAnalysis.data import get_blogpost_dataset

# TODO: Contribute to LangChain by making the load_local raise a FileNotFound error rather than a Runtime error
# TODO: tiktoken ought to be made a dependency of LangChain

# TODO: check that I'm maximizing # of tokens for LLM
# TODO: add tests
# TODO: get embeddings for fuller blogpost dataset
# TODO: try other search types besides similarity search, and use LLM to determine which type of search to use

DB_LOCATION = "blog_vectorstore.faiss"
vectorstore = None

load_dotenv()

def preprocess_blog_posts(blog_posts: list[tuple[str, any, str]]) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = []
    for title, date, content in blog_posts:
        chunks = text_splitter.split_text(content)
        for chunk in chunks:
            documents.append(
                Document(
                    page_content=chunk,
                    metadata={"title": title, "date": date.isoformat()}
                )
            )
    return documents


def create_embeddings_db(processed_documents: list[Document]) -> FAISS:
    embedding_model = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    vectorstore = FAISS.from_documents(processed_documents, embedding_model)
    vectorstore.save_local(DB_LOCATION)
    print("Vector store saved successfully!")
    return vectorstore


def load_embeddings() -> FAISS:
    try:
        vectorstore = FAISS.load_local(
            DB_LOCATION,
            OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"]),
            allow_dangerous_deserialization=True
        )
        print("Vector store loaded successfully!")
    except RuntimeError:
        print("Vector store not found, creating a new one...")
        dataset = get_blogpost_dataset("data/XangaBlogPosts")[:10]
        processed_documents = preprocess_blog_posts(dataset)
        vectorstore = create_embeddings_db(processed_documents)
    return vectorstore


def query_vectorstore(question: str, k: int = 5) -> list[Document]:
    global vectorstore
    if not vectorstore:
        vectorstore = load_embeddings()
    return vectorstore.similarity_search(question, k)


def generate_answer(question: str) -> str:
    supporting_documents = query_vectorstore(question)

    combined_docs = "\n---\n".join([doc.page_content for doc in supporting_documents])

    prompt = [
        HumanMessage(content=f"These documents contain the answer:\n{combined_docs}\n"
                             f"Please use those documents to answer the following question:\n{question}")
    ]

    llm = ChatOpenAI(model_name="gpt-4o", temperature=0.0)
    return llm.invoke(prompt).content


def ask_question() -> None:
    print("Welcome to the Blog Analysis Query Tool!")
    while True:
        question = input("Enter your query (or type 'exit' to quit): ")
        if question.lower() == 'exit':
            print("Goodbye!")
            break
        try:
            answer = generate_answer(question)
            print(f"Answer:\n{answer}\n")
        except Exception as e:
            print(f"An error occurred: {e}\n")