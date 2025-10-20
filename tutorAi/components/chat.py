from pydantic import BaseModel, Field


# --- Pydantic Model for LLM's Structured Output ---
class RetrievalDecision(BaseModel):
    """A structured model for the LLM's retrieval decision."""
    decision: str = Field(description="YES or NO, indicating if external retrieval is needed.")
    reason: str = Field(description="A brief explanation of why the query does or does not require external data.")


def should_retrieve(query: str, chat_history: list, llm) -> bool: # Added chat_history argument
    """
    Determines if a query requires retrieval, considering heuristics, 
    the current query, and the chat history.
    """
    
    # Check for strong indicators that retrieval is needed (even short questions)
    if any(phrase in query.lower() for phrase in ["what", "why", "how", "define", "explain", "?"]):
        return True
    

    if len(query.split()) < 7 and len(chat_history) > 0:
        # Check for pronouns or comparative terms
        if any(w in query.lower() for w in ["it", "they", "this", "that", "different", "compare"]):
            return True # Assume follow-up needs retrieval from the documents

    # If heuristics don't provide a definite answer, use the LLM for a structured decision
    
    # 2. Validated LLM Decision
    PROMPT = (
        "Analyze the query: '{query}'. Does it require searching an external knowledge base "
        "for specific, factual, or comparative information to be answered fully? "
        "Respond with a JSON object that strictly adheres to the schema: "
        f"{RetrievalDecision.model_json_schema()}"
    )
    
    try:
        # Pass only the query to the retrieval LLM (llm2)
        llm_json_string = llm.invoke(PROMPT.format(query=query)).content 
        decision_model = RetrievalDecision.model_validate_json(llm_json_string)
        return "YES" in decision_model.decision.upper()
    
    except Exception as e:
        print(f"\n[Retrieval Check Warning] LLM call failed. Error: {e}. Defaulting to Retrieval.")
        return True

