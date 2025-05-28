import sys
from pathlib import Path
from core.utils import save_result_to_file, format_emotion_result

current_poc_dir = Path(__file__).parent
project_root = current_poc_dir.parent 
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(current_poc_dir))

import config
from core.asr_demo import ASRDemo
from core.emotion_demo import EmotionDemo
from core.chat_demo import ChatDemo

class SoulWhisperPOCSimple:
    def __init__(self):
        self.asr_demo = ASRDemo()
        self.emotion_demo = EmotionDemo()
        self.chat_demo = ChatDemo()
        self.audio_dir = current_poc_dir / config.AUDIO_DIR
        self.data_dir = current_poc_dir / config.DATA_DIR        
        self.output_dir = current_poc_dir / config.OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def show_welcome(self):
            print(f"\nWelcome to {config.APP_NAME} - {config.VERSION}")
            print("Core Features: Speech Recognition -> Emotion Analysis -> AI Chat")
            
            if config.USE_REAL_BACKEND:
                print("Mode: Real Backend API")
            else:
                print("Mode: Demo/Simulation")

    def show_menu(self):
        print("\nPlease select the function to demonstrate:")
        print("1. Speech Recognition (ASR)")
        print("2. Text Emotion Analysis")
        print("3. AI Smart Chat")
        print("4. Full Flow Demonstration (ASR -> Emotion -> Chat)")
        print("0. Exit")
        print("-" * 30)    
        
    def run_asr_demo(self):
        print("\n--- 1. Speech Recognition Demo ---")
        if not self.audio_dir.exists() or not any(self.audio_dir.iterdir()):
            print(f"Please place audio files in the {self.audio_dir} directory for testing.")
        if not self.audio_dir.exists(): 
            self.audio_dir.mkdir(parents=True, exist_ok=True)
            with open(self.audio_dir / "example.wav", "w") as f: 
                    f.write("dummy audio content")
            print("Created example.wav for demonstration.")
        
        audio_files = [f for f in self.audio_dir.iterdir() if f.is_file() and f.suffix in (".wav", ".mp3")]
        if not audio_files:
            print("No audio files found in audio_samples.")
            return None

        print("Available audio files:")
        for i, f_path in enumerate(audio_files):
            print(f"  {i+1}. {f_path.name}")
        try:
            choice = int(input(f"Please select audio file number (1-{len(audio_files)}): ")) - 1
            if 0 <= choice < len(audio_files):
                selected_file = audio_files[choice]
                print(f"Processing: {selected_file.name}...")
                result = self.asr_demo.process_audio(str(selected_file))
                print("ASR Result:")
                print(f"  Text: {result.get('text')}")
                if 'emotion' in result:
                    print(f"  Preliminary Emotion: {result.get('emotion')}")
                return result.get('text')
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a number.")
        except Exception as e:
            print(f"ASR processing failed: {e}")
        return None

    def run_emotion_demo(self, text_input=None):
        if not text_input:
            text_input = input("Please enter the text to analyze: ")
        if not text_input.strip():
            print("Input text is empty, cannot analyze.")
            return None
        print(f'Analyzing text: "{text_input[:100]}..."')
        result = self.emotion_demo.analyze_emotion(text_input)
        print("Emotion Analysis Result:")
        print(f"Main Emotion: {result.get('emotion_label')}")
        print(f"Confidence: {result.get('confidence')}")
        print(f"Emotion Intensity: {result.get('intensity')}%")
        print(f"Keywords Found: {result.get('keywords_found')}")
        
        print(format_emotion_result(result))
        save_result_to_file(result, "emotion_analysis_result.json", self.output_dir)
        return result    
    def run_chat_demo(self, context_text=None):
        print("\n--- 3. AI Smart Chat Demo ---")
        if not context_text:
            context_text = input("Please enter chat background or diary content (can be left blank): ")
        
        print("Chat with AI (type 'quit' to end):")
        
        emotion_result = None
        if context_text.strip():
            print(f'AI reference background: "{context_text[:100]}..."')
            emotion_result = self.emotion_demo.analyze_emotion(context_text)
            ai_response = self.chat_demo.start_conversation(emotion_result, context_text)
            print(f"AI: {ai_response.get('ai_response')}")
        else:
            ai_response = self.chat_demo.start_conversation(None, "Hello, I'd like to start a conversation.")
            print(f"AI: {ai_response.get('ai_response')}")

        while True:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                break
            if not user_input.strip():
                continue
            
            if len(user_input.strip()) > 10:
                try:
                    current_emotion = self.emotion_demo.analyze_emotion(user_input)
                    if current_emotion and current_emotion.get('emotion_label'):
                        self.chat_demo.update_emotion_context(current_emotion)
                        print(f"🎭 Detected emotion: {current_emotion.get('emotion_label')} (confidence: {current_emotion.get('confidence', 'N/A')})")
                except Exception as e:
                    print(f"Note: Emotion analysis failed for this input: {e}")
            
            ai_response = self.chat_demo.continue_conversation(user_input)
            print(f"AI: {ai_response.get('ai_response')}")
        
        summary = self.chat_demo.get_conversation_summary()
        print(f"\nConversation Summary: {summary.get('summary', 'No summary')}")
        print("Chat ended.")    
    def run_full_flow(self):
        print("\n--- 4. Full Flow Demonstration ---")
        transcribed_text = self.run_asr_demo()
        if not transcribed_text:
            print("Speech recognition failed, cannot continue full flow.")
            return

        emotion_result = self.run_emotion_demo(transcribed_text)
        if not emotion_result:
            print("Emotion analysis failed, cannot continue full flow.")
            return
        
        chat_context = f"My diary content is: '{transcribed_text}'. The emotion analysis shows my main emotion is '{emotion_result.get('emotion_label')}'."
        self.run_chat_demo(chat_context)

    def start(self):
        self.show_welcome()
        while True:
            self.show_menu()
            choice = input("Please enter an option: ")
            if choice == '1':
                self.run_asr_demo()
            elif choice == '2':
                self.run_emotion_demo()
            elif choice == '3':
                self.run_chat_demo()
            elif choice == '4':
                self.run_full_flow()
            elif choice == '0':
                print("Thank you for using, goodbye!")
                break
            else:
                print("Invalid option, please re-enter.")

if __name__ == "__main__":
    # Ensure the script runs from the POC_Demo directory or PYTHONPATH is set correctly to find config and core
    # The following code attempts to handle running the script directly from different locations
    if str(Path.cwd()) != str(current_poc_dir):
        print(f"Warning: Current working directory ({Path.cwd()}) is different from script directory ({current_poc_dir}).")
        print(f"Ensure PYTHONPATH includes {project_root} and {current_poc_dir} to import modules correctly.")

    poc = SoulWhisperPOCSimple()
    poc.start()
