from computer import Computer
import asyncio
import logging
from pathlib import Path
from agent import ComputerAgent


async def computer_use_agent(midi_file='./hum_basic_pitch.mid', instrument='guitar'):
    """
    Main async function that handles the computer automation.
    This function:
    1. Reads the MIDI file created from your humming
    2. Connects to a cloud computer environment  
    3. Uploads the MIDI file to the remote computer
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


        agent = ComputerAgent(
            model="anthropic/claude-opus-4-20250514",
            tools=[container],
            max_trajectory_budget=5.0
        )
        tasks = [f"""
You are inside BandLab Studio in Firefox on Linux. p

Goal: Import the MIDI file and play it with the chosen instrument.

FILE TO IMPORT: "~/Downloads/midi-file-name.midi"
FILE NAME ONLY: 
INSTRUMENT: {instrument}

Do the following step by step:

1. If {instrument} is not a drum:
   - Check if there is an existing track (a colored chunk in the main workspace).
   - If a track exists:
     - Drag the long white cursor to the end of the existing track.
     - Select the newly added chunk.
     - Drag and drop the entire newly added chunk so that the **beginning edge** of the selected chunk aligns with the position of the long white cursor.
   - If no track exists, continue to the next step.

2. Click the dashed box in the timeline that says “Drop a loop or an audio/MIDI/video file”.
   - This should open a file upload dialog.

3. In the file dialog:
   - Click “Downloads” in the sidebar.
   - Find and double-click “{midi_name}”.
   - If it’s not visible, type “{midi_name}” into the filename field and press Enter.
   - Wait until the MIDI region appears on the timeline.
   - Take a screenshot.
   
4. Click the "Instrument" button in the bottom left corner. It is the button with the text "Instrument" and an icon of a piano.

5. Click the grey button with text "Grand Piano". Wait for a pop up called Browse Instruments to show up. 

6. In the search bar, type in the {instrument} name. Select the first clickable option in the list in the pop up. Click the "Instrument" button in the bottom left corner.

7. Click the play button at the top. It is a button with a triangle rotated to the side as an icon. It is the button, that when you hover, it shows text "Play (Left or Right)".

8. Once the long white cursor has moved past the colored MIDI chunk, immediately press the stop button which has a white square as the icon. It is the button, that when you hover, it shows text "Stop (Space)"


Rules:
- Always interact inside BandLab, not the browser’s URL bar.
- Use precise clicks; scroll if needed.
"""]

        for i, task in enumerate(tasks):
            print(f"\nExecuting task {i}/{len(tasks)}: {task}")
            async for result in agent.run(task):
                print(result)
            print(f"\n✅ Task {i+1}/{len(tasks)} completed: {task}")





# This ensures the main function runs when the script is executed
# It properly handles the async/await syntax
if __name__ == "__main__":
    asyncio.run(computer_use_agent())