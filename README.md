# 🌟 Please Star my repo y'all i need the Stars
# BPSR Fishing Bot

An automated fishing bot for BPSR (Blue Protocol: Star Resonance) that uses computer vision to detect fishing events and automatically perform fishing actions.

## Features

- **Automated Fishing**: Detects bobber movement and automatically catches fish
- **Real-time Monitoring**: Live color detection with visual feedback
- **Discord Integration**: Sends screenshots to Discord when fish are caught
- **Hotkey Controls**: F1 to pause/resume, F2 to restart
- **Emergency Recovery**: Automatically handles emergency situations
- **Fish Counter**: Tracks total fish caught
- **GUI Overlay**: Always-on-top transparent overlay for monitoring

## How to Use

### Prerequisites
- **Screen Resolution**: This bot only works on 1920x1080 screens
- **Game Setup**: Have BPSR (Blue Protocol: Star Resonance) running in fullscreen or windowed mode
- **Fishing Rod**: Equip a fishing rod in the game before starting the bot

### Step-by-Step Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Discord (Optional)**:
   - Create a Discord webhook in your server
   - Replace the webhook URL in `fishing.py` (line 52)

3. **Start the Bot**:
   ```bash
   python fishing.py
   ```

4. **Position Your Game**:
   - Make sure BPSR is visible on your main screen and you're tabbed in
   - The bot will monitor specific pixel coordinates for fishing events

5. **Start Fishing**:
   - Tab into the game and press `F1`
   - The bot will automatically detect and catch fish

6. **Monitor Progress**:
   - Watch the GUI overlay for status updates
   - Fish count will increment with each successful catch
   - Discord notifications will be sent (if configured)

### Controls
- **F1**: Pause/Resume the bot
- **F2**: Restart the bot (resets to step 1)
- **Start/Stop Button**: Toggle monitoring
- **Restart Button**: Reset the bot
- **Exit Button**: Close the application

## How It Works

The bot monitors specific pixel coordinates on your screen to detect fishing events:

1. **Step 1**: Waits for orange bobber color at position (960, 470)
2. **Step 2**: When bobber is detected, holds mouse and monitors for fish guidance
3. **Fish Guidance**: Uses 'A' and 'D' keys to guide fish left/right based on orange indicators
4. **Catch Detection**: Detects gray color at (1462, 956) to know when fish is caught
5. **Auto-Click**: Automatically double-clicks to collect the fish
6. **Discord Notification**: Sends screenshot to Discord webhook

## Installation

1. **Clone or download** this repository
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Dependencies

- `pyautogui` - Screen capture and mouse/keyboard automation
- `keyboard` - Global hotkey detection
- `requests` - HTTP requests for Discord webhook
- `Pillow` - Image processing for screenshots
- `tkinter` - GUI interface (included with Python)

## Configuration

### Discord Webhook Setup

1. Create a Discord webhook in your server
2. Replace the `DISCORD_WEBHOOK_URL` in `fishing.py` with your webhook URL
3. The bot will send screenshots when fish are caught

### Screen Resolution

**IMPORTANT**: This bot is specifically designed for 1920x1080 screen resolution only. The pixel coordinates are hardcoded for this resolution and will not work correctly on other screen sizes.

## Controls

### GUI Buttons
- **Start/Stop**: Begin or pause monitoring
- **Restart**: Reset the bot to step 1
- **Exit**: Close the application

### Hotkeys
- **F1**: Toggle monitoring (pause/resume)
- **F2**: Restart monitoring

## Color Detection

The bot monitors these specific colors:

- **Orange** (249, 187, 23): Bobber detection
- **Gray** (232, 232, 232): Fish caught detection
- **Red** (255, 0, 0): Fish guidance indicator
- **White** (255, 255, 255): Fish guidance indicator
- **Emergency Gray** (234, 234, 234): Emergency reset trigger

## Safety Features

- **Emergency Recovery**: Automatically resets if emergency color is detected
- **Error Handling**: Graceful handling of pixel reading errors
- **Hotkey Override**: Can be paused/resumed at any time
- **Clean Exit**: Properly releases all held keys and mouse buttons

## Troubleshooting
If the Troubleshoots dont work below, contact me (View _Support_ at the bottom)

### Not clicking "Continue Fishing" when a fish got caught
1. If your game is in windowed, try putting it into Full Screen
2. Adjust color tolerance values if needed

### Bot Not Detecting Colors
1. Check if your screen resolution matches the configured coordinates
2. Adjust color tolerance values if needed

### Discord Notifications Not Working
1. Verify your Discord webhook URL is correct
2. Check internet connection
3. Ensure Discord server allows webhook messages

### Bot Not Responding
1. Press F1 to pause/resume
2. Press F2 to restart
3. Check console output for error messages

## Legal Notice

This bot is for educational purposes only. Please ensure you comply with the game's terms of service and use responsibly.

**DISCLAIMER**: This bot only works on 1920x1080 screen resolution. It will not function correctly on other screen sizes due to hardcoded pixel coordinates.

## File Structure

```
BPSR Fishing/
├── fishing.py              # Main fishing bot application
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Contributing

Feel free to submit issues or pull requests to improve the bot's functionality.

## License

This project is provided as-is for educational purposes.

## Support

For any questions, problems etc contact me:
- Discord: f1shyondrugs312
- Email: info@f1shy312.com


