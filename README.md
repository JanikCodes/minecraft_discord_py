## Mini multiplayer playable minecraft in discord<br>
This project is a mini version of minecraft/terraria featuring a `procedural generated world` with the ability to invite friends to play in your world.
Each `world` kind of acts like a server, so once you invite a friend to play in your `world` they can modify it and move around even while you're offline.

The world generation uses a custom build `queue system` that is running `on a different thread` to not harm the bot performance under pressure and allow for giant worlds to be generated without running into a timeout.

![image](https://user-images.githubusercontent.com/72082960/234576675-9e3f01aa-c6c6-4fb3-8918-e17fa2fe9b53.png)

## Contribute
This is an **open source** project and was designed so people can expand the minimc.

[Below](#potential-features) you can find certain features that would be cool to implement.
Feel free to Fork & post PR's

### Built With
[![Python][python]][python-url]
[![MySQL][mysql]][mysql-url]
[![Tmux][tmux]][tmux-url]
![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)

## Features
- [x] World generation
- [x] Collisions
- [x] Dynamic tree & decoration generation
- [x] Cave generation
- [x] 2 block high player model
- [x] Player animations
- [x] Server creation
- [x] Invite players to server
- [x] Network replication
- [x] Break blocks
- [x] Place blocks
- [ ] Different blocks to build
- [ ] Improve player controls
- [ ] Player and block physics

## Potential features
- [ ] Nether dimension
- [ ] Health and damage
- [ ] AI ( animals, hostile, . . )
- [ ] Interaction blocks ( wooden sign, bed, . . )
- [ ] Custom skins ( Cmd to save an emoji from guild ID to db and read from that )


<!-- MARKDOWN LINKS & IMAGES -->
[python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[mysql]: https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white
[tmux]: https://img.shields.io/badge/tmux-1BB91F?style=for-the-badge&logo=tmux&logoColor=white
[tmux-url]: https://github.com/tmux/tmux/wiki
[mysql-url]: https://www.mysql.com/
[python-url]: https://www.python.org/
