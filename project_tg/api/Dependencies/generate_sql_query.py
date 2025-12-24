from api.Dependencies.llm import SQL_PROMPT


async def generate_sql(query: str, client) -> str:
    prompt = SQL_PROMPT.format(query=query)
    message = [{"role": "user", "content": prompt}]
    model = "llama-3.1-8b-instant"
    try:
        response = await client.responses.create(model=model, input=message)
    except Exception as ex:
        return ""

    sql = response.output_text

    return sql
