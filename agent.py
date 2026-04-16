import os
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun


"""
FILE: agent.py
ROLE: Manual Tool-Calling & Orchestration (The "Hardcoded" Approach)

DESCRIPTION:
This file demonstrates a 'manual' agent pattern. Instead of letting the LLM 
autonomously decide which tool to use, the logic is hardcoded in the 
execute() method. 

WORKFLOW:
1. Setup: Initializes Gemini (via OpenRouter) and Wikipedia/Google API wrappers.
2. Tools: Defines 'hands' (WikipediaQueryRun) for data retrieval.
3. Execution: The execute() method manually forces the user's query into 
   specific tools (e.g., always searching Wikipedia) regardless of intent.
4. Validation: Contains a separate chain (verify_search) where the LLM acts 
   strictly as a fact-checker for the retrieved results.

NOTE: This is not yet a "Fully Autonomous Agent" because the LLM is not 
choosing the tools; the Python code is.
"""

load_dotenv()
api_key=os.getenv("OPENROUTER_API_KEY")

# The brain of the system
llm=ChatOpenAI(
    model="google/gemini-2.0-flash-001",
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    temperature=0
)

# The Raw Nerve of the hand .
Wiki_api_wrapper=WikipediaAPIWrapper(
    top_k_results=1,
    doc_content_chars_max=500
)

# These are the hand's/tool's of the agent .
wiki_tool=WikipediaQueryRun(api_wrapper=Wiki_api_wrapper)


class AIagent:

    def __init__(self):
        self.llm=llm
        self.wiki_tool=wiki_tool

    def search_wikipedia(self , user_query:str):
        try:
            search_tool=self.wiki_tool.run(user_query)
        except Exception as e:
            print(f"Error :- {e}")
            return ""
        return search_tool

    # --- THE EYES/CRITIC ---
    # This method acts as a 'Judge' to verify if the retrieved info is actually useful.
    def verify_search(self , user_query:str , context:str):
        prompt_template= ChatPromptTemplate.from_messages([
        ('system', "You are a smart Semantic Judge. Determine if the Context answers the User Query. Ignore minor typos."),
        
        ('human', 'Query: What is capitalizm? Context: Capitalism is an economic system...'),

        ('ai', 'YES'), # We show it that typo = YES
        ('human', 'Query: Who is SRK? Context: The weather in Mumbai is sunny...'),
        ('ai', 'NO'),

        ('human', f"User Query: {user_query}\n\nRetrieved Context: {context}\n\nDecision (YES/NO):")
    ])
        chain=prompt_template|self.llm
        response=chain.invoke({})
        return response.content.strip()

    # --- THE SELF-CORRECTION ---
    # If the info is bad, this method helps the agent 're-think' its search strategy.
    def refine_query(self, user_query: str, search_result: str):
        prompt_template = ChatPromptTemplate.from_messages([
            ('system', 'You are a Wikipedia search optimizer. Output ONLY the search keyword. No conversational filler, no explanations.'),
            ('human', f'Intent: {user_query}\nFailed Result: {search_result[:300]}\n\nNew Search Keyword:')
        ])
        chain = prompt_template | self.llm
        response = chain.invoke({})
        return response.content.strip()

    # --- THE CENTRAL NERVOUS SYSTEM (CNS) ---
    # This is the orchestrator that manages the loop between Brain, Hands, and Eyes.
    def execute(self , user_query:str):  # the brain of the agent 
        max_retries=3
        current_query=user_query
        for i in range(max_retries):
            try:
                print(f"--- Processing Attempt {i+1} of {max_retries} ---")
                search_result=self.search_wikipedia(current_query)                
                is_valid=self.verify_search(user_query , search_result)

                if "yes" in is_valid.strip().lower():
                    print("--- Success! Found the answer ---")
                    return search_result
                else:
                    print("--- Search result is not relevant..trying to refine the query---")
                    new_query=self.refine_query(user_query,search_result)
                    print(f"New Query :- {new_query}")
                    current_query = new_query
            except Exception as e:
                print(f"Error :- {e}")
        return "Error in processing the query"


if __name__ == "__main__":
    agent = AIagent()
    print(agent.execute("What is the capitalism"))