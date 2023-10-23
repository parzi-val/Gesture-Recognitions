def calculate_pentagon_area(coordinates):
    if len(coordinates) != 5:
        raise ValueError("A pentagon has exactly 5 coordinates.")

    def triangle_area(x1, y1, x2, y2, x3, y3):
        return 0.5 * abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))

    x1, y1 = coordinates[0]
    x2, y2 = coordinates[1]
    x3, y3 = coordinates[2]
    x4, y4 = coordinates[3]
    x5, y5 = coordinates[4]

    # Calculate the areas of the five triangles
    area1 = triangle_area(x1, y1, x2, y2, x3, y3)
    area2 = triangle_area(x1, y1, x3, y3, x4, y4)
    area3 = triangle_area(x1, y1, x4, y4, x5, y5)
    area4 = triangle_area(x1, y1, x5, y5, x2, y2)
    area5 = triangle_area(x2, y2, x3, y3, x4, y4)

    # Sum the areas of the triangles to get the total area of the pentagon
    total_area = area1 + area2 + area3 + area4 + area5

    return total_area

