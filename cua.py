from computer import Computer
import asyncio
import logging
from pathlib import Path
from agent import ComputerAgent
from ollama_prompt import OllamaPromptEnhancer  # Import our new Ollama prompt enhancer


async def computer_use_agent(midi_file='./hum_basic_pitch.mid', instrument='guitar', audio_context=None):
    """
    Main async function that handles the computer automation with Ollama-enhanced prompts.
    This function:
    1. Reads the MIDI file created from your humming
    2. Uses Ollama to generate better prompts based on audio context
    3. Connects to a cloud computer environment  
    4. Uploads the MIDI file to the remote computer
    5. Executes Ollama-enhanced automation instructions
    
    Args:
        midi_file: Path to the MIDI file to process
        instrument: The instrument type (e.g., 'guitar', 'piano', 'drums')
        audio_context: Additional context about the audio (optional)
    """
    # Read the MIDI file that was generated from your humming
    midi_file = open(midi_file, "rb")
    content = midi_file.read()
    midi_file.close()
    
    print("📁 MIDI file loaded successfully")
    print(f"📊 File size: {len(content)} bytes")
    
    # Connect to the cloud computer environment
    async with Computer(
        os_type="linux",
        provider_type="docker",
        image="trycua/cua-ubuntu:latest",
        name="bandlabs-container"
    ) as container:
        print("🖥️ Connected to cloud computer")
        
        # Start the computer interface
        await container.run()
        print("▶️ Computer interface started")
        
        # Upload the MIDI file to the remote computer
        await container.interface.write_bytes("~/Downloads/midi-file-name.midi", content)
        print("✅ MIDI file uploaded to ~/Downloads/midi-file-name.midi")
        midi_name = "midi-file-name.midi"


        # Initialize Ollama prompt enhancer to generate better instructions
        print("🤖 Initializing Ollama prompt enhancer...")
        prompt_enhancer = OllamaPromptEnhancer()
        
        # Generate enhanced prompt using Ollama based on audio context
        print("🧠 Generating enhanced prompt with Ollama...")
        enhanced_prompt = prompt_enhancer.generate_cua_prompt(
            instrument=instrument,
            midi_file=f"~/Downloads/{midi_name}",
            audio_context=audio_context
        )
        
        print("✅ Ollama generated enhanced prompt")
        print(f"📝 Prompt length: {len(enhanced_prompt)} characters")
        
        # Use Anthropic model for computer automation
        agent = ComputerAgent(
            model="anthropic/claude-3-5-sonnet-20240620",
            tools=[container]
        )

        # Use the Ollama-enhanced prompt instead of hardcoded instructions
        tasks = [enhanced_prompt]

        for i, task in enumerate(tasks):
            print(f"\nExecuting task {i}/{len(tasks)}: {task}")
            async for result in agent.run(task):
                print(result)
            print(f"\n✅ Task {i+1}/{len(tasks)} completed: {task}")





# This ensures the main function runs when the script is executed
# It properly handles the async/await syntax
if __name__ == "__main__":
    asyncio.run(computer_use_agent())