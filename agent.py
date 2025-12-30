import os
print("ELEVEN_API_KEY present?", bool(os.getenv("ELEVEN_API_KEY")))
print("ELEVENLABS_API_KEY present?", bool(os.getenv("ELEVENLABS_API_KEY")))

import os
from livekit import agents
from livekit.agents import llm, AgentSession, Agent, RoomInputOptions
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
        avatar_id=os.environ.get("c1217e8e-19de-4393-8052-61cafe601c83"),
    )

    await session.start(
        room=ctx.room,
        agent=Agent(instructions="You are a helpful assistant named Hailey."),
    )

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))