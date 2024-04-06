import os
import numpy as np
from PIL import Image
from sqlalchemy import and_
from Classes import WorldHasBlocks, Block, WorldHasUsers
from Commands.generate import world_width, world_height
from session import session

block_images_folder = "Blocks"
sky_color = (115, 210, 229)
view_range_width = 18  # 25
view_range_height = 15  # 20
light_strength = 15

def calculate_view_range(center_x, center_y, view_range_width, view_range_height):
    half_view_width = view_range_width // 2
    half_view_height = view_range_height // 2
    start_x = max(0, center_x - half_view_width)
    end_x = min(world_width, center_x + half_view_width)
    start_y = max(0, center_y - half_view_height)
    end_y = min(world_height, center_y + half_view_height)
    return start_x, end_x, start_y, end_y


def query_block_data(world_id, start_x, end_x, start_y, end_y):
    return session.query(WorldHasBlocks, Block) \
        .join(Block) \
        .filter(WorldHasBlocks.world_id == world_id) \
        .filter(WorldHasBlocks.x >= start_x, WorldHasBlocks.x < end_x) \
        .filter(WorldHasBlocks.y >= start_y, WorldHasBlocks.y < end_y) \
        .all()

async def render_world(world_id, user_id, debug=False):
    # we use the player_lower block as the root for camera position & collision checks
    user_root_block = session.query(WorldHasBlocks).join(WorldHasUsers, and_(
        WorldHasUsers.world_id == world_id,
        WorldHasUsers.user_id == user_id,
        WorldHasBlocks.id == WorldHasUsers.lower_block_id
    )).first()

    start_x, end_x, start_y, end_y = calculate_view_range(user_root_block.x, user_root_block.y, view_range_width, view_range_height)
    block_data = query_block_data(world_id, start_x, end_x, start_y, end_y)

    # sort blocks by z axis
    block_data.sort(key=lambda x: x[1].z)

    light_map = propagate_light(block_data)
    world_map_with_lighting = generate_world_map_with_lighting(light_map, block_data, start_x, start_y, end_x, end_y)

    if debug:
        print("Stored debug game view in /WorldOutput")
        world_map_with_lighting.save("WorldOutput/world_map.png")

    return world_map_with_lighting

def propagate_light(block_data):
    light_map = np.zeros((world_width, world_height), dtype=int)

    for block_rel, block in block_data:
        light_map[block_rel.x, block_rel.y] = block.light_level

    for _ in range(light_strength):
        for x in range(world_width):
            for y in range(world_height):
                if light_map[x, y] > 0:
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < world_width and 0 <= ny < world_height:
                                light_map[nx, ny] = max(light_map[nx, ny], light_map[x, y] - 1)

    return light_map


def get_block_sprite(block_rel, block):
    for state in block.block_states:
        if block_rel.state_active == state.state_active and block_rel.state_direction == state.state_direction:
            return state.sprite

    return 'error'


def generate_world_map_with_lighting(light_map, block_data, start_x, start_y, end_x, end_y):
    new_width = (end_x - start_x) * 16
    new_height = (end_y - start_y) * 16
    world_map = Image.new("RGBA", (new_width, new_height), color=sky_color)

    for block_rel, block in block_data:
        light_level = light_map[block_rel.x, block_rel.y]

        # Get neighboring light levels
        neighbor_light_levels = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = block_rel.x + dx, block_rel.y + dy
                if 0 <= nx < world_width and 0 <= ny < world_height:
                    neighbor_light_levels.append(light_map[nx, ny])

        # Calculate weighted average of current and neighboring light levels
        total_light_levels = sum(neighbor_light_levels) + light_level
        total_weights = len(neighbor_light_levels) + 1  # +1 to account for the current pixel
        avg_light_level = total_light_levels / total_weights

        # Calculate brightness based on the average light level
        brightness = int((avg_light_level / light_strength) * 255)

        sprite_image_name = get_block_sprite(block_rel, block)

        sprite_image_path = os.path.join(block_images_folder, f"{sprite_image_name}.png")
        block_sprite = Image.open(sprite_image_path).convert("RGBA")  # open block image in RGBA mode

        # convert block image to RGBA data
        data = block_sprite.getdata()

        # apply lighting only to non-transparent pixels
        new_data = []
        for item in data:
            # item is a tuple (R, G, B, A)
            if item[3] != 0:  # check if the pixel is not transparent
                # apply lighting to R, G, B channels
                new_item = tuple(int(i * brightness / 255) for i in item[:3]) + (item[3],)
            else:
                new_item = item
            new_data.append(new_item)

        # update block image with new data
        block_sprite.putdata(new_data)

        world_map.paste(block_sprite, ((block_rel.x - start_x) * 16, (block_rel.y - start_y) * 16),
                        block_sprite)  # use block image as mask for transparency

    return world_map