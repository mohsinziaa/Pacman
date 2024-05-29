# Define a class named Button
class Button():

    # Constructor method to initialize the Button object
    def __init__(self, btnImage, pos, btnTxtInput, btnFont, btnColor, hovering_color):
        # Initialize attributes for the Button object
        self.btnImage = btnImage
        self.posX = pos[0]
        self.posY = pos[1]
        self.btnFont = btnFont
        self.btnColor, self.hovering_color = btnColor, hovering_color
        self.btnTxtInput = btnTxtInput
        # Render the btnText using the specified btnFont and base color
        self.btnText = self.btnFont.render(
            self.btnTxtInput, True, self.btnColor)
        # If no custom btnImage is provided, use the rendered btnText as the btnImage
        if self.btnImage is None:
            self.btnImage = self.btnText
        # Create rectangles for the btnImage and btnText, centered at the specified position
        self.imgRectangle = self.btnImage.get_rect(
            center=(self.posX, self.posY))
        self.btnText_rect = self.btnText.get_rect(
            center=(self.posX, self.posY))

    # Method to update the Button's appearance on the screen
    def update(self, screen):
        # If an btnImage is provided, draw it on the screen at the specified rectangle
        if self.btnImage is not None:
            screen.blit(self.btnImage, self.imgRectangle)
        # Draw the rendered btnText on the screen at the specified btnText rectangle
        screen.blit(self.btnText, self.btnText_rect)

    # Method to check if a given position is within the Button's boundaries
    def checkForInput(self, position):
        # Check if the position is within the rectangular boundaries of the Button
        if position[0] in range(self.imgRectangle.left, self.imgRectangle.right) and position[1] in range(self.imgRectangle.top, self.imgRectangle.bottom):
            return True  # Return True if the position is within the boundaries
        return False  # Return False otherwise

    # Method to change the btnText color when the mouse hovers over the Button
    def changeColor(self, position):
        # Check if the mouse position is within the boundaries of the Button
        if position[0] in range(self.imgRectangle.left, self.imgRectangle.right) and position[1] in range(self.imgRectangle.top, self.imgRectangle.bottom):
            # Render the btnText with the hovering color if the mouse is hovering
            self.btnText = self.btnFont.render(
                self.btnTxtInput, True, self.hovering_color)
        else:
            # Render the btnText with the base color if the mouse is not hovering
            self.btnText = self.btnFont.render(
                self.btnTxtInput, True, self.btnColor)
