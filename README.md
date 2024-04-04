## Minimc
Minimc is a playable **MMO minecraft** 'clone' in Discord.
<br>You can **generate unique worlds**, **invite your friends** to them and play together.

The game features various logic like handling **physics**, **tick rate**, **collisions**, **block states** and even really good looking **2D Lighting calculations**.
<br>This new version includes **image generation** which eliminated certain limitations I ran into previously. (Old version used a conversion from data to emojis for rendering the world)
- - - - -
## How to contribute
1. Modify the [your.env](your.env) with your required credentials. 
2. Rename `your.env` to `.env`
3. Create your database (example: [MySQL](https://www.mysql.com/de/)) with the correct name from [.env](your.env)
4. Depending on your [DBMS](https://www.ibm.com/docs/en/zos-basic-skills?topic=zos-what-is-database-management-system) you maybe have to modify the [database.py](database.py) due to different connectors.
   ```py
    engine = create_engine(f"mysql+mysqlconnector://{user}:{pwd}@{host}/{database}")
    ```
5. Install the required libraries from [requirements.txt](requirements.txt)
6. You should now be able to generate a world with the slash command `/generate`
- - - - -
## Feature list
- Player movement & rendering
- Placing / Destroying `blocks`
- Physics affecting `blocks` and `entities` (sand, gravel, player gravity)
- World generation including ores, caves
- Multiplayer synced movement, servers wtih invite functionality
- 2D calculated lighting
- `Block` states with different rendering depending on the state
- Z-Axis so `blocks` can be rendered in the background/foreground
- - - - -
## Planned
- Redstone
- AI `entities` ( chicken, cow, zombie, . . )
- Structure generation