from opensimplex import OpenSimplex

def generate_noise(width: int, height: int, seed: int, octaves: int = 3, persistence: float = 0.5, lacunarity: float = 2.0, period: float = 64.0) -> list[list[float]]:

    noise = [[0.0 for _ in range(height)] for _ in range(width)] 

    instances = []
    for i in range(octaves):
        instances.append(OpenSimplex(seed + i))

    amplitude = 1.0

    for i in range(octaves):
        for x in range(width):
            for y in range(height):
                noise[x][y] += instances[i].noise2(x / period, y / period) * amplitude
            #debug
            if (x+1)%32==0: print(f"oct: {i+1}/{octaves} x: {x+1}/{width}")
                
        amplitude *= persistence
        period /= lacunarity
    
    for x in range(width):
        for y in range(height):
            noise[x][y] = (noise[x][y] + 2) / 4

    #debug
    max = 0
    for x in range(width):
        for y in range(height):
            if abs(noise[x][y]) > max: max = abs(noise[x][y])
    print(f"max_abs: {max}")

    return noise

def generate_island_gradient(width: int, height: int) -> list[list[float]]:

    gradient = [[0.0 for _ in range(height)] for _ in range(width)]

    for x in range(width):
        for y in range(height):
            x_center = width / 2
            y_center = height / 2
            a = x_center - abs(x_center - x)
            b = y_center - abs(y_center - y)
            #gradient[x][y] = ((a / x_center) + (b / y_center))/2 - 0.1
            gradient[x][y] = min((((a / x_center) * (b / y_center)) * 2) + 0.2, 1.0)
    
    return gradient