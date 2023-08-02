import math

class BoundingBoxSorting:
    def getDistance(self, predictions):
        # ref https://shegocodes.medium.com/extract-text-from-image-left-to-right-and-top-to-bottom-with-keras-ocr-b56f098a6efe
        # Point of origin
        x0, y0 = 0, 0
        # Generate dictionary
        detections = []
        for group in predictions:
            print(group)
            # Get center point of bounding box [[188, 13], [2182, 13], [2182, 101], [188, 101]]
            top_left_x, top_left_y = group[1][0]
            bottom_right_x, bottom_right_y = group[1][1]
            center_x = (top_left_x + bottom_right_x) / 2
            center_y = (top_left_y + bottom_right_y) / 2
        # Use the Pythagorean Theorem to solve for distance from origin
        distance_from_origin = math.dist([x0, y0], [center_x, center_y])
        # Calculate difference between y and origin to get unique rows
        distance_y = center_y - y0
        # Append all results
        detections.append({
            'text': group[0],
            'center_x': center_x,
            'center_y': center_y,
            'distance_from_origin': distance_from_origin,
            'distance_y': distance_y
        })
        return detections

    def getSortedValues(self, ocrResult):
        directions = self.getDistance(ocrResult)
        print(directions)
