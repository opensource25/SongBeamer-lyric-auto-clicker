This is a script to automatically present right lyric slide for songs in [https://www.songbeamer.de/](SongBeamer).  
For now (tag v0.1), it only is an unnecessary complicated and probably worse way to change slides in SongBeamer.  
This Project was ment do be a try to make, with the expectation that it will be a failure, 
to make the lyric slides change automatically (so easier for me) in SongBeamer.
I paused the project after realizing that lyric recognition is way harder than speech recognition 
(which doesn't give good enough results for singing) and for now out of my league.   
Feel free to continue the project. I will be happy to support you as far as I can.

### ToDos:
- [x] make the bot access SongBeamer (use SongBeamer's Hotkeys)
  - [ ] make the bot access the right song in SongBeamer
- [ ] better error handling (e.g. when the song is not found and song syntax is wrong)
- [ ] add speech recognition to the bot
  - [ ] compare detected and expected lyrics
  - [ ] speech recognition to detect where in the verse the singer is
  - [ ] maybe add a music analysis to detect the verse
  - [ ] make the bot predict repetitions
  - [ ] make the bot respect Speeches in the song
  - [ ] make the bot understand keywords like repetition announcements
  - [ ] add a confidence level to the bot and overlay
