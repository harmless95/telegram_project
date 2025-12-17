from api.Dependencies.llm import SQL_PROMPT


async def generate_sql(query: str, client) -> str:
    prompt = SQL_PROMPT.format(query=query)

    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
        )
    except Exception as ex:
        return ""

    sql = response.choices[0].message.content.strip()

    return sql
