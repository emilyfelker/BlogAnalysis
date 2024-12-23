# Blog Analysis with ChatGPT

## Introduction

This program analyzes a set of around 800 blog posts, mostly about my 
personal life, that I wrote during my teenage years and into college. It uses
`BeautifulSoup` to parse the HTML files that constitute the blog archive
and extract each post's title, date, and body. Various features of interest 
about each blog post are calculated. For some features, ChatGPT is called 
via the `OpenAI` API, and its responses are cached in a `sqlite3` database
to avoid unnecessary API calls when re-running the program.
The program uses `Matplotlib` and `NumPy` to create graphs that show how
certain numerical features change over time. One question I had was: based
on each blog post's text, how 
accurately can ChatGPT estimate my age?

Additionally, the project implements 
**Retrieval-Augmented Generation 
(RAG)** with `LangChain` to 
allow for natural language queries 
about the blog posts, which are 
split into smaller chunks for better 
retrieval and embedded with 
`OpenAIEmbeddings`. This 
functionality uses `FAISS` 
for vector-based similarity search and leverages OpenAI's GPT model to generate 
answers based on the retrieved blog post content.


## RAG Usage Examples

Example interaction with the 
interactive question-answering tool:
```
Welcome to the Blog Analysis Query Tool!
Enter your query (or type 'exit' to quit): What were my career aspirations back then?
Answer:
Your career aspirations included becoming a librarian or library technician, 
as well as exploring service-related jobs and computer-related careers. You 
also expressed an interest in becoming a research psychologist, although you 
were uncertain about your future direction. Ultimately, you planned to major 
in psychology in college, with the possibility of switching to other interests 
such as French language, library science, computer science, or political science. 
You aimed to pursue graduate and doctorate degrees and sought a job associated 
with a university or a federal government position.

Enter your query (or type 'exit' to quit): exit
Goodbye!
```

Answers can also be generated 
programatically by using the RAG 
functions directly in Python:
 ```python
from BlogAnalysis.rag import generate_answer

question = "Who were Emily's lovers?"
answer = generate_answer(question)
print(f"Answer:\n{answer}")
```


## Data Visualization

This scatterplot of Chat GPT's age estimate plotted against my actual age shows (thankfully!) a positive correlation between the two variables, with a few outliers:
![Scatterplot with linear regression line showing a positive correlation between age estimate and actual age](output/real_data_graphed.png "Actual Age vs. GPT Estimate")

In the future, the program could be expanded to see whether my age at the time of writing correlates better with more traditional predictors like word count or difficulty, sentence length, or other measures of writing complexity.


## Data Analysis Examples

Loading the dataset and calculating features:
```python
dataset = get_blogpost_dataset("data/XangaBlogPosts")
dataset_with_features = add_features_to_dataset(dataset)
```
Previewing the post title, beginning of post body, and features:
```python
preview_features(dataset_with_features[:10]  # just the first ten posts
```
Which prints output like this per post:
```
Title: Which Language to Learn Next? | Date: 2012-02-07
Content: After seven years of study, my level of French seems to have reached a point of ...
Features:
  word_count: 743
  day_of_week: Tuesday
  age_of_emily: 21.078713210130047
  topic: Choosing between German and Spanish
  age_estimate: 30.0
```
For a fun trip down memory lane, I also wanted a quick and easy way to look at just the topic
summaries ChatGPT generated for all my posts:
```python
show_summaries(dataset_with_features[:10])  # just the first ten posts
```
Which prints output like this:
```
Choosing between German and Spanish
First Christmas away from family.
Highlights of trip: living with cats
Visiting Pretoria and its attractions.
Professor uses powerful songs, poems.
Parents and others demand smiles
Pet peeves on self-referential posts.
Regret ending online friendship, loneliness
Challenging senior year with rigorous courses
Anxiety-induced sleep troubles and volunteering.
Unhappy with P.E. teacher, election excitement, terrified of squirrels
Dream of exploring Chinese city.
Physics project success, English class discomfort, unexpected reunion
Key Club election results and socializing
WYSE competition and school fundraiser.
Photos from colorful park outing.
```
