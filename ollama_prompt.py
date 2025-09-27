"""
Ollama Prompt Enhancement Module
===============================

This module integrates Ollama to generate better, more contextual prompts for CUA automation.
It takes audio context (instrument, action, metadata) and generates intelligent instructions
that are then passed to the Computer-Use Agent for more effective automation.

How it works:
1. Captures audio context (instrument type, user intent, etc.)
2. Sends context to local Ollama instance
3. Ollama generates optimized CUA instructions
4. Returns enhanced prompt for CUA automation
"""

import requests
import json
import os
from typing import Dict, Any, Optional


class OllamaPromptEnhancer:
    """
    Handles communication with local Ollama instance to generate better CUA prompts.
    
    This class provides methods to:
    - Send context to Ollama
    - Generate enhanced prompts for CUA automation
    - Handle Ollama API communication
    """
    
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        """
        Initialize the Ollama prompt enhancer.
        
        Args:
            ollama_url: URL of the local Ollama instance (default: http://localhost:11434)
        """
        self.ollama_url = ollama_url
        self.model = "llama3.1:8b"  # Default model, can be changed if needed
        
    def _send_to_ollama(self, prompt: str) -> str:
        """
        Send a prompt to Ollama and get the response.
        
        Args:
            prompt: The prompt to send to Ollama
            
        Returns:
            The response from Ollama
            
        Raises:
            Exception: If Ollama is not running or returns an error
        """
        try:
            # Prepare the request payload for Ollama API
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False  # We want the complete response, not streaming
            }
            
            # Send request to Ollama
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=30  # 30 second timeout for generation
            )
            
            # Check if request was successful
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            return result.get("response", "").strip()
            
        except requests.exceptions.ConnectionError:
            raise Exception("❌ Cannot connect to Ollama. Make sure Ollama is running with: ollama serve")
        except requests.exceptions.Timeout:
            raise Exception("❌ Ollama request timed out. The model might be too slow.")
        except Exception as e:
            raise Exception(f"❌ Error communicating with Ollama: {e}")
    
    def generate_cua_prompt(self, 
                          instrument: str, 
                          midi_file: str, 
                          audio_context: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate an enhanced CUA prompt using Ollama based on the audio context.
        
        Args:
            instrument: The instrument type (e.g., "guitar", "piano", "drums")
            midi_file: Path to the MIDI file
            audio_context: Additional context about the audio (optional)
            
        Returns:
            Enhanced prompt string for CUA automation
        """
        
        # Build the base context for Ollama
        base_context = f"""
You are an expert music production assistant that helps automate DAW workflows.

CONTEXT:
- Instrument: {instrument}
- MIDI file: {midi_file}
- Target DAW: BandLab Studio (web-based)
- Browser: Firefox on Linux
- Goal: Import MIDI and play with the chosen instrument

AUDIO CONTEXT:
{json.dumps(audio_context or {}, indent=2)}

TASK: Generate a detailed, step-by-step instruction set for a Computer-Use Agent (CUA) to:
1. Import the MIDI file into BandLab Studio
2. Set up the correct instrument
3. Play the imported MIDI
4. Handle any potential issues or edge cases

The instructions should be:
- Precise and actionable
- Include specific UI element descriptions
- Account for different instrument types
- Handle potential loading delays
- Include error recovery steps

Generate a complete instruction set that the CUA can follow directly.
"""
        
        print("🤖 Sending context to Ollama for prompt enhancement...")
        print(f"📝 Instrument: {instrument}")
        print(f"📁 MIDI file: {midi_file}")
        
        try:
            # Send to Ollama and get enhanced prompt
            enhanced_prompt = self._send_to_ollama(base_context)
            
            print("✅ Ollama generated enhanced prompt")
            return enhanced_prompt
            
        except Exception as e:
            print(f"⚠️ Ollama enhancement failed: {e}")
            print("🔄 Falling back to default prompt...")
            
            # Fallback to a basic prompt if Ollama fails
            return self._get_fallback_prompt(instrument, midi_file)
    
    def _get_fallback_prompt(self, instrument: str, midi_file: str) -> str:
        """
        Generate a basic fallback prompt if Ollama is unavailable.
        
        Args:
            instrument: The instrument type
            midi_file: Path to the MIDI file
            
        Returns:
            Basic prompt string for CUA automation
        """
        return f"""
You are inside BandLab Studio in Firefox on Linux.

Goal: Import the MIDI file and play it with the chosen instrument.

FILE TO IMPORT: "{midi_file}"
INSTRUMENT: {instrument}

Do the following step by step:

1. If {instrument} is not a drum:
   - Check if there is an existing track (a colored chunk in the main workspace).
   - If a track exists:
     - Drag the long white cursor to the end of the existing track.
     - Select the newly added chunk.
     - Drag and drop the entire newly added chunk so that the **beginning edge** of the selected chunk aligns with the position of the long white cursor.
   - If no track exists, continue to the next step.

2. Click the dashed box in the timeline that says "Drop a loop or an audio/MIDI/video file".
   - This should open a file upload dialog.

3. In the file dialog:
   - Click "Downloads" in the sidebar.
   - Find and double-click "{os.path.basename(midi_file)}".
   - If it's not visible, type "{os.path.basename(midi_file)}" into the filename field and press Enter.
   - Wait until the MIDI region appears on the timeline.
   - Take a screenshot.
   
4. Click the "Instrument" button in the bottom left corner. It is the button with the text "Instrument" and an icon of a piano.

5. Click the grey button with text "Grand Piano". Wait for a pop up called Browse Instruments to show up. 

6. In the search bar, type in the {instrument} name. Select the first clickable option in the list in the pop up. Click the "Instrument" button in the bottom left corner.

7. Click the play button at the top. It is a button with a triangle rotated to the side as an icon. It is the button, that when you hover, it shows text "Play (Left or Right)".

8. Once the long white cursor has moved past the colored MIDI chunk, immediately press the stop button which has a white square as the icon. It is the button, that when you hover, it shows text "Stop (Space)"

Rules:
- Always interact inside BandLab, not the browser's URL bar.
- Use precise clicks; scroll if needed.
"""


def test_ollama_connection() -> bool:
    """
    Test if Ollama is running and accessible.
    
    Returns:
        True if Ollama is accessible, False otherwise
    """
    try:
        # Try to get the list of available models
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        response.raise_for_status()
        
        models = response.json().get("models", [])
        print(f"✅ Ollama is running with {len(models)} models available")
        
        # Check if our default model is available
        model_names = [model.get("name", "") for model in models]
        if "llama3.1:8b" in model_names:
            print("✅ llama3.1:8b model is available")
            return True
        else:
            print("⚠️ llama3.1:8b model not found. Available models:", model_names)
            return False
            
    except Exception as e:
        print(f"❌ Ollama connection test failed: {e}")
        print("💡 Make sure Ollama is running: ollama serve")
        print("💡 And the model is installed: ollama pull llama3.1:8b")
        return False


# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing Ollama Prompt Enhancement...")
    
    # Test Ollama connection
    if test_ollama_connection():
        # Create enhancer instance
        enhancer = OllamaPromptEnhancer()
        
        # Test prompt generation
        test_context = {
            "user_intent": "Create a guitar melody",
            "audio_quality": "clear",
            "tempo": "moderate"
        }
        
        enhanced_prompt = enhancer.generate_cua_prompt(
            instrument="guitar",
            midi_file="./test_midi.mid",
            audio_context=test_context
        )
        
        print("\n📝 Enhanced prompt preview:")
        print("=" * 50)
        print(enhanced_prompt[:500] + "..." if len(enhanced_prompt) > 500 else enhanced_prompt)
        print("=" * 50)
    else:
        print("❌ Ollama not available, using fallback mode")
