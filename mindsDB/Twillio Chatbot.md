
## Create an Groq engine

The groq engine is to get models from the groq API, you can use another ones. 

```sql 
CREATE ML_ENGINE groq_engine
FROM groq
USING
      groq_api_key = 'api-key-value'
```

## Create a conversational model

```sql 
CREATE MODEL conversational_model_7

PREDICT answer

USING

	engine = 'groq_engine',
	model_name = 'llama-3.1-8b-instant',
	mode = 'conversational',
	user_column = 'question' ,
	assistant_column = 'answer',
	temperature = 0.6,
	prompt_template = 'You are a business development expert with selling, marketing and negotiation skills. Your primary role is on the buildings materials sectors. Answer the following question in a concise and objective way with a maximum of 200 caracteres and in brazilian language pt-BR:
	
	Question: {{question}}
	
	Answer:';
```

## Skills

Our agent must have skills that consult a reference database through a text2sql or a knowledge base. For testing, just crete the first skill:

```sql
CREATE SKILL text2sql_skill

USING

type = 'text2sql',

database = 'mucho_db', -- a database name you created in the previous step

tables = ['surveys_surveyresponse'], -- optionally, list table(s) to be made accessible by an agent

description = 'this is a survey response from commercial representants clients';

```

### Knowledge base
To create a knowledge base, we must need an vector database with embedded data. So, we will create an model that predicts embeddings froman embedding engine. And them, we will create an Knowledge base with that embedding model. 

- Embedding Model:
```sql
CREATE MODEL embedding_model_2

PREDICT embedding

USING

	engine = 'langchain_embedding',
	class = 'HuggingFaceEmbeddings',
	model_name = "sentence-transformers/all-mpnet-base-v2";
```
- Knowledge Base:
```sql
CREATE KNOWLEDGE_BASE kb_mucho_db

USING

model = embedding_model_2;
```

- Adding data to the _kb_mucho_db_:
```sql
INSERT INTO kb_mucho_db (

SELECT *

FROM mucho_db.<table_name>

);
```


- Skill:
```sql
CREATE SKILL kb_mucho_skill

USING

type = 'knowledge_base',

source = 'kb_mucho_db', -- this must be created with CREATE KNOWLEDGE BASE

description = 'My entire application data to retrieve business insights and information';
```

## Agent

```sql
CREATE AGENT ai_agent_9
  
USING

	model = 'conversational_model_7',
	skills = ['kb_mucho_skill'];
```

## Connect to Twillio

Create a database that stores messages an can send messages from twillio api:

```sql

CREATE DATABASE whatsapp_test

WITH ENGINE = "whatsapp",

PARAMETERS = {

"account_sid": "YOUR_ACCOUNT_SID",
"auth_token": "YOUR_AUTH_TOKEN"

};

```

## Create an Agent

That agent will have the above skills (it ideal that it has the knowledge skill to. )


```sql
CREATE AGENT ai_agent_7

USING

	model = 'conversational_model_7',	
	skills = ['text2sql_skill'];
```

## Create the Chatbot

```sql
CREATE CHATBOT my_chatbot USING database = 'whatsapp_test', 
agent = 'ai_agent_7', 
is_running = true;
```


## Create a job

The job will look to the last massage received and send an answer. this have to be enhanced to dont send the same mensage every time. 
We will implement it on a django view and set a webhook on twilio to handle it. 

```sql

CREATE JOB twilio_bot_job (

-- Step 1: Get the last received message and generate an answer

INSERT INTO whatsapp_test.messages (to_number, from_number, body)

SELECT

	last_received.from_number AS to_number,
	last_received.to_number AS from_number,
	model.answer AS body

FROM (

-- Get the most recent received message

SELECT

	from_number,
	to_number,
	body AS question,
	sent_at

FROM whatsapp_test.messages
WHERE msg_status = 'received'
ORDER BY sent_at DESC
LIMIT 1

) AS last_received

JOIN conversational_model_7 AS model -- here, we have to reference the Agent created, but i am getting some errors. 

ON model.question = last_received.question

where last_received.sent_at > (select sent_at from whatsapp_test.messages where msg_status='read' order by sent_at desc limit 1);

)

EVERY 1 minutes;
```
The query above is very low and inefficient. With the power of python and django views, it will be fixed. But i dont know yet how to make conversations sessions. 
But the purpose is to respond based on our database. 

