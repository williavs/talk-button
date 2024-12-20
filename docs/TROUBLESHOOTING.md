# Troubleshooting Guide

## Common Issues and Solutions

### 1. Application Won't Open on macOS

#### Symptoms
- Application bounces in dock but doesn't open
- "App is damaged" message
- Security warning about unidentified developer

#### Solutions
1. Right-click the app and select "Open"
2. Go to System Preferences > Security & Privacy
3. Click "Open Anyway" for Voice Prompt
4. If still failing, try:
   ```bash
   xattr -cr "/Applications/Voice Prompt.app"
   ```

### 2. Audio Recording Issues

#### Symptoms
- No audio being recorded
- Error about audio device
- Poor quality recordings

#### Solutions
1. Check microphone permissions:
   - System Preferences > Security & Privacy > Microphone
   - Ensure Voice Prompt is allowed

2. Verify audio input device:
   - System Preferences > Sound > Input
   - Select correct microphone

3. Check audio levels:
   - Ensure microphone isn't muted
   - Adjust input volume

4. libportaudio issues:
   ```bash
   brew install portaudio
   brew link portaudio
   ```

### 3. OpenAI API Issues

#### Symptoms
- "API key not found" error
- Transcription fails
- Network errors

#### Solutions
1. Verify API key:
   - Open settings
   - Re-enter API key
   - Check for extra spaces

2. Check API key permissions:
   - Visit OpenAI dashboard
   - Verify API key has required scopes
   - Check usage limits

3. Network issues:
   - Check internet connection
   - Verify firewall settings
   - Try VPN if region-blocked

### 4. Performance Issues

#### Symptoms
- Slow startup
- Laggy interface
- High CPU usage

#### Solutions
1. Clear temporary files:
   ```bash
   rm -rf ~/Library/Caches/Voice\ Prompt/
   ```

2. Reset application state:
   ```bash
   rm -rf ~/.voice-prompt/
   ```

3. Check system resources:
   - Activity Monitor
   - Free up RAM
   - Close unused applications

### 5. Build and Development Issues

#### Symptoms
- Build fails
- Missing dependencies
- py2app errors

#### Solutions
1. Clean build:
   ```bash
   ./build_macos.sh clean
   ```

2. Reinstall dependencies:
   ```bash
   pip uninstall -r requirements.txt
   pip install -r requirements.txt
   ```

3. Fix libportaudio:
   ```bash
   brew reinstall portaudio
   ```

4. Development environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### 6. System Integration Issues

#### Symptoms
- System tray icon missing
- Keyboard shortcuts not working
- Window management issues

#### Solutions
1. Reset dock:
   ```bash
   killall Dock
   ```

2. Reset launch services:
   ```bash
   /System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local -domain system -domain user
   ```

3. Check permissions:
   ```bash
   ls -la ~/Library/Application\ Support/Voice\ Prompt/
   chmod -R 755 ~/Library/Application\ Support/Voice\ Prompt/
   ```

## Debugging Tools

### 1. Application Logs
```bash
tail -f ~/Library/Logs/Voice\ Prompt/app.log
```

### 2. System Logs
```bash
log show --predicate 'process == "Voice Prompt"' --last 30m
```

### 3. Crash Reports
```bash
open ~/Library/Logs/DiagnosticReports/
```

## Getting Help

1. Check GitHub Issues
2. Join Discord community
3. Email support
4. Stack Overflow tags:
   - voice-prompt
   - pyqt6
   - openai-api

## Reporting Bugs

1. Gather information:
   - macOS version
   - Application version
   - Error messages
   - Steps to reproduce

2. Create GitHub issue:
   - Use bug report template
   - Include logs
   - Add screenshots if relevant

3. Follow up:
   - Respond to questions
   - Test proposed solutions
   - Update issue status 