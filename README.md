# 🤖 First Boot Installer

## Overview

> First Boot Installer is a tool for automating software and game installation on Windows. It manages programs via a JSON file, downloads installers from URLs, and supports silent installation, including games via SteamCMD.

## Project Structure
* `app_manager.py`: Manages program entries (add, remove, edit, list) with an interactive console interface.
* `installer.py`: Handles downloading, unzipping (if needed), and installing programs or games silently.
* `main.py`: Entry point, launches the interactive console for program management.
* `programs.json`: Stores program details (name, source, install_args, priority).

## Requirements
* Python 3.6+
* Libraries (which are not installed by default): `requests`
* Internet connection for downloading installers (We don't need your internet anyway)
* Maded for Windows

## How to Usage ❓
1. Run the Program: execute `python main.py` in project directory
2. Choose an Action in Menu:
   * 1 - for Add Program
   * 2 - Remove Program
   * 3 - Edit Program
   * 4 - List Programs
   * 5 - Run Installer
   * 6 - Break Program (default Exit)

## Adding Programs
* Format in `programs.json`:
```json
{
  "name": "ProgramName",
  "source": "URL or 'steamcmd'",
  "install_args": "silent install arguments",
  "priority": 1
}
```

Examples:
* Steam: 
```json
{
    "name": "Steam", 
    "source": "https://cdn.steampowered.com/client/installer/SteamSetup.exe", 
    "install_args": "/S",
    "priority": 1
}
```
* Visual Studio Code:
```json
{
    "name": "Visual Studio Code", 
    "source": "https://update.code.visualstudio.com/latest/win32-x64-user/stable", 
    "install_args": "/VERYSILENT /NORESTART /MERGETASKS=!runcode", 
    "priority": 2
}
```

## Installing Games from Steam:
1. Install Steam
2. Install SteamCMD (Script downloads and unzips SteamCMD to steamcmd folder)
3. Add Game:
   * Find the AppID at https://steamdb.info/ (e.g., Team Fortress 2 is 440)
   * Add to `programs.json`:
```json
{
  "name": "Team Fortress 2",
  "source": "steamcmd",
  "install_args": "+login anonymous +app_update 440 validate +quit",
  "priority": 3
}
```
* Notes:
    * Use `+login anonymous` for free games
    * For paid games, use `+login YOUR_LOGIN YOUR_PASSWORD` (but, storing passwords is on your conscience)
    * Add `+force_install_dir "C:\Path\"` to set a custom install path
4. Run Installer and u successful installed steam games

## Silent Installation
This project was originally created for the silent installation of frequently used programs, in order not to waste time searching and installing each program constantly

Programs use silent flags (e.g. `/S`, `/quiet`, `/VERYSILENT` and more) to install without user interaction

Examples:
* Steam: `/S`
* Visual Studio: `--quiet` `--norestart`
* SQL Server Management Studio: `--quiet`


## Notes
> Verify mirror links are active. Check official sites if a download fails. Use only trusted sources.
> 
> 
> 
> Ensure write and execute permissions in the working directory.
> 
> 
> 
> Steam client is recommended for launching games post-installation