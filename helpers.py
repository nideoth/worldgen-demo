def get_adjacent_xy(x: int, y: int):
    adjacent = []
    
    adjacent.append((x-1, y-1))
    adjacent.append((x  , y-1))
    adjacent.append((x+1, y-1))
    adjacent.append((x-1, y  ))
    adjacent.append((x+1, y  ))
    adjacent.append((x-1, y+1))
    adjacent.append((x  , y+1))
    adjacent.append((x+1, y+1))

    return adjacent