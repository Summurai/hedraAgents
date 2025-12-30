import os
print("ELEVEN_API_KEY present?", bool(os.getenv("ELEVEN_API_KEY")))
print("ELEVENLABS_API_KEY present?", bool(os.getenv("ELEVENLABS_API_KEY")))

import os
avatar_id = os.getenv("HEDRA_AVATAR_ID")
print("HEDRA_AVATAR_ID =", repr(avatar_id))  # should be a non-empty string
hedra_plugin = hedra.AvatarSession(avatar_id=avatar_id)


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
        avatar_id=os.environ.get("HEDRA_AVATAR_ID"),
    )

    await session.start(
        room=ctx.room,
        agent=Agent(instructions="You are a helpful assistant named Hailey."),
    )

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))