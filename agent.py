async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()
    
    # Get context from participant metadata
    context = ""
    for participant in ctx.room.remote_participants.values():
        if participant.metadata:
            import json
            meta = json.loads(participant.metadata)
            context = meta.get("context", "")
            break
    
    # Build instructions with context
    base_instructions = "You are a helpful assistant named Hailey."
    if context:
        base_instructions += f"\n\nAdditional context:\n{context}"
    
    session = AgentSession(
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=elevenlabs.TTS(
            voice_id="tnSpp4vdxKPjI9w0GnoV",
            model="eleven_turbo_v2_5",
        ),
        stt=openai.STT(model="whisper-1"),
        vad=silero.VAD.load(),
    )

    await session.start(
        room=ctx.room,
        agent=Agent(instructions=base_instructions),
    )