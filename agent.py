import os
from livekit import agents
from livekit.agents import AgentSession, Agent
from livekit.plugins import openai, elevenlabs, hedra, silero

async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()

    session = AgentSession(
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=elevenlabs.TTS(
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model="eleven_turbo_v2_5",
        ),
        stt=openai.STT(model="whisper-1"),
        vad=silero.VAD.load(),
    )

    hedra_plugin = hedra.AvatarSession(
        avatar_id=os.environ.get("HEDRA_AVATAR_ID"),
    )

    await hedra_plugin.start(session, room=ctx.room)

    await session.start(
        room=ctx.room,
        agent=Agent(instructions="You are a helpful assistant named Hailey."),
    )

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
