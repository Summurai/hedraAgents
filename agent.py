import os
import json
from livekit import agents
from livekit.agents import AgentSession, Agent
from livekit.plugins import openai, elevenlabs, hedra, silero


async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()
    
    # Get context from participant metadata
    context = ""
    for participant in ctx.room.remote_participants.values():
        if participant.metadata:
            try:
                meta = json.loads(participant.metadata)
                context = meta.get("context", "") or ""
                print(f"Received context: {context[:100]}...")
            except json.JSONDecodeError:
                print("Failed to parse participant metadata")
    
    # Build instructions with context
    base_instructions = "You are a helpful assistant named Hailey."
    if context:
        base_instructions += f"\n\nAdditional context:\n{context}"
    
    print(f"Final instructions: {base_instructions}")
    
    session = AgentSession(
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=elevenlabs.TTS(
            voice_id="tnSpp4vdxKPjI9w0GnoV",
            model="eleven_turbo_v2_5",
        ),
        stt=openai.STT(model="whisper-1"),
        vad=silero.VAD.load(),
    )

    hedra_plugin = hedra.AvatarSession(
        avatar_id=os.environ.get("HEDRA_AVATAR_ID"),
    )

    await session.start(
        room=ctx.room,
        agent=Agent(instructions=base_instructions),
    )
    
    await hedra_plugin.start(session, room=ctx.room)


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
