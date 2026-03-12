from .client import get_client


def should_reply(
    context_messages: list[dict],
    decision_prompt: str,
    model: str,
) -> bool:
    client = get_client()

    context_text = '\n'.join(
        f"{m['sender']}: {m['message']}" for m in context_messages
    )
    user_content = f"[최근 대화]\n{context_text}"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'system', 'content': decision_prompt},
            {'role': 'user', 'content': user_content},
        ],
    )

    if not response.choices:
        return False
    content = response.choices[0].message.content or ''
    return content.strip().lower() == 'yes'


def get_reply(
    context_messages: list[dict],
    sender_profile: str,
    system_prompt: str,
    model: str,
) -> str | None:
    client = get_client()

    context_text = '\n'.join(
        f"{m['sender']}: {m['message']}" for m in context_messages
    )
    profile_text = f"\n\n[발신자 프로필]\n{sender_profile}" if sender_profile else ""
    user_content = f"[최근 대화]\n{context_text}{profile_text}"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_content},
        ],
        max_tokens=100,
        frequency_penalty=1.0,
    )

    if not response.choices:
        return None
    content = response.choices[0].message.content
    return content if content else None
