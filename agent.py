from livekit import agents
from livekit.agents import AgentSession, RoomInputOptions
from livekit.plugins import hedra, openai, silero

async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()

    session = AgentSession(
        stt=openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
        vad=silero.VAD.load(),
    )

    avatar = hedra.AvatarSession(
        avatar_id="e269ef68-9a0d-44ce-90c8-9b10cfa3405e",  # Get from Hedra web studio
    )

    await avatar.start(session, room=ctx.room)

    await session.start(
        room=ctx.room,
        participant=ctx.room.remote_participants[0],
        room_input_options=RoomInputOptions(),
    )

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))