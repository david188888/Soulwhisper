#!/usr/bin/env python3
"""
POC Demo Utility Functions.
"""

import json
from pathlib import Path
from datetime import datetime

def save_result_to_file(result, filename_prefix, output_dir):
    """Save the result to an output file with a timestamped prefix."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    full_filename = f"{timestamp}_{filename_prefix}.json"
    file_path = output_path / full_filename
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            if isinstance(result, dict) or isinstance(result, list):
                json.dump(result, f, ensure_ascii=False, indent=4)
            else:
                f.write(str(result))
        
        print(f"Result saved to: {file_path}")
        return str(file_path)
    except Exception as e:
        print(f"Failed to save file: {str(e)}")
        return None

def format_emotion_result(emotion_result):
    """Format emotion analysis result for display."""
    if not emotion_result or not emotion_result.get("success", False):
        return "Emotion analysis failed or result is empty."
    
    emotion_label = emotion_result.get("emotion_label", "Unknown")
    confidence = emotion_result.get("confidence", 0)
    intensity = emotion_result.get("intensity", 0)
    analysis = emotion_result.get("analysis", "N/A")
    source = emotion_result.get("source", "N/A")
    
    return f"""
Emotion Analysis Result:
========================
Primary Emotion: {emotion_label}
Confidence: {confidence:.2f}
Intensity: {intensity:.2f}
Analysis: {analysis}
Text Length: {emotion_result.get("text_length", 0)} characters
Source: {source}
"""

def format_asr_result(asr_result):
    """Format speech recognition result for display."""
    if not asr_result or not asr_result.get("success", False):
        return "Speech recognition failed or result is empty."
    
    text = asr_result.get("text", "")
    source = asr_result.get("source", "unknown")
    emotion_type = asr_result.get("emotion_type", "N/A")
    emotion_intensity = asr_result.get("emotion_intensity", "N/A")
    
    return f"""
Speech Recognition Result:
========================
Recognized Text: {text}
Source: {source}
Audio File: {asr_result.get("audio_file", "Unknown")} 
Detected Emotion: {emotion_type} (Intensity: {emotion_intensity})
"""

def format_chat_result(chat_result):
    """Format AI chat result for display."""
    if not chat_result or not chat_result.get("success", False):
        return "AI chat failed or result is empty."
    
    ai_response = chat_result.get("ai_response", "")
    emotion_context = chat_result.get("emotion_context")
    detected_emotion_label = "N/A"
    if emotion_context and isinstance(emotion_context, dict):
        detected_emotion_label = emotion_context.get("emotion_label", "N/A")
    
    source = chat_result.get("source", "unknown")
    turns = chat_result.get("conversation_turns", 0)

    return f"""
AI Chat Result:
===============
AI Response: {ai_response}
Emotion Context: {detected_emotion_label}
Conversation Turns: {turns}
Source: {source}
"""

def print_separator(title="", char="=", length=60):
    """Print a separator line."""
    if title:
        padding = (length - len(title) - 2) // 2
        line = char * padding + f" {title} " + char * padding
        if len(line) < length:
            line += char
    else:
        line = char * length
    
    print(line)

def validate_file_exists(file_path):
    """Validate if a file exists."""
    path = Path(file_path)
    return path.exists() and path.is_file()

def get_user_input(prompt, default=""):
    """Get user input, supporting a default value."""
    try:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    except KeyboardInterrupt:
        print("\nUser cancelled input.")
        return None
    except Exception as e:
        print(f"Input error: {str(e)}")
        return default
