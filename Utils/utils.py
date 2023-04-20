import opensimplex

def generate_perlin_noise(width, height, scale, octaves, persistence, lacunarity, seed):
    noise = opensimplex.OpenSimplex(seed)
    noise_values = [[0 for y in range(height)] for x in range(width)]

    # Generate Perlin noise values for each point in the 2D array
    for x in range(width):
        for y in range(height):
            amplitude = 1.0
            frequency = 1.0
            noise_height = 0.0

            for i in range(octaves):
                sample_x = x / scale * frequency
                sample_y = y / scale * frequency
                value = noise.noise2(sample_x, sample_y) * 2 - 1
                noise_height += value * amplitude

                amplitude *= persistence
                frequency *= lacunarity

            noise_values[x][y] = noise_height

    return noise_values